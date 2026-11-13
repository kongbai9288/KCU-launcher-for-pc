from pathlib import Path
import re
import sys

t = Path(__file__).resolve().parents[1] / "demos" / "ui-full-kcu-paper.html"
s = t.read_text()
s = re.sub(r"<script>[\s\S]*?</script>", "", s)
s = re.sub(r"<style>[\s\S]*?</style>", "", s)
s = re.sub(r'<section class="view" data-internal="1"[^>]*>[\s\S]*?</section>', "", s)
hits = re.findall(
    r"slot:|core\.[a-z]|plugin\.[a-z]|@modified|setid|未进构建|交接基线|新对话|"
    r"独立验证|四值|SHA-1|命中率|方案待定|演示构建|locked",
    s,
)
print("P09_HITS", len(hits), sorted(set(hits)))
sys.exit(1 if hits else 0)
