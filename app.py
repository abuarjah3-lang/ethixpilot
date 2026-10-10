import streamlit as st
import time

st.set_page_config(page_title="EthixPilot - AI Co-pilot", layout="wide", page_icon="🛡️")

# الهوية البصرية والعنوان
st.markdown("<h2 style='text-align: right; color: #0f172a;'>EthixPilot | المساعد الذكي لحوكمة الذكاء الاصطناعي</h2>", unsafe_allow_html=True)
st.caption("مبادرة مقدمة لتحدي الذكاء الاصطناعي المساعد - دبي (فئة الأعمال)")

# حالة التطبيق
if "aligned" not in st.session_state:
    st.session_state.aligned = False

# الشريط الجانبي: مؤشرات الأداء والامتثال
with st.sidebar:
    st.header("لوحة الامتثال المؤسسي")
    if not st.session_state.aligned:
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