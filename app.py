import streamlit as st
import pandas as pd

# إخفاء عناصر Streamlit الافتراضية
st.set_page_config(
    page_title="المساعد لحساب الوزاري",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إخفاء جميع العناصر الافتراضية
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
    
    @keyframes gradientBG {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    @keyframes shine {
        0% {
            background-position: -100% 50%;
        }
        100% {
            background-position: 200% 50%;
        }
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# CSS للتصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
    }
    
    body {
        background: linear-gradient(45deg, 
            #00092a,
            #000829,
            #010a2b,
            #000b2b,
            #00082c,
            #02082a,
            #010a29,
            #000928,
            #01092d,
            #020b2c
        );
        background-size: 500% 500%;
        animation: gradientBG 20s ease infinite;
    }
    
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        background: rgba(0, 9, 42, 0.7);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 9, 42, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 20%,
            rgba(255, 255, 255, 0.1) 40%,
            rgba(255, 255, 255, 0.1) 60%,
            transparent 80%
        );
        animation: shine 3s infinite linear;
        pointer-events: none;
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(45deg, #fff 10%, #7fdbff 50%, #fff 90%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        text-shadow: 0 0 10px rgba(127, 219, 255, 0.5);
        letter-spacing: 2px;
        position: relative;
    }
    
    .app-subtitle {
        font-size: 1.5rem;
        color: #7fdbff;
        margin-top: 1rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(127, 219, 255, 0.5);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00092a, #020b2c);
        color: #fff;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 9, 42, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 9, 42, 0.7);
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 20%,
            rgba(127, 219, 255, 0.1) 40%,
            rgba(127, 219, 255, 0.1) 60%,
            transparent 80%
        );
        animation: shine 3s infinite linear;
        pointer-events: none;
    }
    
    .stNumberInput>div>div>input {
        background: rgba(0, 9, 42, 0.7);
        border: 1px solid rgba(127, 219, 255, 0.2);
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 1.1rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stNumberInput>div>div>input:focus {
        box-shadow: 0 0 0 2px rgba(127, 219, 255, 0.3);
        border-color: rgba(127, 219, 255, 0.5);
    }
    
    .subject-name {
        color: #7fdbff;
        font-weight: bold;
        font-size: 1.3rem;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 0 0 10px rgba(127, 219, 255, 0.5);
        background: rgba(0, 9, 42, 0.7);
        padding: 1rem;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
    }
    
    .subject-name::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 20%,
            rgba(127, 219, 255, 0.1) 40%,
            rgba(127, 219, 255, 0.1) 60%,
            transparent 80%
        );
        animation: shine 3s infinite linear;
        pointer-events: none;
    }
    
    .grade-label {
        color: #fff;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: center;
        font-size: 1.2rem;
        text-shadow: 0 0 5px rgba(127, 219, 255, 0.5);
    }
    
    .results-table {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 15px;
        padding: 1rem;
        margin: 2rem 0;
    }
    
    .conclusion {
        background: rgba(0, 0, 0, 0.7);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        color: #fff;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: rgba(0, 0, 0, 0.7);
        border-radius: 12px;
        color: #fff;
    }
    
    .social-links {
        margin-bottom: 1rem;
    }
    
    .social-links a {
        color: #00f5a0;
        text-decoration: none;
        margin: 0 1rem;
        font-weight: bold;
    }
    
    .social-links a:hover {
        color: #00d9f5;
    }
    
    .copyright {
        color: #fff;
        font-size: 1rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# إضافة الشعار والعنوان
st.markdown("""
    <div class="app-header">
        <h1 class="app-title">المساعد لحساب الوزاري</h1>
        <div class="app-subtitle">احسب دخولك للوزاري بدقة وسهولة</div>
    </div>
""", unsafe_allow_html=True)

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
    st.markdown(f'<div class="subject-name">{subject}</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f'<div class="grade-label">الفصل الأول</div>', unsafe_allow_html=True)
        subjects[subject]["الفصل الأول"] = st.number_input(
            "",
            value=int(subjects[subject]["الفصل الأول"]),
            min_value=0,
            max_value=100,
            key=f"first_{subject}"
        )
    
    with cols[1]:
        st.markdown(f'<div class="grade-label">نصف السنة</div>', unsafe_allow_html=True)
        subjects[subject]["نصف السنة"] = st.number_input(
            "",
            value=int(subjects[subject]["نصف السنة"]),
            min_value=0,
            max_value=100,
            key=f"mid_{subject}"
        )
    
    with cols[2]:
        st.markdown(f'<div class="grade-label">الفصل الثاني</div>', unsafe_allow_html=True)
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

if st.button("تحليل النتائج", key="calculate_btn"):
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
