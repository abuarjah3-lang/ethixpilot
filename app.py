"""EthixPilot: transparent, local-rule governance prototype.

Run: streamlit run app.py (Python 3.10+).
No API keys, network calls, model inference, certification, or external actions.
Inputs live in the browser and Streamlit server session; no application-level
file/database persistence. Hosting infrastructure has its own retention policy.
The detectors below are intentionally limited heuristics, not legal advice.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from collections import Counter
from datetime import datetime, timezone

import streamlit as st

VERSION = "0.3.0"
POLICY_VERSION = "EP-DEMO-2026.10-v1"
MAX_CHARS = 12000
DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
SEPARATORS = str.maketrans({"–": "-", "—": "-", "‑": "-", "−": "-", "\u00a0": " "})

# Match on a length-preserving normalized view so replacements keep their offsets.
# Candidates are masked conservatively without asserting identifier validity.
PII_RULES = [
    ("PRIVATE_KEY", r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "Potential private-key block"),
    ("UAE_IBAN", r"(?<![A-Za-z0-9])AE(?:[ \t-]*[0-9]){21}(?![ \t-]*[0-9])", "AE followed by 21 digits; candidate, not bank validation"),
    ("EMIRATES_ID", r"(?<![0-9])784(?:[ \t-]*[0-9]){12}(?![ \t-]*[0-9])", "15-digit candidate beginning 784; not identity validation"),
    ("UAE_PHONE", r"(?<![A-Za-z0-9])(?:(?:\+971|00971|971)[ \t-]*(?:5(?:[ \t-]*[0-9]){8}|[234679](?:[ \t-]*[0-9]){7})|05(?:[ \t-]*[0-9]){8}|0[234679](?:[ \t-]*[0-9]){7})(?![ \t-]*[0-9])", "Common UAE international, mobile and landline formats"),
    ("EMAIL", r"(?<![\w.+-])[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", "Common ASCII email pattern"),
    ("SECRET", r"(?i:(?:api[_ -]?key|access[_ -]?token|password|كلمة\s+المرور))\s*[:=]\s*[\"']?([^\s\"',;،]{6,})", "Explicitly labelled credential value, minimum six characters"),
]
COMPILED_PII = [(kind, re.compile(pattern, re.I), reason) for kind, pattern, reason in PII_RULES]
REVIEW_RULES = [
    ("FAIR-01", "fairness", r"الحسم الذكوري|للذكور فقط|للرجال فقط|استبعد.{0,35}(?:النساء|الاناث)|تفضيل خريجي الجامعات الاجنبية فقط|\b(?:men|males) only\b|\bexclude\b.{0,35}\bwomen\b|\bprefer\b.{0,30}\bmale\b", "Explicit exclusion or preference cue; context and intended use need human review."),
    ("FAIR-02", "fairness", r"\b(?:reject|exclude)\b.{0,40}\b(?:pregnant|disabled|older|nationality|religion)\b|استبعد.{0,35}(?:الحوامل|ذوي الاعاقة|كبار السن)", "Potential discriminatory selection criterion; not a legal determination."),
    ("INJ-01", "instruction_risk", r"ignore\s+(?:all\s+)?(?:previous|system)\s+instructions|reveal\s+(?:the\s+)?system\s+prompt|تجاهل\s+(?:كل\s+)?(?:التعليمات\s+السابقة|تعليمات\s+النظام)", "Potential instruction-override phrase; quoted educational text may also match."),
]
LIMITATIONS = [
    "Local regex/phrase rules only. No LLM or semantic understanding is claimed.",
    "Names, addresses, images, attachments, obfuscated secrets and many contexts are not covered.",
    "No flags means no match in enabled rules, not proof of safety, fairness or legal compliance.",
    "No official Dubai or ISO approval, certification, or exhaustive standard mapping.",
    "Masking substitutes text; it is not encryption or irreversible anonymization.",
    "No traffic interception or third-party model connection. Workflow actions are local simulations.",
]


def normalize(text: str) -> str:
    return text.translate(DIGITS).translate(SEPARATORS)


def detect_pii(text: str) -> list[dict]:
    view = normalize(text)
    candidates = []
    for kind, pattern, reason in COMPILED_PII:
        for match in pattern.finditer(view):
            start, end = match.span(1) if kind == "SECRET" else match.span()
            if kind == "SECRET" and text[start:end] == "[MASKED_SECRET]":
                continue
            candidates.append({"type": kind, "start": start, "end": end, "reason": reason})
    # Earlier rule order gives large sensitive spans priority over contained matches.
    accepted = []
    for item in candidates:
        if not any(item["start"] < old["end"] and item["end"] > old["start"] for old in accepted):
            accepted.append(item)
    return sorted(accepted, key=lambda item: item["start"])


def mask_text(text: str, findings: list[dict]) -> str:
    result = text
    for finding in reversed(findings):
        result = result[:finding["start"]] + "[MASKED_" + finding["type"] + "]" + result[finding["end"]:]
    return result


def review_flags(text: str) -> list[dict]:
    view = normalize(text).lower().translate(str.maketrans("أإآى", "اااي"))
    view = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", view)
    flags = []
    for rule_id, category, pattern, reason in REVIEW_RULES:
        if re.search(pattern, view, re.I):
            flags.append({"rule_id": rule_id, "category": category, "reason": reason})
    return flags


def analyze(text: str, scope: str = "full") -> dict:
    if not text.strip():
        raise ValueError("Empty text")
    if len(text) > MAX_CHARS:
        raise ValueError("Input too long")
    started = time.perf_counter()
    pii = detect_pii(text)
    flags = review_flags(text) if scope == "full" else []
    masked = mask_text(text, pii)
    elapsed_ms = (time.perf_counter() - started) * 1000
    return {
        "scan_id": str(uuid.uuid4()),
        "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "app_version": VERSION,
        "policy_version": POLICY_VERSION,
        "scope": scope,
        "characters": len(text),
        "processing_ms": round(elapsed_ms, 3),
        "pii": pii,
        "flags": flags,
        "counts": dict(Counter(item["type"] for item in pii)),
        "masked_text": masked,
        "status": "REVIEW_REQUIRED" if flags else "MASKING_REQUIRED" if pii else "NO_RULE_MATCHES",
    }


def run_workflow(text: str, redact: bool) -> dict:
    """Bounded deterministic workflow: inspect -> optionally mask -> recheck -> route.

    Never sends messages or calls an external system. Unresolved review flags are
    never automatically approved; no automatic 'ethical rewrite' is performed.
    """
    before = analyze(text)
    actions = [{"step": "inspect", "result": before["status"]}]
    candidate = before["masked_text"] if redact else text
    actions.append({"step": "mask", "result": f"{len(before['pii'])} candidate spans replaced" if redact else "Disabled by user"})
    after = analyze(candidate)
    if before["flags"] or after["flags"]:
        decision = "HUMAN_REVIEW_REQUIRED"
    elif after["pii"]:
        decision = "BLOCKED_BY_DEMO_POLICY"
    else:
        decision = "READY_FOR_HUMAN_CHECK"
    actions.extend([
        {"step": "recheck", "result": after["status"]},
        {"step": "route", "result": decision},
        {"step": "external_action", "result": "NOT_EXECUTED — local simulation only"},
    ])
    return {"before": before, "after": after, "decision": decision, "actions": actions, "candidate": candidate}


def evidence(scan: dict) -> dict:
    """Exports no raw input, replacement text, snippets or sensitive values."""
    return {key: scan[key] for key in (
        "scan_id", "created_at_utc", "app_version", "policy_version", "scope",
        "characters", "processing_ms", "counts", "flags", "status"
    )}


def make_report(mode: str, result: dict) -> dict:
    report = {
        "title": "EthixPilot — experimental evidence report / تقرير أدلة تجريبي",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "mode": mode,
        "certification": "NONE — not a compliance certificate",
        "raw_text_included": False,
        "limitations": LIMITATIONS,
    }
    if mode == "workflow":
        report.update(before=evidence(result["before"]), after=evidence(result["after"]), decision=result["decision"], actions=result["actions"])
    else:
        report["scan"] = evidence(result)
    return report


def main() -> None:
    st.set_page_config(page_title="EthixPilot | Governance Lab", page_icon="🛡️", layout="wide")
    english = st.sidebar.radio("Language / اللغة", ["العربية", "English"], key="language") == "English"

    def tr(ar: str, en: str) -> str:
        return en if english else ar

    st.markdown("""<style>
    .stApp {background:#f7f9fc;}
    h1,h2,h3 {color:#142a46;}
    div[data-testid="stMetric"] {background:white;border:1px solid #dce5ee;border-radius:12px;padding:14px;}
    .block-container {padding-top:2rem;}
    </style>""", unsafe_allow_html=True)
    st.title("🛡️ EthixPilot")
    st.write(tr("مختبر الحوكمة وحماية البيانات • نموذج تجريبي قابل للاختبار", "AI governance & privacy lab • testable prototype"))
    st.caption("Sharif Hamdan Arjah · Founder | v" + VERSION)
    st.info(tr("نسخة تجريبية بمحرك قواعد محلي. لا تعتمد على نموذج لغوي، ولا تمنح اعتمادًا رسميًا، ولا ترسل النصوص إلى مزودي نماذج خارجية.", "Local-rule prototype. No language model, official certification, or text transmission to external model providers."))
    with st.sidebar:
        st.subheader(tr("حدود التشغيل", "Operating scope"))
        st.write(tr("الفحص داخل خادم التطبيق؛ لا تحتاج إلى مفتاح API.", "Checks run on the app server; no API key needed."))
        st.caption(tr("استخدم بيانات اصطناعية. النص ينتقل من متصفحك إلى خادم Streamlit ويُحتفظ به أثناء الجلسة. التطبيق لا يكتب المدخلات في ملفات أو قاعدة بيانات؛ سياسة الاستضافة منفصلة. هذا ليس ضمان احتفاظ صفري.", "Use synthetic data. Text travels to the Streamlit server and is held during the session. Application code does not write inputs to files or a database; hosting retention is separate. This is not a zero-retention guarantee."))
        st.caption(tr("سياسة تجريبية: ", "Demo policy: ") + POLICY_VERSION)
        if st.button(tr("مسح جلسة التجربة", "Clear demo session"), key="clear"):
            for key in list(st.session_state.keys()):
                if key != "language":
                    del st.session_state[key]
            st.rerun()

    tabs = st.tabs([
        tr("🧪 فحص النص", "🧪 Playground"),
        tr("🛡️ حماية البيانات", "🛡️ Privacy shield"),
        tr("🔄 مسار المعالجة", "🔄 Remediation workflow"),
        tr("📑 تقرير الأدلة", "📑 Evidence report"),
        tr("ℹ️ نطاق الفحوص", "ℹ️ Check coverage"),
    ])

    status_labels = {
        "REVIEW_REQUIRED": tr("يحتاج مراجعة بشرية", "Human review required"),
        "MASKING_REQUIRED": tr("رُصدت بيانات مرشحة للحجب", "Potential sensitive data detected"),
        "NO_RULE_MATCHES": tr("لا تطابق مع القواعد المفعّلة", "No enabled rule matches"),
    }

    def show_scan(scan: dict) -> None:
        st.subheader(status_labels[scan["status"]])
        col1, col2, col3 = st.columns(3)
        col1.metric(tr("عناصر بيانات مكتشفة", "Detected data spans"), len(scan["pii"]))
        col2.metric(tr("تنبيهات مراجعة", "Review flags"), len(scan["flags"]))
        col3.metric(tr("زمن الفحص المحلي • ms", "Local scan time • ms"), f"{scan['processing_ms']:.3f}")
        st.caption(tr("قياس هذه العملية فقط، ولا يشمل الشبكة أو عرض الصفحة. ليس اختبار أداء مؤسسيًا.", "This scan only; excludes network and page rendering. Not an enterprise benchmark."))
        if scan["counts"]:
            st.table([{"Type": kind, "Count": count} for kind, count in scan["counts"].items()])
        for flag in scan["flags"]:
            st.warning(flag["rule_id"] + " · " + flag["reason"])
        if scan["flags"]:
            st.caption(tr("قد تكون العبارة اقتباسًا أو نفيًا أو مثالًا تعليميًا؛ يلزم فحص السياق. لا يحذف النظام معايير الاختيار تلقائيًا.", "A match may be a quotation, negation, or educational example. Context needs review; selection criteria are not silently rewritten."))
        st.caption(tr("غياب التنبيهات لا يثبت سلامة النص أو عدالته أو امتثاله القانوني.", "No flags does not prove safety, fairness, or legal compliance."))
        st.write(tr("نسخة بحجب الأنماط المكتشفة فقط:", "Copy with detected patterns masked only:"))
        st.code(scan["masked_text"], language=None)

    with tabs[0]:
        st.subheader(tr("اختبر نصًا من اختيارك", "Test your own text"))
        text = st.text_area(tr("النص المراد فحصه", "Text to inspect"), key="prompt_input", height=180, max_chars=MAX_CHARS,
                            placeholder=tr("مثال اصطناعي: استبعد النساء من قائمة المرشحين، وأرسل الرد إلى demo@example.com", "Synthetic example: Exclude women from the shortlist and email demo@example.com"))
        if st.button(tr("فحص النص", "Inspect text"), key="scan_prompt", type="primary"):
            if text.strip():
                result = analyze(text)
                st.session_state["prompt_result"] = (text, result)
                st.session_state["latest_report"] = make_report("playground", result)
                st.session_state["report_source"] = ("prompt_input", text, None)
            else:
                st.warning(tr("أدخل نصًا أولًا.", "Enter text first."))
        saved = st.session_state.get("prompt_result")
        if saved and saved[0] == text:
            show_scan(saved[1])
        elif saved:
            st.info(tr("تغيّر النص؛ أعد الفحص لتحديث النتيجة والتقرير.", "Input changed. Run a new scan to update results and report."))

    with tabs[1]:
        st.subheader(tr("فحص الخصوصية وحجب الأنماط", "Privacy pattern detection & masking"))
        st.caption(tr("بريد إلكتروني، هوية إماراتية محتملة، IBAN إماراتي محتمل، أرقام هاتف إماراتية، وقيم أسرار معنونة. يدعم الأرقام العربية والفارسية وتنسيقات شائعة.", "Email, candidate Emirates ID/UAE IBAN, common UAE phones, and labelled secrets. Arabic/Persian digits and common separators supported."))
        text = st.text_area(tr("بيانات اصطناعية للاختبار", "Synthetic test data"), key="privacy_input", height=150, max_chars=MAX_CHARS,
                            placeholder="demo@example.com | 784200000000000 | +971 50 000 0000")
        if st.button(tr("فحص وحجب", "Inspect & mask"), key="scan_privacy", type="primary"):
            if text.strip():
                result = analyze(text, "privacy")
                st.session_state["privacy_result"] = (text, result)
                st.session_state["latest_report"] = make_report("privacy", result)
                st.session_state["report_source"] = ("privacy_input", text, None)
            else:
                st.warning(tr("أدخل نصًا أولًا.", "Enter text first."))
        saved = st.session_state.get("privacy_result")
        if saved and saved[0] == text:
            show_scan(saved[1])
            st.info(tr(f"استُبدل {len(saved[1]['pii'])} عنصرًا وفق الأنماط المفعّلة. هذا حجب نصي، وليس تشفيرًا.", f"Replaced {len(saved[1]['pii'])} detected spans. This is masking, not encryption."))
        elif saved:
            st.info(tr("تغيّر النص؛ أعد الفحص.", "Input changed. Scan again."))

    with tabs[2]:
        st.subheader(tr("اكتشاف ← حجب ← إعادة فحص ← إحالة", "Inspect → mask → recheck → route"))
        st.caption(tr("محاكاة محلية محدودة لتنظيم خطوات المعالجة. لا ينفّذ إرسالًا أو قرارات توظيف أو إجراءات خارجية، وليس وكيلًا مستقلاً كاملًا.", "Bounded local workflow simulation. No sending, hiring decisions, or external actions. Not a fully autonomous AI agent."))
        text = st.text_area(tr("مسودة رسالة أو أمر للاختبار", "Draft message or instruction"), key="workflow_input", max_chars=MAX_CHARS, height=150)
        redact = st.checkbox(tr("السماح بحجب الأنماط المكتشفة داخل التجربة", "Allow detected-pattern masking in this simulation"), value=True, key="redact")
        if st.button(tr("تشغيل مسار المعالجة", "Run remediation workflow"), key="run_workflow", type="primary"):
            if text.strip():
                result = run_workflow(text, redact)
                st.session_state["workflow_result"] = (text, redact, result)
                st.session_state["latest_report"] = make_report("workflow", result)
                st.session_state["report_source"] = ("workflow_input", text, redact)
            else:
                st.warning(tr("أدخل نصًا أولًا.", "Enter text first."))
        saved = st.session_state.get("workflow_result")
        if saved and saved[:2] == (text, redact):
            result = saved[2]
            labels = {
                "HUMAN_REVIEW_REQUIRED": tr("توقف: يلزم تقييم بشري للمخاطر المرصودة.", "Stopped: human risk review required."),
                "BLOCKED_BY_DEMO_POLICY": tr("توقف: بقيت بيانات مرصودة دون حجب.", "Stopped: detected data remains unmasked."),
                "READY_FOR_HUMAN_CHECK": tr("جاهز للفحص البشري؛ لم يُنفّذ أي إرسال.", "Ready for human check; nothing was sent."),
            }
            st.info(labels[result["decision"]])
            st.table(result["actions"])
            st.write(tr("نتيجة إعادة الفحص:", "Recheck result:"))
            show_scan(result["after"])
            if result["before"]["flags"]:
                st.write(tr("تنبيهات الفحص الأول:", "Initial review flags:"))
                st.table(result["before"]["flags"])
        elif saved:
            st.info(tr("تغيّر النص أو الإذن؛ شغّل المسار مجددًا.", "Input or permission changed. Run the workflow again."))

    with tabs[3]:
        st.subheader(tr("تقرير أدلة تجريبي — غير معتمد", "Experimental evidence report — not certified"))
        report = st.session_state.get("latest_report")
        source = st.session_state.get("report_source")
        fresh = source and st.session_state.get(source[0]) == source[1] and (source[2] is None or st.session_state.get("redact") == source[2])
        if report and fresh:
            st.caption(tr("آخر عملية مكتملة فقط. لا يتضمن النص الخام أو القيم المحجوبة. يحتوي أنواع النتائج ومعرّفات القواعد والأوقات.", "Latest completed run only. Excludes raw text and masked values. Includes result types, rule IDs and timestamps."))
            payload = json.dumps(report, ensure_ascii=False, indent=2)
            st.json(report)
            st.download_button(tr("تنزيل تقرير JSON", "Download JSON report"), payload.encode("utf-8"), file_name="ethixpilot-evidence.json", mime="application/json", key="download_json")
            st.download_button(tr("تنزيل تقرير TXT", "Download TXT report"), payload.encode("utf-8-sig"), file_name="ethixpilot-evidence.txt", mime="text/plain", key="download_txt")
        elif report:
            st.warning(tr("مدخلات التقرير الأخير تغيّرت. أعد تشغيل الفحص قبل تصدير تقرير جديد.", "The last report's input changed. Rerun its check before exporting."))
        else:
            st.info(tr("نفّذ فحصًا لإنشاء تقرير مبني على النتائج.", "Run a check to generate an evidence-based report."))

    with tabs[4]:
        st.subheader(tr("ما الذي تفحصه هذه النسخة؟", "What does this version check?"))
        st.table([{"Rule": kind, "Coverage": reason} for kind, _, reason in PII_RULES])
        st.table([{"Rule": rid, "Category": category, "Coverage": reason} for rid, category, _, reason in REVIEW_RULES])
        for limitation in LIMITATIONS:
            st.write("• " + limitation)
        st.warning(tr("القواعد سياسة تجريبية داخلية، وليست ترجمة معتمدة لمبادئ دبي أو ISO/IEC 42001. لا يوجد Ethix Score أو اعتماد آلي.", "Rules are an internal demo policy, not an approved implementation of Dubai principles or ISO/IEC 42001. No Ethix Score or automatic certification."))


if __name__ == "__main__":
    main()
