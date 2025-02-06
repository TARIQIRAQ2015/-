import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import json

# إخفاء عناصر Streamlit الافتراضية
st.set_page_config(
    page_title="نظام إدارة الدرجات المتطور",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إخفاء عناصر واجهة المستخدم الافتراضية
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
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
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 2rem;
        border-radius: 20px;
        color: #fff;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #4a90e2 0%, #2b6cb0 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        font-weight: bold;
        margin-top: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(74, 144, 226, 0.4);
    }
    
    div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .stTextInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        text-align: right;
    }
    
    .stSelectbox>div>div>div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
        text-align: right;
    }
    
    h1, h2, h3 {
        color: #4a90e2;
        text-align: right;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        border-radius: 8px;
        text-align: right;
    }
    
    .success-box {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .english-mode * {
        direction: ltr;
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
        "failed": "راسب",
        "enter_name": "الرجاء إدخال اسم الطالب",
        "print_success": "تم إرسال النتائج للطباعة"
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
        "failed": "Failed",
        "enter_name": "Please enter student name",
        "print_success": "Results sent to printer"
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
    "اللغة الفرنسية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 1},
    "الرياضيات": {"الفصل الأول": 50, "نصف السنة": 32, "الفصل الثاني": 0, "حد النجاح": 68, "المعامل": 3},
    "الفيزياء": {"الفصل الأول": 30, "نصف السنة": 8, "الفصل الثاني": 0, "حد النجاح": 112, "المعامل": 2},
    "الكيمياء": {"الفصل الأول": 14, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 136, "المعامل": 2},
    "الأحياء": {"الفصل الأول": 30, "نصف السنة": 14, "الفصل الثاني": 0, "حد النجاح": 106, "المعامل": 2}
}

# الإعدادات
add_helping_marks = st.checkbox(current_texts["helping_marks"])

# إدخال الدرجات في جدول منظم
st.subheader("📝 درجات المواد")
for subject, scores in subjects.items():
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown(f"**{subject}**")
    with cols[1]:
        scores["الفصل الثاني"] = st.number_input(
            f"درجة الفصل الثاني - {subject}",
            value=float(scores["الفصل الثاني"]),
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            key=f"grade_{subject}"
        )

def calculate_possibility(current_score, required_score, max_possible):
    remaining_score_needed = required_score - current_score
    if remaining_score_needed <= max_possible:
        return True, remaining_score_needed
    return False, remaining_score_needed

# زر الحساب
if st.button(current_texts["calculate"], key="calculate_btn"):
    if not student_name:
        st.error(current_texts["enter_name"])
    else:
        all_scores = []
        
        # حساب النتائج
        for subject, scores in subjects.items():
            current_score = (scores["الفصل الأول"] + scores["نصف السنة"]) / 2
            is_possible, needed_score = calculate_possibility(
                current_score,
                scores["حد النجاح"],
                100
            )
            
            status_text = ""
            if is_possible:
                if needed_score <= 0:
                    status_text = "✅ (ناجح بغض النظر عن الفصل الثاني)"
                else:
                    status_text = f"⚠️ (يجب الحصول على {needed_score:.1f} أو أكثر للنجاح)"
            else:
                status_text = "❌ (يستحيل النجاح)"
            
            all_scores.append({
                "المادة": subject,
                "الدرجة الحالية": current_score,
                "حد النجاح": scores["حد النجاح"],
                "الحالة": status_text
            })
        
        # عرض النتائج في جدول منظم
        df_results = pd.DataFrame(all_scores)
        st.subheader(current_texts["final_results"])
        st.table(df_results)
        
        # الرسوم البيانية
        st.subheader(current_texts["advanced_analytics"])
        
        # مخطط شريطي مقارن
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            name='الدرجة الحالية',
            x=df_results['المادة'],
            y=df_results['الدرجة الحالية'],
            marker_color='rgba(74, 144, 226, 0.8)'
        ))
        
        fig1.add_trace(go.Bar(
            name='حد النجاح',
            x=df_results['المادة'],
            y=df_results['حد النجاح'],
            marker_color='rgba(255, 99, 132, 0.8)'
        ))
        
        fig1.update_layout(
            title='مقارنة الدرجات الحالية مع حد النجاح',
            barmode='group',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
        )
        
        st.plotly_chart(fig1, use_container_width=True)
        
        # مخطط راداري
        fig2 = go.Figure()
        fig2.add_trace(go.Scatterpolar(
            r=df_results['الدرجة الحالية'],
            theta=df_results['المادة'],
            fill='toself',
            name='الدرجات الحالية',
            line_color='rgba(74, 144, 226, 0.8)'
        ))
        
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    color='white'
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title='التوزيع الشعاعي للدرجات'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
        # التوصيات المحسنة
        st.subheader(current_texts["recommendations"])
        for subject, scores in subjects.items():
            current_score = (scores["الفصل الأول"] + scores["نصف السنة"]) / 2
            is_possible, needed_score = calculate_possibility(
                current_score,
                scores["حد النجاح"],
                100
            )
            
            if not is_possible:
                with st.error(f"🚫 {subject}"):
                    st.write("يستحيل النجاح في هذه المادة. نقترح التركيز على المواد الأخرى.")
            elif needed_score > 0:
                if needed_score > 90:
                    with st.error(f"⚠️ {subject}"):
                        st.write(f"تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني. هذا تحدٍ صعب جداً.")
                        st.write("توصيات:")
                        st.write("- التركيز المكثف على هذه المادة")
                        st.write("- طلب مساعدة إضافية من المعلم")
                        st.write("- تخصيص وقت دراسة إضافي")
                elif needed_score > 70:
                    with st.warning(f"⚠️ {subject}"):
                        st.write(f"تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني. يتطلب جهداً كبيراً.")
                        st.write("توصيات:")
                        st.write("- مراجعة المواضيع السابقة")
                        st.write("- حل تمارين إضافية")
                else:
                    with st.info(f"ℹ️ {subject}"):
                        st.write(f"تحتاج إلى {needed_score:.1f} درجة في الفصل الثاني. هدف قابل للتحقيق.")
                        st.write("توصيات:")
                        st.write("- المحافظة على مستوى الدراسة الحالي")
                        st.write("- مراجعة دورية للمواد")
            else:
                with st.success(f"✅ {subject}"):
                    st.write("أنت ناجح بالفعل! حافظ على مستواك الممتاز.")

        # زر الطباعة
        if st.button(current_texts["print"]):
            st.balloons()
            st.success(current_texts["print_success"])

if language == "English":
    st.markdown('</div>', unsafe_allow_html=True)
