import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import json

# تكوين الصفحة
st.set_page_config(
    page_title="نظام إدارة الدرجات المتطور",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS للتصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    * {
        font-family: 'Tajawal', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: bold;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .success-text {
        color: #10b981;
        font-weight: bold;
    }
    
    .failure-text {
        color: #ef4444;
        font-weight: bold;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3c72;
    }
    
    .css-1d391kg {
        padding: 3rem 1rem;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        padding: 0.5rem;
        background: white;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h1, h2, h3 {
        color: #1e3c72;
        text-align: right;
    }
    
    .english-mode h1, .english-mode h2, .english-mode h3 {
        text-align: left;
    }
    </style>
    """, unsafe_allow_html=True)

# اختيار اللغة
language = st.selectbox("🌐 Language / اللغة", ["العربية", "English"])

# تحديد النصوص حسب اللغة
texts = {
    "العربية": {
        "title": "🎓 النظام المتطور لإدارة وتحليل الدرجات",
        "student_name": "اسم الطالب",
        "academic_year": "السنة الدراسية",
        "calculate": "حساب النتيجة",
        "print": "طباعة النتيجة",
        "final_results": "النتيجة النهائية",
        "analysis": "التحليل",
        "advanced_analytics": "التحليلات المتقدمة",
        "recommendations": "التوصيات",
        "helping_marks": "إضافة 10 درجات مساعدة",
        "passed": "ناجح",
        "failed": "راسب"
    },
    "English": {
        "title": "🎓 Advanced Grade Management System",
        "student_name": "Student Name",
        "academic_year": "Academic Year",
        "calculate": "Calculate Results",
        "print": "Print Results",
        "final_results": "Final Results",
        "analysis": "Analysis",
        "advanced_analytics": "Advanced Analytics",
        "recommendations": "Recommendations",
        "helping_marks": "Add 10 Helping Marks",
        "passed": "Passed",
        "failed": "Failed"
    }
}

# تعيين اللغة الحالية
current_texts = texts[language]

# إضافة class للتحكم في المحاذاة
if language == "English":
    st.markdown('<div class="english-mode">', unsafe_allow_html=True)

# عنوان التطبيق
st.title(current_texts["title"])

# بيانات الطالب
col1, col2 = st.columns(2)
with col1:
    student_name = st.text_input(current_texts["student_name"])
with col2:
    academic_year = st.selectbox(current_texts["academic_year"], ["2024-2025", "2025-2026", "2026-2027"])

# تعريف المواد وحدود النجاح
subjects = {
    "الإسلامية": {"الفصل الأول": 75, "نصف السنة": 77, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 1},
    "اللغة العربية": {"الفصل الأول": 30, "نصف السنة": 40, "الفصل الثاني": 0, "حد النجاح": 80, "المعامل": 2},
    "اللغة الإنجليزية": {"الفصل الأول": 30, "نصف السنة": 48, "الفصل الثاني": 0, "حد النجاح": 72, "المعامل": 2},
    "الرياضيات": {"الفصل الأول": 50, "نصف السنة": 32, "الفصل الثاني": 0, "حد النجاح": 68, "المعامل": 3},
    "الفيزياء": {"الفصل الأول": 30, "نصف السنة": 8, "الفصل الثاني": 0, "حد النجاح": 112, "المعامل": 2},
    "الكيمياء": {"الفصل الأول": 14, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 136, "المعامل": 2},
    "الأحياء": {"الفصل الأول": 30, "نصف السنة": 14, "الفصل الثاني": 0, "حد النجاح": 106, "المعامل": 2},
    "اللغة الفرنسية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 1}
}

# الإعدادات
add_helping_marks = st.checkbox(current_texts["helping_marks"])

# إدخال الدرجات
col1, col2 = st.columns(2)
details = []
all_scores = []

for subject, scores in subjects.items():
    with col1:
        st.subheader(f"📌 {subject}")
        scores["الفصل الثاني"] = st.number_input(
            f"درجة الفصل الثاني - {subject}",
            value=float(scores["الفصل الثاني"]),
            min_value=0.0,
            max_value=100.0,
            step=1.0
        )

def calculate_possibility(current_score, required_score, max_possible):
    remaining_score_needed = required_score - current_score
    if remaining_score_needed <= max_possible:
        return True, remaining_score_needed
    return False, remaining_score_needed

# زر الحساب
if st.button(current_texts["calculate"]):
    if not student_name:
        st.error("الرجاء إدخال اسم الطالب" if language == "العربية" else "Please enter student name")
    else:
        passed_subjects = 0
        failed_subjects = 0
        total_weighted_score = 0
        total_weights = 0
        
        for subject, scores in subjects.items():
            current_score = (scores["الفصل الأول"] + scores["نصف السنة"]) / 2
            max_possible_final = 100  # أقصى درجة ممكنة في الفصل الثاني
            
            is_possible, needed_score = calculate_possibility(
                current_score,
                scores["حد النجاح"],
                max_possible_final
            )
            
            status_text = ""
            if is_possible:
                if needed_score <= 0:
                    status_text = "(ناجح بغض النظر عن الفصل الثاني)"
                else:
                    status_text = f"(يجب الحصول على {needed_score:.1f} أو أكثر للنجاح)"
            else:
                status_text = "(يستحيل النجاح)"
            
            details.append(f"**{subject}**: {current_score:.1f} {status_text}")
            all_scores.append({
                "المادة": subject,
                "الدرجة الحالية": current_score,
                "حد النجاح": scores["حد النجاح"],
                "الحالة": status_text
            })

        # عرض النتائج
        st.subheader(current_texts["final_results"])
        st.write("\n".join(details))
        
        # التحليلات المتقدمة
        st.subheader(current_texts["advanced_analytics"])
        
        # الرسم البياني الأول
        df = pd.DataFrame(all_scores)
        fig1 = go.Figure()
        
        fig1.add_trace(go.Bar(
            name='الدرجة الحالية',
            x=df['المادة'],
            y=df['الدرجة الحالية'],
            marker_color='rgb(26, 118, 255)'
        ))
        
        fig1.add_trace(go.Bar(
            name='حد النجاح',
            x=df['المادة'],
            y=df['حد النجاح'],
            marker_color='rgb(55, 83, 109)'
        ))
        
        fig1.update_layout(
            title='مقارنة الدرجات الحالية مع حد النجاح',
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # الرسم البياني الثاني (مخطط راداري)
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatterpolar(
            r=df['الدرجة الحالية'],
            theta=df['المادة'],
            fill='toself',
            name='الدرجات الحالية'
        ))
        
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title='التوزيع الشعاعي للدرجات'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # التوصيات
        st.subheader(current_texts["recommendations"])
        for subject, scores in subjects.items():
            current_score = (scores["الفصل الأول"] + scores["نصف السنة"]) / 2
            is_possible, needed_score = calculate_possibility(
                current_score,
                scores["حد النجاح"],
                100
            )
            
            if not is_possible:
                st.error(f"🚫 {subject}: يستحيل النجاح في هذه المادة. نقترح التركيز على المواد الأخرى.")
            elif needed_score > 0:
                if needed_score > 90:
                    st.error(f"⚠️ {subject}: تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني. هذا تحدٍ صعب جداً.")
                elif needed_score > 70:
                    st.warning(f"⚠️ {subject}: تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني. يتطلب جهداً كبيراً.")
                else:
                    st.info(f"ℹ️ {subject}: تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني. هدف قابل للتحقيق.")
            else:
                st.success(f"✅ {subject}: أنت ناجح بالفعل! حافظ على مستواك.")

        # زر الطباعة
        if st.button(current_texts["print"]):
            st.balloons()
            st.success("تم إرسال النتائج للطباعة" if language == "العربية" else "Results sent to printer")

if language == "English":
    st.markdown('</div>', unsafe_allow_html=True)
