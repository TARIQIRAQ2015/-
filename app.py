import streamlit as st
import pandas as pd
from PIL import Image
import base64

# إضافة أيقونة افتراضية
DEFAULT_ICON = "📊"

# تعريف أيقونة افتراضية في حالة عدم وجود الملف
try:
    icon = Image.open('logo.png')
    with open('logo.png', 'rb') as f:
        icon_base64 = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    icon = None
    icon_base64 = ""

st.set_page_config(
    page_title="المساعد لحساب الوزاري",
    page_icon=DEFAULT_ICON,  # استخدام الأيقونة الافتراضية دائماً
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إضافة الشعار والعنوان بدون صورة
st.markdown("""
    <div class="app-header">
        <div style="font-size: 64px; 
                    color: #00ff9d;
                    margin: 20px;
                    text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);">
            📚
        </div>
        <h1 class="app-title">المساعد لحساب الوزاري</h1>
        <div class="app-subtitle">احسب دخولك للوزاري بدقة وسهولة</div>
    </div>
""", unsafe_allow_html=True)

# اختيار اللغة
language = st.selectbox("", ["العربية", "English"], index=0)

# تحديد اتجاه النص بناءً على اللغة
direction = "rtl" if language == "العربية" else "ltr"
st.markdown(f"<style>body {{ direction: {direction}; }}</style>", unsafe_allow_html=True)

# تعريف النصوص حسب اللغة
texts = {
    "العربية": {
        "first_term": "الفصل الأول",
        "mid_term": "نصف السنة",
        "second_term": "الفصل الثاني",
        "analyze": "تحليل النتائج",
        "subjects": {
            "الإسلامية": "الإسلامية",
            "اللغة العربية": "اللغة العربية",
            "اللغة الإنجليزية": "اللغة الإنجليزية",
            "اللغة الفرنسية": "اللغة الفرنسية",
            "الرياضيات": "الرياضيات",
            "الفيزياء": "الفيزياء",
            "الكيمياء": "الكيمياء",
            "الأحياء": "الأحياء"
        }
    },
    "English": {
        "first_term": "First Term",
        "mid_term": "Mid Term",
        "second_term": "Second Term",
        "analyze": "Analyze Results",
        "subjects": {
            "الإسلامية": "Islamic Studies",
            "اللغة العربية": "Arabic",
            "اللغة الإنجليزية": "English",
            "اللغة الفرنسية": "French",
            "الرياضيات": "Mathematics",
            "الفيزياء": "Physics",
            "الكيمياء": "Chemistry",
            "الأحياء": "Biology"
        }
    }
}

current_texts = texts[language]

# تعريف المواد
subjects = {
    "الإسلامية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "اللغة العربية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "اللغة الإنجليزية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "اللغة الفرنسية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الرياضيات": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الفيزياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الكيمياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الأحياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0}
}

# إدخال الدرجات
for subject in subjects:
    st.markdown(f'<div class="subject-name">{current_texts["subjects"][subject]}</div>', unsafe_allow_html=True)
    cols = st.columns(3, gap="large")
    
    with cols[0]:
        st.markdown(f'<div class="grade-label">{current_texts["first_term"]}</div>', unsafe_allow_html=True)
        subjects[subject]["الفصل الأول"] = st.number_input(
            "",
            value=int(subjects[subject]["الفصل الأول"]),
            min_value=0,
            max_value=100,
            key=f"first_{subject}"
        )
    
    with cols[1]:
        st.markdown(f'<div class="grade-label">{current_texts["mid_term"]}</div>', unsafe_allow_html=True)
        subjects[subject]["نصف السنة"] = st.number_input(
            "",
            value=int(subjects[subject]["نصف السنة"]),
            min_value=0,
            max_value=100,
            key=f"mid_{subject}"
        )
    
    with cols[2]:
        st.markdown(f'<div class="grade-label">{current_texts["second_term"]}</div>', unsafe_allow_html=True)
        subjects[subject]["الفصل الثاني"] = st.number_input(
            "",
            value=int(subjects[subject]["الفصل الثاني"]),
            min_value=0,
            max_value=100,
            key=f"second_{subject}"
        )

def calculate_minimum_required(first_term, mid_term):
    required_total = 50 * 3
    current_total = first_term + mid_term
    minimum_required = required_total - current_total
    return minimum_required

if st.button(current_texts["analyze"], key="calculate_btn"):
    results = []
    passing_subjects = []
    possible_subjects = []
    impossible_subjects = []
    
    for subject, scores in subjects.items():
        minimum_required = calculate_minimum_required(
            scores["الفصل الأول"],
            scores["نصف السنة"]
        )
        
        status = ""
        if minimum_required <= 0:
            status = "✅ (ناجح بغض النظر عن الفصل الثاني)"
            passing_subjects.append(subject)
        elif minimum_required > 100:
            status = "❌ (يستحيل النجاح)"
            impossible_subjects.append(subject)
        else:
            status = f"❌ (يجب الحصول على {minimum_required:.0f} أو أكثر للنجاح)"
            possible_subjects.append(subject)
        
        results.append({
            "المادة": subject,
            "الفصل الأول": scores["الفصل الأول"],
            "نصف السنة": scores["نصف السنة"],
            "الفصل الثاني": scores["الفصل الثاني"],
            "الحد الأدنى المطلوب في الفصل الثاني": f"{minimum_required:.0f} {status}"
        })
    
    st.markdown('<div class="results-table">', unsafe_allow_html=True)
    df = pd.DataFrame(results)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="conclusion">', unsafe_allow_html=True)
    if passing_subjects:
        st.write(f"المواد التي ضمنت النجاح هي: {', '.join(passing_subjects)}، حتى لو حصلت على 0 في الفصل الثاني.")
    
    if possible_subjects:
        st.write(f"المواد التالية لديك فرصة للنجاح فيها إذا حصلت على الدرجة المطلوبة في الفصل الثاني: {', '.join(possible_subjects)}")
    
    if impossible_subjects:
        st.write(f"المواد التالية لا يمكن النجاح فيها حتى لو حصلت على 100 في الفصل الثاني: {', '.join(impossible_subjects)}")
    
    if possible_subjects:
        st.write("بالتالي، تحتاج إلى التركيز بشكل كبير على المواد التي لديك فرصة للنجاح فيها. 🚀")
    st.markdown('</div>', unsafe_allow_html=True)

# إضافة معلومات التواصل وحقوق النشر
st.markdown("""
    <div class="footer">
        <div class="social-links">
            <a href="https://t.me/SadsHelp" target="_blank">شبكة المساعد التعليمية 📖</a>
            <a href="https://t.me/+mg19Snwv14U4NWZi" target="_blank">كروب طلاب السادس الاعدادي 📖</a>
        </div>
        <div class="copyright">
            By Tariq Al-Yaseen © 2025-2026
        </div>
    </div>
""", unsafe_allow_html=True)
