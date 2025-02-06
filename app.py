import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# إخفاء عناصر Streamlit الافتراضية
st.set_page_config(
    page_title="المساعد الوزاري",
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
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #e2e8f0;
    }
    
    .app-title {
        text-align: center;
        color: #38bdf8;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
        background: linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4);
    }
    
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        text-align: center;
    }
    
    h1, h2, h3 {
        color: #38bdf8;
        text-align: center;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .grade-input {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .grade-input label {
        color: #38bdf8;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .result-box {
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .result-box h3 {
        color: #38bdf8;
        margin-bottom: 1rem;
    }
    
    .result-value {
        font-size: 2rem;
        font-weight: bold;
        color: #38bdf8;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# عنوان التطبيق
st.markdown('<h1 class="app-title">المساعد الوزاري</h1>', unsafe_allow_html=True)

# بيانات الطالب
st.markdown("### معلومات الطالب")
student_name = st.text_input("اسم الطالب")

# تعريف المواد وحدود النجاح
subjects = {
    "الإسلامية": {"الفصل الأول": 75, "نصف السنة": 77, "الفصل الثاني": 0, "حد النجاح": 50},
    "اللغة العربية": {"الفصل الأول": 30, "نصف السنة": 40, "الفصل الثاني": 0, "حد النجاح": 80},
    "اللغة الإنجليزية": {"الفصل الأول": 30, "نصف السنة": 48, "الفصل الثاني": 0, "حد النجاح": 72},
    "اللغة الفرنسية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50},
    "الرياضيات": {"الفصل الأول": 50, "نصف السنة": 32, "الفصل الثاني": 0, "حد النجاح": 68},
    "الفيزياء": {"الفصل الأول": 30, "نصف السنة": 8, "الفصل الثاني": 0, "حد النجاح": 112},
    "الكيمياء": {"الفصل الأول": 14, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 136},
    "الأحياء": {"الفصل الأول": 30, "نصف السنة": 14, "الفصل الثاني": 0, "حد النجاح": 106}
}

# إدخال درجات الفصل الثاني
st.markdown("### درجات الفصل الثاني")
for subject, scores in subjects.items():
    with st.container():
        st.markdown(f'<div class="grade-input">', unsafe_allow_html=True)
        scores["الفصل الثاني"] = st.number_input(
            f"📚 {subject}",
            value=float(scores["الفصل الثاني"]),
            min_value=0.0,
            max_value=100.0,
            step=1.0
        )
        st.markdown('</div>', unsafe_allow_html=True)

def calculate_possibility(current_score, required_score, max_possible):
    remaining_score_needed = required_score - current_score
    if remaining_score_needed <= max_possible:
        return True, remaining_score_needed
    return False, remaining_score_needed

# زر الحساب
if st.button("تحليل النتائج", key="calculate_btn"):
    if not student_name:
        st.error("الرجاء إدخال اسم الطالب")
    else:
        st.markdown("### نتائج التحليل")
        
        for subject, scores in subjects.items():
            current_score = (scores["الفصل الأول"] + scores["نصف السنة"]) / 2
            is_possible, needed_score = calculate_possibility(
                current_score,
                scores["حد النجاح"],
                100
            )
            
            with st.container():
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"#### {subject}")
                st.markdown(f'<div class="result-value">{current_score:.1f}</div>', unsafe_allow_html=True)
                
                if not is_possible:
                    st.error("❌ يستحيل النجاح في هذه المادة")
                elif needed_score <= 0:
                    st.success("✅ ناجح بغض النظر عن الفصل الثاني")
                else:
                    if needed_score > 90:
                        st.error(f"⚠️ تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني")
                    elif needed_score > 70:
                        st.warning(f"⚠️ تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني")
                    else:
                        st.info(f"ℹ️ تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني")
                
                st.markdown('</div>', unsafe_allow_html=True)
