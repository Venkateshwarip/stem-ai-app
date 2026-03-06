import streamlit as st
import sqlite3
import hashlib
import pandas as pd
from pathlib import Path
from utils.theme import apply_theme

# ---------- DEFAULT LOGIN ----------
ADMIN_EMAIL = "admin@stem.com"
ADMIN_PASS = "admin123"

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="AI in STEM Tutor",
    page_icon="🧠",
    layout="wide"
)

apply_theme()

# -------------------------------------------------
# SAFE GLOBAL CSS
# -------------------------------------------------
def apply_global_theme():
    st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .auth-card {
        background: linear-gradient(135deg, #081b4b, #0e2a6f);
        padding: 40px;
        border-radius: 22px;
        box-shadow: 0 0 40px rgba(79,195,247,0.35);
        text-align: center;
    }
    footer {visibility:hidden;}
    #MainMenu {visibility:hidden;}
    [data-testid="stStatusWidget"] { display:none; }
    </style>
    """, unsafe_allow_html=True)

def hide_sidebar():
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
conn = sqlite3.connect("tutor.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(email, password):
    c.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hash_password(password))
    )
    return c.fetchone() is not None

# -------------------------------------------------
# ADMIN DASHBOARD (FIXED — 11 SUBJECTS)
# -------------------------------------------------
def admin_dashboard():
    st.title("📊 ADMIN — ALL USERS PERFORMANCE")

    df = pd.read_sql_query(
        "SELECT student_name, topic, score FROM quiz_marks",
        conn
    )

    if df.empty:
        st.warning("No Quiz Performance Found")
        return

    # ✅ Define all 11 subjects
    all_subjects = [
        "Control Flow",
        "Data Structures",
        "File Handling",
        "OOPs Concepts",
        "Python Biology",
        "Python Exception Handling",
        "Python Botany",
        "Python Maths",
        "Python Physics",
        "Python Zoology",
        "Python Chemistry"
    ]

    # Create pivot table
    table = df.pivot_table(
        index="student_name",
        columns="topic",
        values="score",
        aggfunc="sum"
    ).fillna(0)

    # Add missing subject columns
    for subject in all_subjects:
        if subject not in table.columns:
            table[subject] = 0

    # Reorder columns
    table = table[all_subjects]

    # Calculate total
    table["Total Score"] = table.sum(axis=1)

    # Assuming each subject is out of 20
    MAX_TOTAL = 11 * 20

    table["Percentage"] = (table["Total Score"] / MAX_TOTAL) * 100

    st.dataframe(table.reset_index(), use_container_width=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("user_email", "")
st.session_state.setdefault("username", "")
st.session_state.setdefault("show_signup", False)
st.session_state.setdefault("role", "user")

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
def login_page():
    apply_global_theme()
    hide_sidebar()

    col1, col2, col3 = st.columns([2,3,2])

    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        st.title("🔐 AI STEM Tutor")
        st.caption("Login to continue")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", use_container_width=True):

            # ADMIN LOGIN
            if email == ADMIN_EMAIL and password == ADMIN_PASS:
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.session_state.user_email = email
                st.session_state.username = email
                st.rerun()

            # USER LOGIN
            elif validate_user(email, password):
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.session_state.user_email = email
                st.session_state.username = email
                st.rerun()

            else:
                st.error("Invalid email or password")

        if st.button("New user? Sign up", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# SIGNUP PAGE
# -------------------------------------------------
def signup_page():
    apply_global_theme()
    hide_sidebar()

    col1, col2, col3 = st.columns([2,3,2])

    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        st.title("📝 Create Account")
        st.caption("Register with your email")

        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Create Account", use_container_width=True):
            if password != confirm:
                st.error("Passwords do not match")
            elif create_user(email, password):
                st.success("Account created successfully")
                st.session_state.show_signup = False
                st.rerun()
            else:
                st.error("Email already exists")

        if st.button("Back to Login", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------
def home_page():
    apply_global_theme()

    # ---------------- ADMIN VIEW ----------------
    if st.session_state.role == "admin":

        # Hide sidebar fully
        hide_sidebar()

        col1, col2 = st.columns([8, 1])
        with col1:
            st.success(f"👑 Admin: {st.session_state.user_email}")
        with col2:
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.session_state.user_email = ""
                st.session_state.username = ""
                st.session_state.role = "user"
                st.rerun()

        admin_dashboard()
        return

    # ---------------- USER VIEW ----------------
    else:
        # Show sidebar only for users
        st.sidebar.success(f"👤 {st.session_state.user_email}")

        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.username = ""
            st.session_state.role = "user"
            st.rerun()

        st.markdown("""
        <div style="text-align:center; padding:30px">
            <h1>AI in STEM — Intelligent Tutoring</h1>
            <p>Explore Programming, Quizzes, Study Material and Student Performance using the sidebar</p>
        </div>
        """, unsafe_allow_html=True)

        img = Path("assets/images/ai_stem_home.png")
        if img.exists():
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image(str(img), width=520)


# -------------------------------------------------
# ROUTER
# -------------------------------------------------
if st.session_state.logged_in:
    home_page()
else:
    signup_page() if st.session_state.show_signup else login_page()
