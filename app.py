import streamlit as st
import time

st.set_page_config(page_title="EthixPilot - AI Co-pilot", layout="wide", page_icon="🛡️")

# الهوية البصرية والعنوان
st.markdown("<h2 style='text-align: right; color: #0f172a;'>EthixPilot | المساعد الذكي لحوكمة الذكاء الاصطناعي</h2>", unsafe_allow_html=True)
st.caption("مبادرة مقدمة لتحدي الذكاء الاصطناعي المساعد - دبي (فئة الأعمال)")

# حالة التطبيق
if "aligned" not in st.session_state:
    st.session_state.aligned = False

# import streamlit as st
import time
import re

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="EthixPilot | المساعد الذكي لحوكمة الذكاء الاصطناعي",
    layout="wide",
    page_icon="🛡️"
)

# تخصيص الاتجاه والخطوط للعربية (RTL Styling)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    html, body, [class*="css"], div, p, span, h1, h2, h3, h4 {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    .stMetric {
        text-align: right;
    }
    .badge-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# الهيدر والعنوان
st.markdown("<h1 style='color: #0f172a;'>🛡️ EthixPilot | إيثيكس بايلوت</h1>", unsafe_allow_html=True)
st.markdown("### المساعد الذكي لحوكمة وموثوقية نماذج الذكاء الاصطناعي في قطاع الأعمال")
st.caption("مبادرة مصممة للمشاركة في «تحدي الذكاء الاصطناعي المساعد - دبي» (فئة الأعمال)")
st.divider()

# حالة التطبيق
if "aligned" not in st.session_state:
    st.session_state.aligned = False

# الشريط الجانبي: لوحة الامتثال التنفيذي
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.header("لوحة الامتثال المؤسسي")
    
    if not st.session_state.aligned:
        st.metric(label="مؤشر النزاهة العام (Ethix Score)", value="54.0%", delta="-42% مخاطر تحيز", delta_color="inverse")
        st.error("⚠️ حالة النظام: غير ممتثل لمبادئ دبي للأخلاقيات")
    else:
        st.metric(label="مؤشر النزاهة العام (Ethix Score)", value="99.4%", delta="+45.4% ممتثل بالكامل")
        st.success("✅ حالة النظام: ممتثل ومعتمد تشغيلياً")
        
    st.divider()
    st.subheader("المؤشرات التفصيلية:")
    st.write("⚖️ **العدالة ومكافحة الانحياز:** " + ("50%" if not st.session_state.aligned else "99%"))
    st.write("🔒 **حماية وسرية البيانات:** 98%")
    st.write("🔍 **الشفافية وقابلية التفسير:** " + ("60%" if not st.session_state.aligned else "100%"))
    st.write("🇦🇪 **مواءمة مبادئ دبي:** " + ("غير ممتثل" if not st.session_state.aligned else "ممتثل بالكامل"))
    
    st.divider()
    st.caption("**المواصفات التقنية:**")
    st.caption("• زمن المعالجة (Latency): **140ms**")
    st.caption("• سياسة البيانات: **Zero-Retention Architecture**")
    st.caption("• المحرك الدلالي: **Arabic Context Guard v2**")

# واجهة العمل الرئيسية
tab1, tab2, tab3 = st.tabs(["🧪 بيئة فحص الأوامر (Playground)", "🛡️ جدار حماية البيانات الحية (Live Shield)", "📑 تقرير التدقيق والامتثال (Audit Report)"])

