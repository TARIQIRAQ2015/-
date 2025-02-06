import streamlit as st
import plotly.express as px
import pandas as pd
import sqlite3
from datetime import datetime
from fpdf import FPDF
import os

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('grades.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS grades
                 (student_name TEXT, subject TEXT, first_term REAL, 
                  mid_term REAL, second_term REAL, final_grade REAL, 
                  date TEXT)''')
    conn.commit()
    conn.close()

# تهيئة قاعدة البيانات
init_db()

# تكوين الصفحة
st.set_page_config(page_title="نظام إدارة الدرجات المتقدم", layout="wide")

# CSS للتصميم
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .success-text {
        color: green;
        font-weight: bold;
    }
    .failure-text {
        color: red;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# عنوان التطبيق
st.title("🎓 النظام المتقدم لإدارة وتحليل الدرجات")

# بيانات الطالب
student_name = st.text_input("📝 اسم الطالب")
academic_year = st.selectbox("السنة الدراسية", ["2024-2025", "2025-2026", "2026-2027"])

# تعريف المواد وحدود النجاح
subjects = {
    "الإسلامية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 1},
    "اللغة العربية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 2},
    "اللغة الإنجليزية": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 2},
    "الرياضيات": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 3},
    "الفيزياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 2},
    "الكيمياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 2},
    "الأحياء": {"الفصل الأول": 0, "نصف السنة": 0, "الفصل الثاني": 0, "حد النجاح": 50, "المعامل": 2},
}

# الإعدادات المتقدمة
with st.expander("⚙️ الإعدادات المتقدمة"):
    add_helping_marks = st.checkbox("إضافة 10 درجات مساعدة")
    show_analytics = st.checkbox("عرض التحليلات المتقدمة", value=True)
    enable_recommendations = st.checkbox("تفعيل نظام التوصيات", value=True)

# إدخال الدرجات
col1, col2 = st.columns(2)
details = []
all_scores = []

for subject, scores in subjects.items():
    with col1:
        st.subheader(f"📌 {subject}")
        scores["الفصل الأول"] = st.number_input(f"درجة الفصل الأول - {subject}", 0, 100, step=1)
        scores["نصف السنة"] = st.number_input(f"درجة نصف السنة - {subject}", 0, 100, step=1)
        scores["الفصل الثاني"] = st.number_input(f"درجة الفصل الثاني - {subject}", 0, 100, step=1)

def generate_pdf(student_name, details, final_result):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    
    # إضافة العنوان
    pdf.cell(200, 10, txt=f"تقرير درجات الطالب: {student_name}", ln=True, align='C')
    pdf.ln(10)
    
    # إضافة التفاصيل
    for detail in details:
        pdf.cell(200, 10, txt=detail, ln=True)
    
    # إضافة النتيجة النهائية
    pdf.ln(10)
    pdf.cell(200, 10, txt=final_result, ln=True)
    
    # حفظ الملف
    filename = f"نتائج_{student_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def calculate_gpa(total_scores):
    if total_scores >= 90:
        return "ممتاز", 4.0
    elif total_scores >= 80:
        return "جيد جداً", 3.5
    elif total_scores >= 70:
        return "جيد", 3.0
    elif total_scores >= 60:
        return "مقبول", 2.5
    else:
        return "ضعيف", 2.0

# زر الحساب
if st.button("🔍 حساب النتيجة"):
    if not student_name:
        st.error("الرجاء إدخال اسم الطالب")
    else:
        passed_subjects = 0
        failed_subjects = 0
        total_weighted_score = 0
        total_weights = 0
        
        for subject, scores in subjects.items():
            total_score = (scores["الفصل الأول"] + scores["نصف السنة"] + scores["الفصل الثاني"]) / 3
            if add_helping_marks:
                total_score = min(100, total_score + 10)
            
            weighted_score = total_score * scores["المعامل"]
            total_weighted_score += weighted_score
            total_weights += scores["المعامل"]
            
            result = "✅ ناجح" if total_score >= scores["حد النجاح"] else "❌ راسب"
            details.append(f"**{subject}**: {total_score:.2f} - {result}")
            all_scores.append({"المادة": subject, "الدرجة": total_score})
            
            # حفظ في قاعدة البيانات
            conn = sqlite3.connect('grades.db')
            c = conn.cursor()
            c.execute("""INSERT INTO grades VALUES (?, ?, ?, ?, ?, ?, ?)""",
                     (student_name, subject, scores["الفصل الأول"], 
                      scores["نصف السنة"], scores["الفصل الثاني"], 
                      total_score, datetime.now().strftime("%Y-%m-%d")))
            conn.commit()
            conn.close()
            
            if total_score >= scores["حد النجاح"]:
                passed_subjects += 1
            else:
                failed_subjects += 1
        
        # حساب المعدل التراكمي
        final_average = total_weighted_score / total_weights
        grade_letter, gpa = calculate_gpa(final_average)
        
        # عرض النتائج
        st.subheader("📊 النتيجة النهائية")
        st.write("\n".join(details))
        
        # تحليل النجاح والرسوب
        st.subheader("📢 التحليل")
        if passed_subjects >= 4:
            result_text = f"🎉 مبروك! لقد نجحت، حيث نجحت في {passed_subjects} مواد ورسبت في {failed_subjects} مواد."
            st.success(result_text)
        else:
            result_text = f"⚠️ للأسف، أنت راسب لأنك نجحت فقط في {passed_subjects} مواد."
            st.error(result_text)
        
        st.write(f"المعدل التراكمي: {final_average:.2f}")
        st.write(f"التقدير: {grade_letter}")
        st.write(f"المعدل النقطي: {gpa}")
        
        # التحليلات المتقدمة
        if show_analytics:
            st.subheader("📈 التحليلات المتقدمة")
            df = pd.DataFrame(all_scores)
            
            # رسم بياني للدرجات
            fig = px.bar(df, x="المادة", y="الدرجة",
                        title="تحليل الدرجات حسب المواد",
                        labels={"المادة": "المادة الدراسية", "الدرجة": "الدرجة النهائية"})
            st.plotly_chart(fig)
        
        # نظام التوصيات
        if enable_recommendations:
            st.subheader("💡 التوصيات")
            for subject, scores in subjects.items():
                total_score = (scores["الفصل الأول"] + scores["نصف السنة"] + scores["الفصل الثاني"]) / 3
                if total_score < scores["حد النجاح"]:
                    st.warning(f"توصية لمادة {subject}: يجب التركيز على تحسين الأداء في هذه المادة.")
                elif total_score < 70:
                    st.info(f"توصية لمادة {subject}: هناك مجال للتحسين للوصول إلى مستوى أفضل.")
        
        # تصدير النتائج
        if st.button("📤 تصدير النتائج كملف PDF"):
            try:
                filename = generate_pdf(student_name, details, result_text)
                st.success(f"تم تصدير النتائج إلى الملف: {filename}")
            except Exception as e:
                st.error(f"حدث خطأ أثناء إنشاء ملف PDF: {str(e)}")

# إضافة قسم لإدخال مواد جديدة
with st.sidebar:
    st.subheader("➕ إضافة مادة جديدة")
    new_subject = st.text_input("اسم المادة الجديدة")
    new_pass_mark = st.number_input("حد النجاح للمادة الجديدة", 0, 100, step=1, value=50)
    new_weight = st.number_input("معامل المادة", 1, 5, step=1, value=1)
    
    if st.button("إضافة المادة"):
        if new_subject:
            subjects[new_subject] = {
                "الفصل الأول": 0,
                "نصف السنة": 0,
                "الفصل الثاني": 0,
                "حد النجاح": new_pass_mark,
                "المعامل": new_weight
            }
            st.success(f"تمت إضافة المادة: {new_subject}")
        else:
            st.error("يرجى إدخال اسم المادة.")
    
    # حذف المواد
    st.subheader("🗑️ حذف مادة")
    subject_to_delete = st.selectbox("اختر المادة للحذف", list(subjects.keys()))
    
    if st.button("حذف المادة"):
        del subjects[subject_to_delete]
        st.success(f"تم حذف المادة: {subject_to_delete}")
