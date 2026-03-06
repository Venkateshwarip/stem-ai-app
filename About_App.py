import streamlit as st
from utils.theme import apply_theme

# -------------------------------------------------
# PAGE CONFIG (MUST BE FIRST)
# -------------------------------------------------
st.set_page_config(
    page_title="About — AI in STEM App",
    layout="wide"
)

apply_theme()

# -------------------------------------------------
# EXTRA PARAGRAPH GAP CSS
# -------------------------------------------------
st.markdown("""
<style>

.content-card{
    max-width:900px;
    margin:auto;
    padding:30px;
}

.content-text{
    font-size:18px;
    line-height:1.8;
    margin-bottom:28px;  /* 👈 GAP BETWEEN PARAGRAPHS */
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# ABOUT CONTENT
# -------------------------------------------------
st.markdown("""
<h1 style="text-align:center;">About — AI in STEM App</h1>

<div class="content-card">

<div class="content-text">
The AI in STEM App is an intelligent learning platform developed to enhance
the teaching and learning experience in STEM higher education. It focuses on
improving students’ understanding of programming and computational thinking
through interactive and AI-supported learning methods.
</div>

<div class="content-text">
The application features an AI-powered virtual tutor that provides real-time
coding assistance, explanations, and debugging support. Through an interactive
chatbot interface, students can explore concepts step by step and receive
personalized guidance.
</div>

<div class="content-text">
The platform also includes integrated study materials, quizzes, and performance
tracking tools. These features allow students to practice regularly, assess
their understanding, and monitor academic progress effectively.
</div>

<div class="content-text">
Built using lightweight open-source technologies such as Python, Streamlit,
and SQLite, the application is scalable and suitable for institutions with
limited resources while maintaining high-quality educational support.
</div>

<div class="content-text">
Overall, the AI in STEM App promotes interactive, personalized learning by
combining intelligent tutoring, real-time feedback, and performance analytics.
It empowers students to build strong STEM foundations and confidently apply
their knowledge to real-world challenges.
</div>

</div>
""", unsafe_allow_html=True)
