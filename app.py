import streamlit as st
import pandas as pd
from PIL import Image
import base64

# تحميل وتحويل الأيقونة
icon = Image.open('logo.png')
st.set_page_config(
    page_title="المساعد لحساب الوزاري",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إخفاء عناصر Streamlit الافتراضية
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    .css-eh5xgm {visibility: hidden;}
    .css-1dp5vir {visibility: hidden;}
    .css-1wrcr25 {display: none;}
    .css-6qob1r {display: none;}
    .css-zt5igj {display: none;}
    .stDeployButton {display:none;}
    div[data-testid="stDecoration"] {display:none;}
    div[data-testid="stMarkdownContainer"] > p {margin: 0;}
    
    /* ... (باقي الأنماط السابقة) ... */
    
    .language-selector {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .language-btn {
        background: rgba(0, 9, 42, 0.8);
        color: #fff;
        padding: 0.5rem 1.5rem;
        border: 1px solid rgba(0, 255, 157, 0.2);
        border-radius: 8px;
        cursor: pointer;
        margin: 0 0.5rem;
        transition: all 0.3s ease;
    }
    
    .language-btn:hover {
        background: rgba(0, 255, 157, 0.2);
    }
    
    .language-btn.active {
        background: rgba(0, 255, 157, 0.2);
        border-color: rgba(0, 255, 157, 0.5);
    }
    
    .social-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
    }
    
    .social-links a {
        color: #00ff9d;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        background: rgba(0, 9, 42, 0.5);
    }
    
    .social-links a:hover {
        background: rgba(0, 255, 157, 0.1);
        transform: translateY(-2px);
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# إضافة محدد اللغة
st.markdown("""
    <div class="language-selector">
        <button class="language-btn active" onclick="switchLanguage('ar')">العربية</button>
        <button class="language-btn" onclick="switchLanguage('en')">English</button>
    </div>
""", unsafe_allow_html=True)

# تعريف المواد باللغتين
subjects = {
    "العربية": {
        "الإسلامية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "اللغة العربية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "اللغة الإنجليزية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "اللغة الفرنسية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "الرياضيات": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "الفيزياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "الكيمياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
        "الأحياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0}
    },
    "English": {
        "Islamic Studies": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "Arabic": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "English": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "French": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "Mathematics": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "Physics": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "Chemistry": {"First Term": 0, "Mid-Term": 0, "Second Term": 0},
        "Biology": {"First Term": 0, "Mid-Term": 0, "Second Term": 0}
    }
}

# القيم الافتراضية
current_lang = "العربية"
current_subjects = subjects[current_lang]

# إدخال الدرجات
for subject in current_subjects:
    st.markdown(f'<div class="subject-name">{subject}</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    
    if current_lang == "العربية":
        # ترتيب من اليمين لليسار للغة العربية
        with cols[0]:
            st.markdown(f'<div class="grade-label">الفصل الأول</div>', unsafe_allow_html=True)
            current_subjects[subject]["الفصل الأول"] = st.number_input(
                "",
                value=int(current_subjects[subject]["الفصل الأول"]),
                min_value=0,
                max_value=100,
                key=f"first_{subject}"
            )
        
        with cols[1]:
            st.markdown(f'<div class="grade-label">نصف السنة</div>', unsafe_allow_html=True)
            current_subjects[subject]["نصف السنة"] = st.number_input(
                "",
                value=int(current_subjects[subject]["نصف السنة"]),
                min_value=0,
                max_value=100,
                key=f"mid_{subject}"
            )
        
        with cols[2]:
            st.markdown(f'<div class="grade-label">الفصل الثاني</div>', unsafe_allow_html=True)
            current_subjects[subject]["الفصل الثاني"] = st.number_input(
                "",
                value=int(current_subjects[subject]["الفصل الثاني"]),
                min_value=0,
                max_value=100,
                key=f"second_{subject}"
            )
    else:
        # ترتيب من اليسار لليمين للغة الإنجليزية
        with cols[2]:
            st.markdown(f'<div class="grade-label">First Term</div>', unsafe_allow_html=True)
            current_subjects[subject]["First Term"] = st.number_input(
                "",
                value=int(current_subjects[subject]["First Term"]),
                min_value=0,
                max_value=100,
                key=f"first_{subject}"
            )
        
        with cols[1]:
            st.markdown(f'<div class="grade-label">Mid-Term</div>', unsafe_allow_html=True)
            current_subjects[subject]["Mid-Term"] = st.number_input(
                "",
                value=int(current_subjects[subject]["Mid-Term"]),
                min_value=0,
                max_value=100,
                key=f"mid_{subject}"
            )
        
        with cols[0]:
            st.markdown(f'<div class="grade-label">Second Term</div>', unsafe_allow_html=True)
            current_subjects[subject]["Second Term"] = st.number_input(
                "",
                value=int(current_subjects[subject]["Second Term"]),
                min_value=0,
                max_value=100,
                key=f"second_{subject}"
            )

def calculate_minimum_required(first_term, mid_term):
    required_total = 50 * 3
    current_total = first_term + mid_term
    minimum_required = required_total - current_total
    return minimum_required

if st.button("تحليل النتائج", key="calculate_btn"):
    results = []
    passing_subjects = []
    possible_subjects = []
    impossible_subjects = []
    
    for subject, scores in current_subjects.items():
        if current_lang == "العربية":
            minimum_required = calculate_minimum_required(
                scores["الفصل الأول"],
                scores["نصف السنة"]
            )
        else:
            minimum_required = calculate_minimum_required(
                scores["First Term"],
                scores["Mid-Term"]
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
        
        if current_lang == "العربية":
            results.append({
                "المادة": subject,
                "الفصل الأول": scores["الفصل الأول"],
                "نصف السنة": scores["نصف السنة"],
                "الفصل الثاني": scores["الفصل الثاني"],
                "الحد الأدنى المطلوب في الفصل الثاني": f"{minimum_required:.0f} {status}"
            })
        else:
            results.append({
                "Subject": subject,
                "First Term": scores["First Term"],
                "Mid-Term": scores["Mid-Term"],
                "Second Term": scores["Second Term"],
                "Minimum Required in Second Term": f"{minimum_required:.0f} {status}"
            })
    
    if current_lang == "العربية":
        st.markdown('<div class="results-table">', unsafe_allow_html=True)
        df = pd.DataFrame(results)
        st.table(df)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="results-table">', unsafe_allow_html=True)
        df = pd.DataFrame(results)
        st.table(df)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if current_lang == "العربية":
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
    else:
        st.markdown('<div class="conclusion">', unsafe_allow_html=True)
        if passing_subjects:
            st.write(f"The subjects that guaranteed success are: {', '.join(passing_subjects)}, even if you got 0 in the second term.")
        
        if possible_subjects:
            st.write(f"The following subjects have a chance of success if you get the required grade in the second term: {', '.join(possible_subjects)}")
        
        if impossible_subjects:
            st.write(f"The following subjects cannot be passed even if you get 100 in the second term: {', '.join(impossible_subjects)}")
        
        if possible_subjects:
            st.write("Therefore, you need to focus heavily on the subjects that have a chance of success. 🚀")
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
