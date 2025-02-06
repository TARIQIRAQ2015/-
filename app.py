import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(
    page_title="المساعد لحساب الوزاري",
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

    @keyframes gradientFlow {
        0% {
            background-position: 0% 50%;
            background-color: #00092a;
        }
        10% {
            background-color: #000829;
        }
        20% {
            background-color: #010a2b;
        }
        30% {
            background-color: #000b2b;
        }
        40% {
            background-color: #00082c;
        }
        50% {
            background-position: 100% 50%;
            background-color: #02082a;
        }
        60% {
            background-color: #010a29;
        }
        70% {
            background-color: #000928;
        }
        80% {
            background-color: #01092d;
        }
        90% {
            background-color: #020b2c;
        }
        100% {
            background-position: 0% 50%;
            background-color: #00092a;
        }
    }

    @keyframes shine {
        0% {
            background-position: -100% 50%;
            opacity: 0.3;
        }
        100% {
            background-position: 200% 50%;
            opacity: 0.6;
        }
    }

    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }

    body {
        animation: gradientFlow 15s ease infinite;
        background-size: 200% 200%;
    }

    .language-selector {
        text-align: center;
        margin-bottom: 1rem;
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
    
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        background: rgba(0, 9, 42, 0.8);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 255, 157, 0.2);
        position: relative;
        overflow: hidden;
        animation: float 6s ease-in-out infinite;
        border: 1px solid rgba(0, 255, 157, 0.1);
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
            rgba(0, 255, 157, 0.1) 40%,
            rgba(0, 255, 157, 0.1) 60%,
            transparent 80%
        );
        animation: shine 4s infinite linear;
        pointer-events: none;
    }
    
    .app-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #fff;
        margin: 0;
        padding: 0;
        letter-spacing: 2px;
        position: relative;
        text-shadow: 0 0 10px rgba(0, 255, 157, 0.5),
                     0 0 20px rgba(0, 255, 157, 0.3),
                     0 0 30px rgba(0, 255, 157, 0.2);
    }
    
    .app-subtitle {
        font-size: 1.5rem;
        color: #00ff9d;
        margin-top: 1rem;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
    }
    
    .subject-name {
        color: #00ff9d;
        font-weight: bold;
        font-size: 1.3rem;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 0 0 10px rgba(0, 255, 157, 0.5);
        background: rgba(0, 9, 42, 0.9);
        padding: 1rem;
        border-radius: 10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
        border: 1px solid rgba(0, 255, 157, 0.1);
        animation: float 6s ease-in-out infinite;
    }

    .grade-label {
        color: #fff;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: center;
        font-size: 1.2rem;
        text-shadow: 0 0 5px rgba(0, 255, 157, 0.5);
    }

    .stNumberInput>div>div>input {
        background: rgba(0, 9, 42, 0.9);
        border: 1px solid rgba(0, 255, 157, 0.2);
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 1.1rem;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
    }

    .stNumberInput>div>div>input:focus {
        box-shadow: 0 0 0 2px rgba(0, 255, 157, 0.3);
        border-color: rgba(0, 255, 157, 0.5);
    }

    .results-table {
        background: rgba(0, 9, 42, 0.9);
        border-radius: 15px;
        padding: 1rem;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
        border: 1px solid rgba(0, 255, 157, 0.1);
        animation: float 6s ease-in-out infinite;
    }

    .conclusion {
        background: rgba(0, 9, 42, 0.9);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        color: #fff;
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
        border: 1px solid rgba(0, 255, 157, 0.1);
        animation: float 6s ease-in-out infinite;
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
    }

    .social-links a {
        color: #00ff9d;
        text-decoration: none;
        padding: 0.5rem 1rem;
        background: rgba(0, 9, 42, 0.8);
        border-radius: 8px;
        border: 1px solid rgba(0, 255, 157, 0.2);
        transition: all 0.3s ease;
    }

    .social-links a:hover {
        background: rgba(0, 255, 157, 0.1);
        transform: translateY(-2px);
    }

    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: rgba(0, 9, 42, 0.9);
        border-radius: 12px;
        color: #fff;
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
        border: 1px solid rgba(0, 255, 157, 0.1);
        animation: float 6s ease-in-out infinite;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# إضافة محدد اللغة
lang = st.radio("", ["العربية", "English"], horizontal=True, label_visibility="collapsed")

# إضافة العنوان
if lang == "العربية":
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">المساعد لحساب الوزاري</h1>
            <div class="app-subtitle">احسب دخولك للوزاري بدقة وسهولة</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="app-header">
            <h1 class="app-title">Ministry Calculator</h1>
            <div class="app-subtitle">Calculate your grades accurately and easily</div>
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
current_lang = lang
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
        with cols[0]:
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
        
        with cols[2]:
            st.markdown(f'<div class="grade-label">Second Term</div>', unsafe_allow_html=True)
            current_subjects[subject]["Second Term"] = st.number_input(
                "",
                value=int(current_subjects[subject]["Second Term"]),
                min_value=0,
                max_value=100,
                key=f"second_{subject}"
            )

# دالة حساب الحد الأدنى المطلوب
def calculate_minimum_required(first_term, mid_term):
    required_total = 50 * 3
    current_total = first_term + mid_term
    minimum_required = required_total - current_total
    return minimum_required

# عرض النتائج
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
        status = "✅ (نجاح مضمون)"
        passing_subjects.append(subject)
    elif minimum_required > 100:
        status = "❌ (لا يمكن النجاح)"
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

st.markdown('<div class="results-table">', unsafe_allow_html=True)
df = pd.DataFrame(results)
st.table(df)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="conclusion">', unsafe_allow_html=True)
if current_lang == "العربية":
    if passing_subjects:
        st.write(f"المواد التي ضمنت النجاح هي: {', '.join(passing_subjects)}، حتى لو حصلت على 0 في الفصل الثاني.")
    
    if possible_subjects:
        st.write(f"المواد التالية لديك فرصة للنجاح فيها إذا حصلت على الدرجة المطلوبة في الفصل الثاني: {', '.join(possible_subjects)}")
    
    if impossible_subjects:
        st.write(f"المواد التالية لا يمكن النجاح فيها حتى لو حصلت على 100 في الفصل الثاني: {', '.join(impossible_subjects)}")
    
    if possible_subjects:
        st.write("بالتالي، تحتاج إلى التركيز بشكل كبير على المواد التي لديك فرصة للنجاح فيها. 🚀")
else:
    if passing_subjects:
        st.write(f"Subjects that guaranteed success: {', '.join(passing_subjects)}, even if you get 0 in the second term.")
    
    if possible_subjects:
        st.write(f"Subjects with a chance of success if you get the required grade in the second term: {', '.join(possible_subjects)}")
    
    if impossible_subjects:
        st.write(f"Subjects that cannot be passed even if you get 100 in the second term: {', '.join(impossible_subjects)}")
    
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
