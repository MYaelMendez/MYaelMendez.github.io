//! continuity-core — Rust/WASM core for the governed continuity record.
//!
//! Port of the reactive half of `continuity.html`. The Rust core owns:
//!   - the SECTION model (read from JSON, never hardcoded),
//!   - reactive DERIVATION (INPUTS rewritten → whole result re-derived),
//!   - a real SHA-256 receipt over canonical state,
//!   - fail-closed parity (a marker that parses empty REFUSES).
//!
//! It deliberately does NOT own the authority verdict. That stays in the real
//! Mech wasm reading `authority.mec` out_string() — reimplementing it here
//! would create a second drifting copy of the policy (the exact failure the
//! stack exists to prevent).
//!
//!   derive(state_json, inputs_json) -> JSON derivation
//!   grade(state_json, inputs_json)  -> two derivations, byte-compared
//!   canon_sha256(bytes)             -> real SHA-256 hex
//!   doctor()                        -> what this core measures

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use wasm_bindgen::prelude::*;

/// One record section. Contract read from the artifact's fields.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Section {
    pub key: String,
    pub label: String,
    pub title: String,
    pub date: String,
    pub parity: String,
    pub has_proved: bool,
    pub has_broke: bool,
    pub has_change: bool,
}

/// ⟦inputs⟧ — rewritten on every Δ; the whole derivation is re-run.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Inputs {
    pub q: String,
    pub verdict: String,
}

impl Default for Inputs {
    fn default() -> Self {
        Inputs { q: String::new(), verdict: "all".to_string() }
    }
}

/// The derived result of INPUTS over the sections.
#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Derivation {
    pub schema: &'static str,
    pub visible: Vec<String>,
    pub count: usize,
    pub total: usize,
    pub query: String,
    pub verdict_filter: String,
    pub parity: String,
    pub receipt: String,
    pub refused: bool,
    pub reason: String,
}

fn canonical<T: Serialize>(v: &T) -> String {
    // serde_json with BTreeMap key ordering is deterministic; structs keep
    // declaration order, which is fixed here — so two calls produce equal bytes.
    serde_json::to_string(v).unwrap_or_default()
}

pub fn sha256_hex(bytes: &[u8]) -> String {
    let mut h = Sha256::new();
    h.update(bytes);
    let out = h.finalize();
    let mut s = String::with_capacity(64);
    for b in out {
        s.push_str(&format!("{:02x}", b));
    }
    s
}

/// Fail-closed parity: a verdict marker that parsed empty REFUSES.
fn parity_of(sections: &[Section]) -> String {
    if sections.iter().any(|s| s.parity == "MISSING") {
        "MISSING".to_string()
    } else {
        "ok".to_string()
    }
}

fn derive_inner(state_json: &str, inputs_json: &str) -> Derivation {
    let sections: Vec<Section> = match serde_json::from_str(state_json) {
        Ok(v) => v,
        Err(e) => {
            return Derivation {
                schema: "ae/continuity-derivation/1", visible: vec![], count: 0, total: 0,
                query: String::new(), verdict_filter: "all".to_string(), parity: "unknown".to_string(),
                receipt: String::new(), refused: true,
                reason: format!("REFUSED: state is not valid JSON: {}", e),
            }
        }
    };
    let inputs: Inputs = if inputs_json.is_empty() {
        Inputs::default()
    } else {
        match serde_json::from_str(inputs_json) {
            Ok(v) => v,
            Err(e) => {
                return Derivation {
                    schema: "ae/continuity-derivation/1", visible: vec![], count: 0,
                    total: sections.len(), query: String::new(), verdict_filter: "all".to_string(),
                    parity: parity_of(&sections), receipt: String::new(), refused: true,
                    reason: format!("REFUSED: inputs are not valid JSON: {}", e),
                }
            }
        }
    };

    let parity = parity_of(&sections);
    if parity == "MISSING" {
        return Derivation {
            schema: "ae/continuity-derivation/1", visible: vec![], count: 0,
            total: sections.len(), query: inputs.q, verdict_filter: inputs.verdict,
            parity, receipt: String::new(), refused: true,
            reason: "REFUSED: a section carries a verdict marker that parsed empty".to_string(),
        };
    }

    let term = inputs.q.trim().to_lowercase();
    let has = |s: &Section, k: &str| match k {
        "proved" => s.has_proved,
        "broke" => s.has_broke,
        "change" => s.has_change,
        _ => false,
    };
    let mut visible = Vec::new();
    for s in &sections {
        let hit = term.is_empty()
            || s.title.to_lowercase().contains(&term)
            || s.label.to_lowercase().contains(&term)
            || s.key.to_lowercase().contains(&term)
            || s.date.contains(&term);
        let filter_ok = inputs.verdict == "all" || has(s, &inputs.verdict);
        if hit && filter_ok {
            visible.push(s.key.clone());
        }
    }
    let receipt = sha256_hex(canonical(&(&sections, &inputs)).as_bytes());
    Derivation {
        schema: "ae/continuity-derivation/1", count: visible.len(), total: sections.len(),
        visible, query: inputs.q, verdict_filter: inputs.verdict, parity, receipt,
        refused: false, reason: String::new(),
    }
}

