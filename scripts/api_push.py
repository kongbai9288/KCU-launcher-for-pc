import base64
import json
import os
import re
import stat
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://api.github.com"
UA = "KCU-Launcher-Desktop/0.0.0"
ACCEPT = "application/vnd.github+json"
VERSION = "2022-11-28"


def request(method, path, body=None):
    token = os.environ.get("KCU_PAT")
    if not token:
        raise RuntimeError("KCU_PAT required")
    headers = {
        "User-Agent": UA,
        "Accept": ACCEPT,
        "X-GitHub-Api-Version": VERSION,
        "Authorization": "token " + token,
    }
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            payload = json.loads(raw) if raw else {}
        except ValueError:
            payload = {"raw": raw.decode("utf-8", "replace")[:300]}
        return exc.code, payload
    except urllib.error.URLError as exc:
        return 0, {"reason": str(exc.reason)}


def repo_slug():
    url = subprocess.check_output(["git", "remote", "get-url", "origin"], text=True).strip()
    match = re.search(r"github\.com[/:]([^/]+)/([^/.]+?)(?:\.git)?/?$", url)
    if not match:
        raise RuntimeError("remote url not parseable: " + url)
    return match.group(1) + "/" + match.group(2)


def tracked_files():
    raw = subprocess.check_output(["git", "ls-files", "-z"])
    return [os.fsdecode(p) for p in raw.split(b"\0") if p]


def blob(content, local_sha, existing):
    if local_sha in existing:
        return local_sha
    status, payload = request(
        "POST",
        "/repos/" + REPO + "/git/blobs",
        {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
    )
    if status != 201:
        status, payload = request(
            "POST",
            "/repos/" + REPO + "/git/blobs",
            {"content": base64.b64encode(content).decode("ascii"), "encoding": "base64"},
        )
    if status != 201:
        raise RuntimeError("blob create " + str(status) + " " + json.dumps(payload, ensure_ascii=False)[:300])
    return payload["sha"]


def remote_blobs(parent):
    if not parent:
        return set()
    status, commit = request("GET", "/repos/" + REPO + "/git/commits/" + parent)
    if status != 200:
        return set()
    status, tree = request("GET", "/repos/" + REPO + "/git/trees/" + commit["tree"]["sha"] + "?recursive=1")
    if status != 200:
        return set()
    return set(x["sha"] for x in tree.get("tree", []) if x.get("type") == "blob")


def bootstrap(branch):
    status, payload = request(
        "PUT",
        "/repos/" + REPO + "/contents/README.md",
        {
            "message": "init",
            "content": base64.b64encode(b"init\n").decode("ascii"),
            "encoding": "base64",
            "branch": branch,
        },
    )
    if status not in (200, 201):
        raise RuntimeError("bootstrap " + str(status) + " " + json.dumps(payload, ensure_ascii=False)[:300])
    log("bootstrap", branch, "OK", "commit=" + payload["commit"]["sha"][:7] + " via=contents_api")
    return payload["commit"]["sha"]


def log(action, target, result, detail):
    print("[KCU] remote " + action + " " + target + " " + result + " " + detail)


def main():
    global REPO
    REPO = repo_slug()
    branch = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"], text=True).strip()
    message = sys.argv[1] if len(sys.argv) > 1 else "snapshot"
    paths = tracked_files()
    if not paths:
        log("push", branch, "FAIL", "empty_file_list")
        return 2

    ref_path = "/repos/" + REPO + "/git/ref/heads/" + branch
    status, ref = request("GET", ref_path)
    parent = None
    if status == 200:
        parent = ref.get("object", {}).get("sha")
    elif status == 409:
        parent = bootstrap(branch)
    else:
        log("ref", branch, "FAIL", "http=" + str(status) + " " + json.dumps(ref, ensure_ascii=False)[:300])
        return 1

    existing = remote_blobs(parent)

    def one(path):
        with open(path, "rb") as handle:
            content = handle.read()
        local_sha = subprocess.check_output(["git", "hash-object", path], text=True).strip()
        sha = blob(content, local_sha, existing)
        mode = "100755" if os.stat(path).st_mode & stat.S_IXUSR else "100644"
        return {"path": path, "mode": mode, "type": "blob", "sha": sha}

    with ThreadPoolExecutor(max_workers=8) as pool:
        tree = list(pool.map(one, paths))
    log("blob", str(len(tree)), "OK", "concurrent=8 remote_reused=" + str(len(existing)))

    status, tree_obj = request("POST", "/repos/" + REPO + "/git/trees", {"tree": tree})
    if status != 201:
        log("tree", branch, "FAIL", "http=" + str(status) + " " + json.dumps(tree_obj, ensure_ascii=False)[:300])
        return 1

    commit_body = {"message": message, "tree": tree_obj["sha"]}
    if parent:
        commit_body["parents"] = [parent]
    status, commit = request("POST", "/repos/" + REPO + "/git/commits", commit_body)
    if status != 201:
        log("commit", branch, "FAIL", "http=" + str(status) + " " + json.dumps(commit, ensure_ascii=False)[:300])
        return 1

    if parent:
        status, result = request(
            "PATCH", "/repos/" + REPO + "/git/refs/heads/" + branch,
            {"sha": commit["sha"], "force": False},
        )
        expected = 200
    else:
        status, result = request(
            "POST", "/repos/" + REPO + "/git/refs",
            {"ref": "refs/heads/" + branch, "sha": commit["sha"]},
        )
        expected = 201
    if status != expected:
        log("ref", branch, "FAIL", "http=" + str(status) + " " + json.dumps(result, ensure_ascii=False)[:300])
        return 1

    log("push", branch, "OK", "commit=" + commit["sha"][:7] + " files=" + str(len(tree)) + " via=git_data_api")
    return 0


if __name__ == "__main__":
    sys.exit(main())