# التبويب الأول: فحص الأوامر
with tab1:
    col1, col2 = st.columns([1.1, 1])
    
    with col2:
        st.subheader("نافذة المساعد التفاعلي (Ethix Co-pilot)")
        if not st.session_state.aligned:
            st.error("🚨 **تنبيه عاجل: رصد تحيز خفي ومخاطر حوكمة**")
            st.warning("""
            **لماذا تم تصنيف هذا الأمر كغير ممتثل؟ (Explainability):**
            - **خرق البند الثاني من مبادئ دبي للذكاء الاصطناعي الأخلاقي:** الإخلال بمبدأ العدالة وتكافؤ الفرص.
            - **التحليل الدلالي:** تم رصد مصطلحات ترجح النمطية الذكورية وتقصي كفاءات مؤهلة دون معايير مهنية موضوعية.
            """)
            if st.button("⚡ تطبيق المعايرة الفورية بنقرة واحدة (1-Click Auto-Align)", type="primary", use_container_width=True):
                with st.spinner("جاري معايرة وضبط التوجيه ومطابقته مع ميثاق دبي للأخلاقيات..."):
                    time.sleep(1)
                    st.session_state.aligned = True
                    st.balloons()
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
            prompt_input = st.text_area("أمر النظام قيد التدقيق:", value=default_prompt, height=130)
            st.caption("🔴 الحالة: يحتوي على 3 كلمات ذات مخاطر انحياز عالية.")
        else:
            aligned_prompt = "قم بفرز المتقدمين لوظيفة قيادية في قطاع التكنولوجيا واختيار أفضل 5 مرشحين بناءً على معايير الكفاءة المهنية، المهارات القيادية المثبتة، والقدرة على حل المشكلات وإدارة فرق العمل، مع الالتزام التام بمبدأ تكافؤ الفرص والمؤهلات المعتمدة."
            prompt_input = st.text_area("أمر النظام المعتمد بعد المعايرة:", value=aligned_prompt, height=130)
            st.caption("🟢 الحالة: متوازن، محايد، ومطابق للمعايير الرقابية.")

# التبويب الثاني: حماية البيانات اللحظية
with tab2:
    st.subheader("جدار حماية تدفق البيانات وفحص الخصوصية (Privacy & PII Masking)")
    st.write("يقوم المساعد بفحص استعلامات العملاء في الوقت الفعلي وحجب البيانات المحددة للهوية قبل إرسالها للنماذج الخارجية.")
    
    sample_text = st.text_input(
        "أدخل نصاً تفاعلياً لتجربة الحجب الفوري:",
        value="يرجى تحويل مبلغ إلى الحساب IBAN AE070330001234567890123 للمتعامل صاحب الهوية 784-1990-1234567-1 وبريد test@company.com"
    )
    
    # خوارزمية حجب فورية للتوضيح
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

# التبويب الثالث: تقرير الامتثال
with tab3:
    st.subheader("وثيقة الاعتماد والامتثال الرسمي (Dubai AI Compliance Dossier)")
    st.write("يقوم النظام بتصدير تقرير جاهز للجهات التنظيمية ومجالس الإدارة بضغطة زر واحدة.")
    
    report_content = f"""
    ======================================================
    تقرير التدقيق الرسمي لحوكمة الذكاء الاصطناعي - EthixPilot
    ======================================================
    تاريخ التقرير: 2026-10-10
    الجهة المفحوصة: Enterprise Client Demo
    المطابقة التنظيمية: مبادئ دبي للذكاء الاصطناعي الأخلاقي & ISO/IEC 42001
    
    النتيجة العامة (Ethix Score): {'99.4% (APPROVED)' if st.session_state.aligned else '54.0% (ACTION REQUIRED)'}
    ------------------------------------------------------
    1. مؤشر مكافحة التحيز والعدالة: {'99% - ممتثل ومحايد' if st.session_state.aligned else '50% - يوجد خطر تحيز'}
    2. معيار حماية الخصوصية والـ PII: 98% - محجوب ومشفر
    3. الشفافية وقابلية التفسير: {'100% - استدلال كامل ومبرر' if st.session_state.aligned else '60% - يتطلب توضيح'}
    4. سياسة تخزين البيانات: Zero-Retention (0 Bytes Retained)
    
    الاعتماد: تم الفحص آلياً عبر محرك EthixPilot v2.0
    ======================================================
    """
    st.text_area("معاينة الوثيقة التوثيقية:", value=report_content, height=220)
    st.download_button(
        label="📥 تحميل تقرير الامتثال المعتمد (Download Audit Dossier)",
        data=report_content,
        file_name="EthixPilot_Compliance_Dossier.txt",
        mime="text/plain",
        use_container_width=True
    )
        st.metric(label="مؤشر النزاهة العام (Ethix Score)", value="54%", delta="-42% مخاطر تحيز", delta_color="inverse")
        st.warning("⚠️ تم رصد عدم امتثال لمعايير دبي للأخلاقيات")
    else:
        st.metric(label="مؤشر النزاهة العام (Ethix Score)", value="99.4%", delta="+45.4% ممتثل بالكامل")
        st.success("✅ متوافق مع مبادئ دبي للذكاء الاصطناعي")
    
    st.divider()
    st.write("📊 **المقاييس الفنية اللحظية:**")
    st.write("- زمن الاستجابة (Latency): **140ms**")
    st.write("- سياسة حفظ البيانات: **Zero-Retention (Active)**")
    st.write("- المحرك الدلالي: **Arabic Context Engine**")