/// wasm-bindgen: rewrite INPUTS and re-derive. Same inputs → same receipt.
#[wasm_bindgen]
pub fn derive(state_json: &str, inputs_json: &str) -> String {
    canonical(&derive_inner(state_json, inputs_json))
}

/// Two derivations, byte-compared. A receipt is evidence only after both match.
#[wasm_bindgen]
pub fn grade(state_json: &str, inputs_json: &str) -> String {
    let a = derive_inner(state_json, inputs_json);
    let b = derive_inner(state_json, inputs_json);
    let same = canonical(&a) == canonical(&b) && !a.refused;
    format!(
        "{{\"ok\":{},\"refused\":{},\"receipt\":\"{}\",\"reason\":\"{}\"}}",
        same,
        !same,
        if same { a.receipt } else { String::new() },
        if same { "".to_string() } else if !a.reason.is_empty() {
            a.reason
        } else {
            "REFUSED: derivation is not deterministic".to_string()
        }
    )
}

/// Real SHA-256 over bytes — no placeholder hash.
#[wasm_bindgen]
pub fn canon_sha256(bytes: &[u8]) -> String {
    sha256_hex(bytes)
}

#[wasm_bindgen]
pub fn doctor() -> String {
    format!(
        "{{\"ok\":true,\"schema\":\"ae/continuity-core/1\",\"owns\":\"model+derivation+sha256\",\
\"never_owns\":\"authority verdict (Mech wasm reads authority.mec)\",\"rule\":\"INPUTS rewritten -> whole result re-derived\"}}"
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    fn state() -> String {
        r#"[
          {"key":"1","label":"§1","title":"alpha","date":"2026-11-01","parity":"ok","has_proved":true,"has_broke":false,"has_change":false},
          {"key":"2","label":"§2","title":"beta","date":"2026-11-02","parity":"ok","has_proved":false,"has_broke":true,"has_change":false},
          {"key":"3","label":"§3","title":"gamma","date":"2026-11-03","parity":"ok","has_proved":true,"has_broke":true,"has_change":true}
        ]"#.to_string()
    }

    #[test]
    fn derive_all_returns_every_section() {
        let d = derive_inner(&state(), "");
        assert_eq!(d.total, 3);
        assert_eq!(d.count, 3);
        assert!(!d.refused);
    }

    #[test]
    fn verdict_filter_is_real() {
        let d = derive_inner(&state(), r#"{"q":"","verdict":"broke"}"#);
        assert_eq!(d.visible, vec!["2", "3"]);
        let d2 = derive_inner(&state(), r#"{"q":"","verdict":"proved"}"#);
        assert_eq!(d2.visible, vec!["1", "3"]);
    }

    #[test]
    fn query_and_verdict_compose() {
        let d = derive_inner(&state(), r#"{"q":"gamma","verdict":"proved"}"#);
        assert_eq!(d.visible, vec!["3"]);
        let d2 = derive_inner(&state(), r#"{"q":"gamma","verdict":"none"}"#);
        assert!(d2.visible.is_empty());
    }

    #[test]
    fn same_inputs_give_same_receipt() {
        let a = derive_inner(&state(), r#"{"q":"a","verdict":"all"}"#);
        let b = derive_inner(&state(), r#"{"q":"a","verdict":"all"}"#);
        assert_eq!(a.receipt, b.receipt);
        assert_eq!(a.receipt.len(), 64);
    }

    #[test]
    fn parity_marker_refuses_closed() {
        let bad = state().replace("\"parity\":\"ok\"", "\"parity\":\"MISSING\"");
        let d = derive_inner(&bad, "");
        assert!(d.refused && d.count == 0);
        assert!(d.reason.contains("REFUSED"));
    }

    #[test]
    fn malformed_state_refuses() {
        let d = derive_inner("{not json", "");
        assert!(d.refused && d.reason.contains("REFUSED"));
    }

    #[test]
    fn sha256_is_real() {
        // SHA-256("abc") is a known vector.
        assert_eq!(sha256_hex(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
    }

    #[test]
    fn grade_green_on_valid_state() {
        let g = grade(&state(), "");
        assert!(g.contains("\"ok\":true"));
        assert!(!g.contains("\"ok\":false"));
    }

    #[test]
    fn doctor_declares_never_owns_authority() {
        let d = doctor();
        assert!(d.contains("authority verdict"));
    }
}
