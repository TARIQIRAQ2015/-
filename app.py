import streamlit as st
import pandas as pd
from PIL import Image
import base64
import os

# في بداية الملف، أضف هذا المتغير
DEFAULT_LOGO = """iVBORw0KGgoAAAANSUhEUgAA... """  # سيتم وضع رمز Base64 للصورة هنا

# تعريف أيقونة افتراضية في حالة عدم وجود الملف
try:
    icon = Image.open('assets/logo.png')
    icon_base64 = base64.b64encode(open('assets/logo.png', 'rb').read()).decode()
except FileNotFoundError:
    # استخدام الصورة الافتراضية
    icon_base64 = DEFAULT_LOGO
    icon = None

st.set_page_config(
    page_title="المساعد لحساب الوزاري",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إخفاء جميع العناصر الافتراضية
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# اختيار اللغة (نقل هذا الجزء إلى الأعلى)
language = st.selectbox("", ["العربية", "English"], index=0)
direction = 'rtl' if language == "العربية" else 'ltr'

# تعديل العنوان الرئيسي مع تحسين المحاذاة
st.markdown("""
    <div class="app-header">
        <h1 class="app-title">المساعد لحساب الوزاري</h1>
    </div>
""", unsafe_allow_html=True)

# تحديث CSS للعنوان
st.markdown("""
    <style>
    /* تنسيق العنوان الرئيسي */
    .app-header {
        text-align: center;
        width: 100%;
        position: relative;
        padding: 1rem;
        margin: 0;
    }
    
    .app-title {
        color: #00ff9d;
        font-size: 2rem;
        font-weight: bold;
        margin: 0 auto;
        text-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
        display: inline-block;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
        white-space: nowrap;
    }

    /* تحسين شكل قائمة اختيار اللغة */
    .stSelectbox {
        margin-bottom: 1rem;
    }

    .stSelectbox > div {
        width: fit-content;
        margin-left: auto;
    }

    /* إخفاء تسمية قائمة اختيار اللغة */
    .stSelectbox label {
        display: none;
    }

    /* تصحيح المسافات */
    .block-container {
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# إضافة العنوان في بداية التطبيق
st.markdown("""
    <div class="main-title">
        احسب دخولك للوزاري بدقة وسهولة
    </div>
""", unsafe_allow_html=True)

# إضافة CSS للعنوان
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #00ff9d;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1rem 0 2rem 0;
        padding: 1rem;
        background: rgba(0, 9, 42, 0.8);
        border-radius: 15px;
        border: 2px solid rgba(0, 255, 157, 0.2);
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# تحديد اتجاه النص بناءً على اللغة
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
    impossible_subjects = []  # المواد التي يستحيل النجاح فيها
    need_improvement_subjects = []  # المواد التي تحتاج إلى تحسين
    
    for subject, scores in subjects.items():
        # تضمين اللغة الفرنسية فقط إذا كان هناك درجة واحدة على الأقل
        if subject == "اللغة الفرنسية":
            has_any_grade = scores["الفصل الأول"] > 0 or scores["نصف السنة"] > 0 or scores["الفصل الثاني"] > 0
            if not has_any_grade:
                continue
            
        minimum_required = calculate_minimum_required(
            scores["الفصل الأول"],
            scores["نصف السنة"]
        )
        
        status = ""
        if minimum_required <= 0:
            status = f"✅ ({minimum_required:.0f})"
            passing_subjects.append(subject)
        elif minimum_required > 100:
            status = f"❌ ({minimum_required:.0f})"
            impossible_subjects.append(subject)
        else:
            status = f"❌ ({minimum_required:.0f})"
            need_improvement_subjects.append(subject)
        
        results.append({
            "المادة": subject,
            "الفصل الأول": scores["الفصل الأول"],
            "نصف السنة": scores["نصف السنة"],
            "الفصل الثاني": scores["الفصل الثاني"],
            "الحد الأدنى المطلوب في الفصل الثاني": status
        })
    
    # إنشاء وعرض جدول الدرجات
    df = pd.DataFrame(results)
    
    # إعادة ترتيب الأعمدة حسب اللغة
    if direction == 'rtl':
        column_order = ["المادة", "الفصل الأول", "نصف السنة", "الفصل الثاني", "الحد الأدنى المطلوب في الفصل الثاني"]
    else:
        column_order = ["الحد الأدنى المطلوب في الفصل الثاني", "الفصل الثاني", "نصف السنة", "الفصل الأول", "المادة"]
    
    df = df[column_order]
    
    # عرض جدول الدرجات
    st.markdown('<div class="results-table">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # عرض النصائح في قسم منفصل
    passed_subjects_str = "، ".join(passing_subjects) if passing_subjects else "لا يوجد"
    impossible_subjects_str = "، ".join(impossible_subjects) if impossible_subjects else "لا يوجد"
    need_improvement_subjects_str = "، ".join(need_improvement_subjects) if need_improvement_subjects else "لا يوجد"
    
    # تحديد إمكانية الدخول للوزاري
    total_subjects = len(results)  # عدد المواد الكلي
    passing_count = len(passing_subjects)  # عدد المواد المضمونة
    impossible_count = len(impossible_subjects)  # عدد المواد المستحيلة
    improvement_count = len(need_improvement_subjects)  # عدد المواد التي تحتاج تحسين
    
    # تحديد النصيحة النهائية
    final_advice = ""
    if passing_count >= 4:
        final_advice = (
            '<div class="advice-item success final-advice">'
            '🎉 مبارك! يمكنك الدخول للوزاري حيث أنك ضامن النجاح في 4 مواد أو أكثر.'
            '</div>'
        )
    elif passing_count + improvement_count >= 4:
        # تجميع المعلومات التفصيلية عن المواد التي تحتاج تحسين
        improvement_details = []
        for subject in need_improvement_subjects:
            min_required = calculate_minimum_required(
                subjects[subject]["الفصل الأول"],
                subjects[subject]["نصف السنة"]
            )
            improvement_details.append(f"{subject} (تحتاج {min_required:.0f} درجة)")

        improvement_subjects_details = "، ".join(improvement_details)
        
        final_advice = (
            '<div class="advice-item warning final-advice">'
            f'⚠️ يمكنك الدخول للوزاري مع التركيز على تحسين درجاتك.'
            f'<br>لديك {passing_count} مواد مضمونة.'
            f'<br>المواد التي تحتاج إلى تحسين هي: {improvement_subjects_details}.'
            f'<br>تحتاج إلى النجاح في {max(4 - passing_count, 0)} مواد على الأقل من المواد المتبقية.'
            '</div>'
        )
    else:
        final_advice = (
            '<div class="advice-item danger final-advice">'
            f'⛔ غير مؤهل للدخول للوزاري هذا العام.'
            f'<br>لديك فقط {passing_count} مواد مضمونة و {improvement_count} مواد تحتاج إلى تحسين.'
            f'<br>يجب ضمان النجاح في 4 مواد على الأقل للتأهل للوزاري.'
            '</div>'
        )

    # تحديث عرض النصائح مع إضافة التقييم النهائي
    st.markdown(f"""
        <div class="advice-section">
            <div class="advice-item success">
                ✅ المواد التي ضمنت النجاح هي: {passed_subjects_str} حتى لو حصلت على 0 في الفصل الثاني.
            </div>
            <br>
            <div class="advice-item warning">
                ⚠️ المواد التي تحتاج إلى تحسين هي: {need_improvement_subjects_str}
            </div>
            <br>
            <div class="advice-item danger">
                ❌ المواد التي يستحيل النجاح فيها هي: {impossible_subjects_str}
            </div>
            <br>
            <div class="final-advice-separator"></div>
            {final_advice}
        </div>
    """, unsafe_allow_html=True)

# إضافة CSS للتقييم النهائي
st.markdown("""
    <style>
    .final-advice-separator {
        border-top: 1px solid rgba(0, 255, 157, 0.2);
        margin: 1rem 0;
    }
    
    .final-advice {
        font-size: 1.2rem !important;
        padding: 1.2rem !important;
        margin-top: 1rem !important;
        border-width: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

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

print("Current working directory:", os.getcwd())
print("Logo file exists:", os.path.exists('logo.png'))

# تحديث CSS للتصميم الكامل
st.markdown(f"""
    <style>
    /* تحسين المظهر العام */
    .stApp {{
        background: linear-gradient(135deg, #000428 0%, #004e92 100%);
        direction: {direction};
    }}
    
    /* العنوان الرئيسي دائماً في الوسط */
    .app-header {{
        text-align: center !important;
    }}
    
    .app-title {{
        text-align: center !important;
    }}
    
    /* عناوين المواد في الوسط */
    .subject-name {{
        text-align: center !important;
    }}
    
    /* عناوين الفصول في الوسط */
    .grade-label {{
        text-align: center !important;
    }}
    
    /* محاذاة النص حسب اللغة */
    .advice-section {{
        text-align: {direction == 'rtl' and 'right' or 'left'} !important;
    }}
    
    /* تنسيق الجدول */
    .dataframe {{
        direction: {direction};
    }}
    
    .dataframe th {{
        text-align: center !important;
    }}
    
    /* المواد والفصول في وسط الجدول */
    .dataframe td:nth-child(1),
    .dataframe td:nth-child(2),
    .dataframe td:nth-child(3),
    .dataframe td:nth-child(4) {{
        text-align: center !important;
    }}
    
    /* الحد الأدنى المطلوب محاذاة حسب اللغة */
    .dataframe td:nth-child(5) {{
        text-align: {direction == 'rtl' and 'right' or 'left'} !important;
    }}
    
    /* تحسين قائمة اختيار اللغة */
    .stSelectbox {{
        text-align: {direction == 'rtl' and 'right' or 'left'} !important;
    }}
    
    /* روابط التذييل */
    .social-links {{
        text-align: center !important;
    }}
    
    .copyright {{
        text-align: center !important;
    }}
    
    /* تنسيق قسم النصائح */
    .advice-section {{
        background: rgba(0, 9, 42, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        font-size: 1.1rem;
        line-height: 1.8;
        text-align: {direction == 'rtl' and 'right' or 'left'};
        border: 1px solid rgba(0, 255, 157, 0.2);
        direction: {direction};
        box-shadow: 0 4px 15px rgba(0, 255, 157, 0.1);
    }}

    .advice-item {{
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}

    .advice-item.success {{
        background: rgba(0, 255, 157, 0.1);
        border-right: 4px solid #00ff9d;
        border-left: 4px solid #00ff9d;
    }}

    .advice-item.warning {{
        background: rgba(255, 193, 7, 0.1);
        border-right: 4px solid #ffc107;
        border-left: 4px solid #ffc107;
    }}

    .advice-item.danger {{
        background: rgba(255, 72, 72, 0.1);
        border-right: 4px solid #ff4848;
        border-left: 4px solid #ff4848;
    }}

    .final-advice-separator {{
        border-top: 2px solid rgba(0, 255, 157, 0.2);
        margin: 1.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 255, 157, 0.1);
    }}

    .final-advice {{
        font-size: 1.3rem !important;
        padding: 1.5rem !important;
        margin-top: 1.5rem !important;
        border-width: 4px !important;
        text-align: center !important;
        background: rgba(0, 9, 42, 0.9) !important;
        box-shadow: 0 4px 20px rgba(0, 255, 157, 0.15);
        animation: glow 2s infinite alternate;
    }}

    @keyframes glow {{
        from {{
            box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
        }}
        to {{
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.4);
        }}
    }}

    /* تحسين الأيقونات */
    .advice-item::before {{
        margin-left: 0.5rem;
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }}

    /* تحسين المسافات بين العناصر */
    br {{
        display: none;
    }}

    .advice-item + .advice-item {{
        margin-top: 1rem;
    }}
    </style>
""", unsafe_allow_html=True)

# تحديث CSS للتصميم المتجاوب
st.markdown("""
    <style>
    /* إزالة الهوامش والحواف الزائدة */
    .main .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    
    /* إزالة التمرير الأفقي */
    .main {
        overflow-x: hidden;
    }
    
    /* تحسين عرض الأعمدة */
    .stColumns {
        gap: 1rem !important;
    }
    
    /* تحسين عرض الجدول */
    .results-table {
        margin: 1rem 0;
        width: 100%;
    }
    
    /* تحسين عرض حقول الإدخال */
    .stNumberInput {
        width: 100% !important;
    }
    
    /* إخفاء شريط التمرير */
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* تعطيل التمرير الأفقي للصفحة بالكامل */
    body {
        overflow-x: hidden !important;
    }
    </style>
""", unsafe_allow_html=True)
