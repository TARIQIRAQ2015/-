import streamlit as st
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
    
    .results-table {
        width: 100%;
        margin: 2rem 0;
        border-collapse: collapse;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        overflow: hidden;
    }
    
    .results-table th, .results-table td {
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .results-table th {
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        font-weight: bold;
    }
    
    .results-table tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.02);
    }
    
    .conclusion {
        background: rgba(56, 189, 248, 0.05);
        padding: 2rem;
        border-radius: 12px;
        margin-top: 2rem;
        border: 1px solid rgba(56, 189, 248, 0.1);
    }
    
    .conclusion h3 {
        color: #38bdf8;
        margin-bottom: 1rem;
    }
    
    .conclusion ul {
        list-style-type: none;
        padding: 0;
    }
    
    .conclusion li {
        margin-bottom: 0.8rem;
        padding-right: 1.5rem;
        position: relative;
    }
    
    .conclusion li:before {
        content: "•";
        color: #38bdf8;
        position: absolute;
        right: 0;
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
col1, col2 = st.columns(2)

for subject in subjects:
    with col1:
        subjects[subject]["الفصل الأول"] = st.number_input(
            f"الفصل الأول - {subject}",
            value=float(subjects[subject]["الفصل الأول"]),
            min_value=0.0,
            max_value=100.0,
            step=1.0
        )
    with col2:
        subjects[subject]["نصف السنة"] = st.number_input(
            f"نصف السنة - {subject}",
            value=float(subjects[subject]["نصف السنة"]),
            min_value=0.0,
            max_value=100.0,
            step=1.0
        )

def calculate_minimum_required(first_term, mid_term):
    # الدرجة المطلوبة = (50 × 3) - (الفصل الأول + نصف السنة)
    required_total = 50 * 3
    current_total = first_term + mid_term
    minimum_required = required_total - current_total
    return minimum_required

if st.button("تحليل النتائج", key="calculate_btn"):
    if not student_name:
        st.error("الرجاء إدخال اسم الطالب")
    else:
        # إنشاء جدول النتائج
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
                "الحد الأدنى المطلوب في الفصل الثاني": f"{minimum_required:.0f} {status}"
            })
        
        # عرض النتائج في جدول
        st.markdown("### نتائج التحليل")
        df = pd.DataFrame(results)
        st.table(df)
        
        # عرض الاستنتاج
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
