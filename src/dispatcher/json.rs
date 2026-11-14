pub type Json = serde_json::Value;

pub fn parse(input: &str) -> Result<Json, String> {
    serde_json::from_str(input).map_err(|e| e.to_string())
}

pub trait StringField {
    fn string_field(&self, key: &str) -> Option<String>;
}

impl StringField for Json {
    fn string_field(&self, key: &str) -> Option<String> {
        self.get(key).and_then(Json::as_str).map(str::to_string)
    }
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
        assert_eq!(parse("{}"), Ok(Json::Object(serde_json::Map::new())));
        assert_eq!(parse("[]"), Ok(Json::Array(Vec::new())));
        assert_eq!(parse("-1.5e2"), Ok(serde_json::json!(-150.0)));
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
        for _ in 0..200 {
            s.push('[');
        }
        for _ in 0..200 {
            s.push(']');
        }
        assert!(parse(&s).is_err());
    }

    #[test]
    fn object_keys_are_ordered() {
        let v = parse(r#"{"b":1,"a":2}"#).unwrap();
        let keys: Vec<&String> = match &v {
            Json::Object(m) => m.keys().collect(),
            _ => unreachable!(),
        };
        assert_eq!(keys, vec!["a", "b"]);
    }
}
