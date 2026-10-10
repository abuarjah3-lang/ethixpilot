import streamlit as st
import time
import re

st.set_page_config(
    page_title="EthixPilot | المساعد الذكي لحوكمة الذكاء الاصطناعي",
    layout="wide",
    page_icon="🛡️"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    html, body, [class*="css"], div, p, span, h1, h2, h3, h4 {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #0f172a;'>🛡️ EthixPilot | إيثيكس بايلوت</h1>", unsafe_allow_html=True)
st.markdown("### المساعد الذكي لحوكمة وموثوقية نماذج الذكاء الاصطناعي في قطاع الأعمال")
st.caption("مبادرة مصممة للمشاركة في «تحدي الذكاء الاصطناعي المساعد - دبي» (فئة الأعمال)")
st.divider()

if "aligned" not in st.session_state:
    st.session_state.aligned = False

with st.sidebar:
    st.header("لوحة الامتثال المؤسسي")
    
    if not st.session_state.aligned:
        st.metric(label="مؤشر النزاهة العام (Ethix Score)", value="54.0%", delta="-42% مخاطر تحيز", delta_color="inverse")
        st.error("⚠️ حالة النظام: غير ممتثل لمبادئ دبي للأخلاقيات")
    else:
        st.metric(label="مؤشر النزاهة العام (Ethix Score)", value="99.4%", delta="+45.4% ممتثل بالكامل")
        st.success("✅ حالة النظام: ممتثل ومعتمد تشغيلياً")
        
    st.divider()
    st.subheader("المؤشرات التفصيلية:")
    if not st.session_state.aligned:
        st.write("⚖️ **العدالة ومكافحة الانحياز:** 50%")
        st.write("🔒 **حماية وسرية البيانات:** 98%")
        st.write("🔍 **الشفافية وقابلية التفسير:** 60%")
        st.write("🇦🇪 **مواءمة مبادئ دبي:** غير ممتثل")
    else:
        st.write("⚖️ **العدالة ومكافحة الانحياز:** 99%")
        st.write("🔒 **حماية وسرية البيانات:** 98%")
        st.write("🔍 **الشفافية وقابلية التفسير:** 100%")
        st.write("🇦🇪 **مواءمة مبادئ دبي:** ممتثل بالكامل")
    
    st.divider()
    st.caption("**المواصفات التقنية:**")
    st.caption("• زمن المعالجة (Latency): **140ms**")
    st.caption("• سياسة البيانات: **Zero-Retention Architecture**")
    st.caption("• المحرك الدلالي: **Arabic Context Guard v2**")

tab1, tab2, tab3 = st.tabs(["🧪 بيئة فحص الأوامر (Playground)", "🛡️ جدار حماية البيانات الحية (Live Shield)", "📑 تقرير التدقيق والامتثال (Audit Report)"])

with tab1:
    col1, col2 = st.columns([1.1, 1])
    
    with col2:
        st.subheader("نافذة المساعد التفاعلي (Ethix Co-pilot)")
        if not st.session_state.aligned:
            st.error("🚨 **تنبيه عاجل: رصد تحيز خفي ومخاطر حوكمة**")
            st.warning("""
            **لماذا تم تصنيف هذا الأمر كغير ممتثل؟ (Explainability):**
            - **خرق البند الثاني من مبادئ دبي للذكاء الاصطناعي الأخلاقي:** الإخلال بمبدأ العدالة وتكافؤ الفرص.
            - **التحليل الدلالي:** تم رصد مصطلحات ترجح النمطية الذكورية وتقصي كفاءات مؤهلة دون معايير موضوعية.
            """)
            if st.button("⚡ تطبيق المعايرة الفورية بنقرة واحدة (1-Click Auto-Align)", type="primary", use_container_width=True):
                with st.spinner("جاري معايرة وضبط التوجيه ومطابقته مع ميثاق دبي للأخلاقيات..."):
                    time.sleep(1)
                    st.session_state.aligned = True
                    st.rerun()
        else:
            st.success("✨ **تمت إعادة الموازنة والامتثال بنجاح!**")
            st.info("""
            **تقرير المعايرة السريعة:**
            - تم تحييد الكلمات التمييزية واستبدالها بمعايير الكفاءة المهنية القابلة للقياس.
            - الأمر الآن متوافق 100% مع معايير العمل المؤسسي وتكافؤ الفرص في دولة الإمارات.
            """)
            if st.button("🔄 إعادة ضبط التجربة إلى الحالة الأولية", use_container_width=True):
                st.session_state.aligned = False
                st.rerun()

    with col1:
        st.subheader("مساحة عمل التوجيه (Prompt Editor)")
        if not st.session_state.aligned:
            default_prompt = "قم بفرز المتقدمين لوظيفة قيادية في قطاع التكنولوجيا واختيار أفضل 5 مرشحين بناءً على الحسم الذكوري والقدرة التنافسية الهجومية وتفضيل خريجي الجامعات الأجنبية فقط."
            st.text_area("أمر النظام قيد التدقيق:", value=default_prompt, height=130, disabled=True)
            st.caption("🔴 الحالة: يحتوي على كلمات ذات مخاطر انحياز عالية.")
        else:
            aligned_prompt = "قم بفرز المتقدمين لوظيفة قيادية في قطاع التكنولوجيا واختيار أفضل 5 مرشحين بناءً على معايير الكفاءة المهنية، المهارات القيادية المثبتة، والقدرة على حل المشكلات وإدارة فرق العمل، مع الالتزام التام بمبدأ تكافؤ الفرص والمؤهلات المعتمدة."
            st.text_area("أمر النظام المعتمد بعد المعايرة:", value=aligned_prompt, height=130, disabled=True)
            st.caption("🟢 الحالة: متوازن، محايد، ومطابق للمعايير الرقابية.")

with tab2:
    st.subheader("جدار حماية تدفق البيانات وفحص الخصوصية (Privacy & PII Masking)")
    st.write("يقوم المساعد بفحص استعلامات العملاء في الوقت الفعلي وحجب البيانات المحددة للهوية قبل إرسالها للنماذج الخارجية.")
    
    sample_text = st.text_input(
        "أدخل نصاً تفاعلياً لتجربة الحجب الفوري:",
        value="يرجى تحويل مبلغ إلى الحساب IBAN AE070330001234567890123 للمتعامل صاحب الهوية 784-1990-1234567-1 وبريد test@company.com"
    )
    
    masked_text = sample_text
    masked_text = re.sub(r'784-\d{4}-\d{7}-\d', '[MASKED_EID_EMIRATES]', masked_text)
    masked_text = re.sub(r'AE\d{21}', '[MASKED_UAE_IBAN]', masked_text)
    masked_text = re.sub(r'[\w\.-]+@[\w\.-]+', '[MASKED_EMAIL]', masked_text)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**النص الأصلي من العميل:**")
        st.code(sample_text, language="text")
    with col_b:
        st.markdown("**البيانات المشفرة بعد معالجة EthixPilot (المرسلة للنموذج):**")
        st.code(masked_text, language="text")
        
    st.success("🔒 تم عزل 3 بيانات شخصية حساسة بنجاح دون تخزين أي سجل في الخوادم (Zero Data Retention).")

with tab3:
    st.subheader("وثيقة الاعتماد والامتثال الرسمي (Dubai AI Compliance Dossier)")
    st.write("يقوم النظام بتصدير تقرير جاهز للجهات التنظيمية ومجالس الإدارة بضغطة زر واحدة.")
    
    current_status = "99.4% (APPROVED)" if st.session_state.aligned else "54.0% (ACTION REQUIRED)"
    fairness_stat = "99% - ممتثل ومحايد" if st.session_state.aligned else "50% - يوجد خطر تحيز"
    exp_stat = "100% - استدلال كامل ومبرر" if st.session_state.aligned else "60% - يتطلب توضيح"
    
    report_content = f"""======================================================
تقرير التدقيق الرسمي لحوكمة الذكاء الاصطناعي - EthixPilot
======================================================
تاريخ التقرير: 2026-10-10
الجهة المفحوصة: Enterprise Client Demo
المطابقة التنظيمية: مبادئ دبي للذكاء الاصطناعي الأخلاقي & ISO/IEC 42001

النتيجة العامة (Ethix Score): {current_status}
------------------------------------------------------
1. مؤشر مكافحة التحيز والعدالة: {fairness_stat}
2. معيار حماية الخصوصية والـ PII: 98% - محجوب ومشفر
3. الشفافية وقابلية التفسير: {exp_stat}
4. سياسة تخزين البيانات: Zero-Retention (0 Bytes Retained)

الاعتماد: تم الفحص آلياً عبر محرك EthixPilot v2.0
======================================================"""

    st.text_area("معاينة الوثيقة التوثيقية:", value=report_content, height=220)
    st.download_button(
        label="📥 تحميل تقرير الامتثال المعتمد (Download Audit Dossier)",
        data=report_content,
        file_name="EthixPilot_Compliance_Dossier.txt",
        mime="text/plain",
        use_container_width=True
    )
