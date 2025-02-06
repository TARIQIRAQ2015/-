import streamlit as st
import pandas as pd
from PIL import Image
import base64

# إخفاء عناصر Streamlit الافتراضية
st.set_page_config(
    page_title="شبكة المساعد",
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
        color: #e2e8f0;
    }
    
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #00f5a0 0%, #00d9f5 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 245, 160, 0.2);
    }
    
    .app-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #1a1a2e 0%, #16213e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        padding: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sponsor {
        margin-top: 1rem;
        font-size: 1.2rem;
        color: #1a1a2e;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #00f5a0 0%, #00d9f5 100%);
        color: #1a1a2e;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 245, 160, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 245, 160, 0.3);
    }
    
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: none;
        color: white;
        border-radius: 10px;
        padding: 0.8rem 1rem;
        font-size: 1.1rem;
        text-align: center;
    }
    
    .stNumberInput>div>div>input:focus {
        box-shadow: 0 0 0 2px rgba(0, 245, 160, 0.3);
        border: none;
    }
    
    h1, h2, h3 {
        color: #00f5a0;
        text-align: center;
        margin: 2rem 0;
        font-weight: bold;
    }
    
    .results-table {
        width: 100%;
        margin: 2rem 0;
        border-collapse: separate;
        border-spacing: 0 8px;
    }
    
    .results-table th {
        background: rgba(0, 245, 160, 0.1);
        color: #00f5a0;
        font-weight: bold;
        padding: 1rem;
        text-align: center;
    }
    
    .results-table td {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        text-align: center;
    }
    
    .conclusion {
        background: rgba(0, 245, 160, 0.05);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
    }
    
    .grades-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .grade-input {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 12px;
    }
    
    .grade-label {
        color: #00f5a0;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# إضافة الشعار والعنوان
st.markdown("""
    <div class="app-header">
        <img src="https://raw.githubusercontent.com/yourusername/yourrepo/main/logo.png" width="150">
        <h1 class="app-title">نظام المستقبل للحسابات الذكية</h1>
        <div class="sponsor">برعاية شبكة المساعد @SadsHelp</div>
    </div>
""", unsafe_allow_html=True)

# بيانات الطالب
st.markdown("### معلومات الطالب")
student_name = st.text_input("اسم الطالب")

# تعريف المواد
subjects = {
    "الإسلامية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "اللغة العربية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "اللغة الإنجليزية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الرياضيات": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الفيزياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الكيمياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0},
    "الأحياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0}
}

# إدخال الدرجات
st.markdown("### إدخال الدرجات")
for subject in subjects:
    st.markdown(f'<div class="grades-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="grade-label">الفصل الأول</div>', unsafe_allow_html=True)
        subjects[subject]["الفصل الأول"] = st.number_input(
            "",
            value=int(subjects[subject]["الفصل الأول"]),
            min_value=0,
            max_value=100,
            key=f"first_{subject}"
        )
    
    with col2:
        st.markdown(f'<div class="grade-label">نصف السنة</div>', unsafe_allow_html=True)
        subjects[subject]["نصف السنة"] = st.number_input(
            "",
            value=int(subjects[subject]["نصف السنة"]),
            min_value=0,
            max_value=100,
            key=f"mid_{subject}"
        )
    
    with col3:
        st.markdown(f'<div class="grade-label">الفصل الثاني</div>', unsafe_allow_html=True)
        subjects[subject]["الفصل الثاني"] = st.number_input(
            "",
            value=int(subjects[subject]["الفصل الثاني"]),
            min_value=0,
            max_value=100,
            key=f"second_{subject}"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

def calculate_minimum_required(first_term, mid_term):
    required_total = 50 * 3
    current_total = first_term + mid_term
    minimum_required = required_total - current_total
    return minimum_required

if st.button("تحليل النتائج", key="calculate_btn"):
    if not student_name:
        st.error("الرجاء إدخال اسم الطالب")
    else:
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
        
        st.markdown("### نتائج التحليل")
        df = pd.DataFrame(results)
        st.table(df)
        
        st.markdown('<div class="conclusion">', unsafe_allow_html=True)
        st.markdown("### الاستنتاج")
        
        if passing_subjects:
            st.write(f"المواد التي ضمنت النجاح هي: {', '.join(passing_subjects)}، حتى لو حصلت على 0 في الفصل الثاني.")
        
        if possible_subjects:
            st.write(f"المواد التالية لديك فرصة للنجاح فيها إذا حصلت على الدرجة المطلوبة في الفصل الثاني: {', '.join(possible_subjects)}")
        
        if impossible_subjects:
            st.write(f"المواد التالية لا يمكن النجاح فيها حتى لو حصلت على 100 في الفصل الثاني: {', '.join(impossible_subjects)}")
        
        if possible_subjects:
            st.write("بالتالي، تحتاج إلى التركيز بشكل كبير على المواد التي لديك فرصة للنجاح فيها. 🚀")
        
        st.markdown('</div>', unsafe_allow_html=True)
