use std::collections::BTreeMap;

const MAX_DEPTH: usize = 64;

#[derive(Debug, Clone, PartialEq)]
pub enum Json {
    Null,
    Bool(bool),
    Num(f64),
    Str(String),
    Arr(Vec<Json>),
    Obj(BTreeMap<String, Json>),
}

impl Json {
    pub fn get(&self, key: &str) -> Option<&Json> {
        match self {
            Json::Obj(m) => m.get(key),
            _ => None,
        }
    }

    pub fn as_str(&self) -> Option<&str> {
        match self {
            Json::Str(s) => Some(s),
            _ => None,
        }
    }

    pub fn as_bool(&self) -> Option<bool> {
        match self {
            Json::Bool(b) => Some(*b),
            _ => None,
        }
    }

    pub fn as_u64(&self) -> Option<u64> {
        match self {
            Json::Num(n) if *n >= 0.0 && n.fract() == 0.0 => Some(*n as u64),
            _ => None,
        }
    }

    pub fn as_array(&self) -> Option<&[Json]> {
        match self {
            Json::Arr(a) => Some(a),
            _ => None,
        }
    }

    pub fn string_field(&self, key: &str) -> Option<String> {
        self.get(key).and_then(Json::as_str).map(str::to_string)
    }
}

struct Reader<'a> {
    src: &'a [u8],
    pos: usize,
    depth: usize,
}

impl<'a> Reader<'a> {
    fn new(src: &'a str) -> Self {
        Self {
            src: src.as_bytes(),
            pos: 0,
            depth: 0,
        }
    }

    fn ws(&mut self) {
        while self.pos < self.src.len() && self.src[self.pos].is_ascii_whitespace() {
            self.pos += 1;
        }
    }

    fn err(&self, message: &str) -> String {
        format!("{} at byte {}", message, self.pos)
    }

    fn enter(&mut self) -> Result<(), String> {
        self.depth += 1;
        if self.depth > MAX_DEPTH {
            return Err(self.err("depth limit"));
        }
        Ok(())
    }

    fn leave(&mut self) {
        self.depth = self.depth.saturating_sub(1);
    }

    fn value(&mut self) -> Result<Json, String> {
        self.ws();
        let b = *self.src.get(self.pos).ok_or_else(|| self.err("unexpected end"))?;
        match b {
            b'{' => self.object(),
            b'[' => self.array(),
            b'"' => Ok(Json::Str(self.string()?)),
            b't' => {
                self.literal(b"true")?;
                Ok(Json::Bool(true))
            }
            b'f' => {
                self.literal(b"false")?;
                Ok(Json::Bool(false))
            }
            b'n' => {
                self.literal(b"null")?;
                Ok(Json::Null)
            }
            b'-' | b'0'..=b'9' => self.number(),
            _ => Err(self.err("unexpected token")),
        }
    }

    fn literal(&mut self, word: &[u8]) -> Result<(), String> {
        if self.src.get(self.pos..self.pos + word.len()) == Some(word) {
            self.pos += word.len();
            Ok(())
        } else {
            Err(self.err("invalid literal"))
        }
    }

    fn object(&mut self) -> Result<Json, String> {
        self.enter()?;
        self.pos += 1;
        let mut map = BTreeMap::new();
        self.ws();
        if self.src.get(self.pos) == Some(&b'}') {
            self.pos += 1;
            self.leave();
            return Ok(Json::Obj(map));
        }
        loop {
            self.ws();
            if self.src.get(self.pos) != Some(&b'"') {
                return Err(self.err("object key expected"));
            }
            let key = self.string()?;
            self.ws();
            if self.src.get(self.pos) != Some(&b':') {
                return Err(self.err("colon expected"));
            }
            self.pos += 1;
            let value = self.value()?;
            map.insert(key, value);
            self.ws();
            match self.src.get(self.pos) {
                Some(b',') => self.pos += 1,
                Some(b'}') => {
                    self.pos += 1;
                    self.leave();
                    return Ok(Json::Obj(map));
                }
                _ => return Err(self.err("comma or close expected")),
            }
        }
    }

    fn array(&mut self) -> Result<Json, String> {
        self.enter()?;
        self.pos += 1;
        let mut items = Vec::new();
        self.ws();
        if self.src.get(self.pos) == Some(&b']') {
            self.pos += 1;
            self.leave();
            return Ok(Json::Arr(items));
        }
        loop {
            items.push(self.value()?);
            self.ws();
            match self.src.get(self.pos) {
                Some(b',') => self.pos += 1,
                Some(b']') => {
                    self.pos += 1;
                    self.leave();
                    return Ok(Json::Arr(items));
                }
                _ => return Err(self.err("comma or close expected")),
            }
        }
    }