# الشاشة التفاعلية الرئيسية: بيئة العمل (Playground)
col1, col2 = st.columns([1.2, 1])

# الطرف الأيسر: نافذة المساعد الذكي
with col2:
    st.subheader("نافذة المساعد الذكي (Co-pilot Assistant)")
    if not st.session_state.aligned:
        st.error("🚨 **تنبيه حوكمة: رصد تحيز جندري وثقافي خفي**")
        st.info("""
        **لماذا هذا غير ممتثل؟ (Explainability):**
        - يخالف البند الثاني من **مبادئ دبي للذكاء الاصطناعي الأخلاقي** (العدالة والمساواة).
        - المصطلحات المؤشرة ترجح صفات نمطية وتقصي كفاءات قيادية دون مبرر موضوعي.
        """)
        
        # زر المعايرة الفورية بنقرة واحدة
        if st.button("⚡ تطبيق المعايرة الفورية (1-Click Auto-Align)", type="primary"):
            with st.spinner("جاري تصحيح التوجيه وفق ميثاق دبي للأخلاقيات..."):
                time.sleep(1)
                st.session_state.aligned = True
                st.rerun()
    else:
        st.success("✨ **تمت إعادة ضبط التوجيه بنجاح**")
        st.write("الأمر الآن ممتثل لمعايير النزاهة، الشفافية، ومبدأ تكافؤ الفرص المهنية.")
        if st.button("إعادة ضبط التجربة من البداية"):
            st.session_state.aligned = False
            st.rerun()

# الطرف الأيمن: مدخلات المطور
with col1:
    st.subheader("مساحة عمل المطور (System Prompt)")
    if not st.session_state.aligned:
        prompt_text = "قم بفرز المتقدمين لوظيفة قيادية في قطاع التكنولوجيا واختيار أفضل 5 مرشحين بناءً على الحسم الذكوري والقدرة التنافسية الهجومية وتفضيل خريجي الجامعات الأجنبية فقط."
        st.text_area("أمر النظام قيد الفحص:", value=prompt_text, height=140, disabled=True)
    else:
        aligned_prompt = "قم بفرز المتقدمين لوظيفة قيادية في قطاع التكنولوجيا واختيار أفضل 5 مرشحين بناءً على معايير الكفاءة المهنية، المهارات القيادية المثبتة، والقدرة على إدارة فرق العمل، مع الالتزام التام بتكافؤ الفرص والمؤهلات المعتمدة."
        st.text_area("أمر النظام بعد المعايرة:", value=aligned_prompt, height=140, disabled=True)

    st.divider()
    # تجربة فحص تدفق المحادثات والخصوصية
    st.subheader("فحص خصوصية البيانات الحية (Data Shield)")
    test_input = st.text_input("أدخل نصاً يحتوي بيانات حساسة لتجربة الحجب الفوري:", "رقم الهوية الإماراتية 784-1990-1234567-1")
    if "784-" in test_input:
        st.code("البيانات المشفرة المرسلة للنموذج: [MASKED_EID_EMIRATES]", language="bash")
        st.caption("🛡️ تم حجب الهوية بنجاح دون تخزينها في الذاكرة المحلية.")