    fn string(&mut self) -> Result<String, String> {
        self.pos += 1;
        let mut out = String::new();
        while self.pos < self.src.len() {
            let b = self.src[self.pos];
            self.pos += 1;
            match b {
                b'"' => return Ok(out),
                b'\\' => {
                    let e = *self.src.get(self.pos).ok_or_else(|| self.err("bad escape"))?;
                    self.pos += 1;
                    match e {
                        b'"' => out.push('"'),
                        b'\\' => out.push('\\'),
                        b'/' => out.push('/'),
                        b'b' => out.push('\u{0008}'),
                        b'f' => out.push('\u{000c}'),
                        b'n' => out.push('\n'),
                        b'r' => out.push('\r'),
                        b't' => out.push('\t'),
                        b'u' => {
                            let hex = self.src.get(self.pos..self.pos + 4).ok_or_else(|| self.err("bad unicode"))?;
                            let text = std::str::from_utf8(hex).map_err(|_| self.err("bad unicode"))?;
                            let cp = u32::from_str_radix(text, 16).map_err(|_| self.err("bad unicode"))?;
                            self.pos += 4;
                            out.push(char::from_u32(cp).unwrap_or('\u{fffd}'));
                        }
                        _ => return Err(self.err("bad escape")),
                    }
                }
                0..=31 => return Err(self.err("control character")),
                _ => {
                    let start = self.pos - 1;
                    let mut end = start;
                    while end < self.src.len() && self.src[end] >= 0x20 && self.src[end] != b'"' && self.src[end] != b'\\' {
                        end += 1;
                    }
                    let chunk = std::str::from_utf8(&self.src[start..end]).map_err(|_| self.err("invalid utf-8"))?;
                    out.push_str(chunk);
                    self.pos = end;
                }
            }
        }
        Err(self.err("unterminated string"))
    }

    fn number(&mut self) -> Result<Json, String> {
        let start = self.pos;
        if self.src.get(self.pos) == Some(&b'-') {
            self.pos += 1;
        }
        let int_start = self.pos;
        while matches!(self.src.get(self.pos), Some(b'0'..=b'9')) {
            self.pos += 1;
        }
        if self.pos - int_start > 1 && self.src[int_start] == b'0' {
            return Err(self.err("leading zero"));
        }
        if self.src.get(self.pos) == Some(&b'.') {
            self.pos += 1;
            while matches!(self.src.get(self.pos), Some(b'0'..=b'9')) {
                self.pos += 1;
            }
        }
        if matches!(self.src.get(self.pos), Some(b'e') | Some(b'E')) {
            self.pos += 1;
            if matches!(self.src.get(self.pos), Some(b'+') | Some(b'-')) {
                self.pos += 1;
            }
            while matches!(self.src.get(self.pos), Some(b'0'..=b'9')) {
                self.pos += 1;
            }
        }
        let text = std::str::from_utf8(&self.src[start..self.pos]).map_err(|_| self.err("bad number"))?;
        let n = text.parse::<f64>().map_err(|_| self.err("bad number"))?;
        Ok(Json::Num(n))
    }
}

pub fn parse(input: &str) -> Result<Json, String> {
    let mut r = Reader::new(input);
    let value = r.value()?;
    r.ws();
    if r.pos != r.src.len() {
        return Err(r.err("trailing content"));
    }
    Ok(value)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_object_with_nested_values() {
        let v = parse(r#"{"id":"t1","mem":2048,"first":true,"tags":["a","b"],"extra":null}"#).unwrap();
        assert_eq!(v.string_field("id").as_deref(), Some("t1"));
        assert_eq!(v.get("mem").unwrap().as_u64(), Some(2048));
        assert_eq!(v.get("first").unwrap().as_bool(), Some(true));
        assert_eq!(v.get("tags").unwrap().as_array().unwrap().len(), 2);
        assert_eq!(v.get("extra"), Some(&Json::Null));
    }

    #[test]
    fn parses_escapes_and_unicode() {
        let v = parse(r#"{"s":"a\n\t\"\\\u4e2d\u6587"}"#).unwrap();
        assert_eq!(v.string_field("s").as_deref(), Some("a\n\t\"\\中文"));
    }

    #[test]
    fn parses_empty_containers_and_negative_numbers() {
        assert_eq!(parse("{}"), Ok(Json::Obj(BTreeMap::new())));
        assert_eq!(parse("[]"), Ok(Json::Arr(Vec::new())));
        assert_eq!(parse("-1.5e2"), Ok(Json::Num(-150.0)));
    }

    #[test]
    fn rejects_trailing_content() {
        assert!(parse("{} {}").is_err());
    }

    #[test]
    fn rejects_malformed_input() {
        for s in ["{", "[1,]", "{\"a\" 1}", "tru", "\"unterminated", "{\"a\":01}"] {
            assert!(parse(s).is_err(), "{}", s);
        }
    }

    #[test]
    fn rejects_excessive_depth() {
        let mut s = String::new();
        for _ in 0..80 {
            s.push('[');
        }
        for _ in 0..80 {
            s.push(']');
        }
        assert!(parse(&s).is_err());
    }

    #[test]
    fn object_keys_are_ordered() {
        let v = parse(r#"{"b":1,"a":2}"#).unwrap();
        let keys: Vec<&String> = match &v {
            Json::Obj(m) => m.keys().collect(),
            _ => unreachable!(),
        };
        assert_eq!(keys, vec!["a", "b"]);
    }
}
