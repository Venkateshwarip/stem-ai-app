import streamlit as st
from utils.theme import apply_theme

# ================= APPLY THEME =================
apply_theme()

# ---------------- BACKEND ----------------
from backend.ai_engine import smart_ai_explanation_with_debug
from backend import chat_manager
from backend.code_runner import run_code_simulated

# ---------------- RULE BASED MODELS ----------------
from models.code_explainer import line_by_line_explanation
from models.ai_debugger import debug_code

# ---------- PAGE TITLE ----------
st.title("Programming Tutor (T)")
user_id = "default_user"

# =========================================================
# 📚 STUDY MATERIAL DROPDOWN
# =========================================================

st.subheader("📚 Study Materials")

topic = st.selectbox(
    "Choose a topic",
    [
        "Select Topic",

        # 🔹 Programming Topics
        "Control Flow",
        "Data Structures",
        "OOPs Concepts",
        "Exception Handling",
        "File Handling",

        # 🔹 New Science Python Topics
        "Python Biology",
        "Python Botany",
        "Python Chemistry",
        "Python Maths",
        "Python Physics",
        "Python Zoology"
    ]
)

if topic != "Select Topic":
    if st.session_state.get("last_topic") != topic:
        st.session_state["selected_topic"] = topic
        st.session_state["last_topic"] = topic
        st.switch_page("pages/Study_Material.py")

st.divider()

# =========================================================
# 💻 CODE INPUT
# =========================================================

code = st.text_area(
    "Paste your code here (Python)",
    height=250
)

# =========================================================
# 📘 EXPLAIN CODE
# =========================================================

if st.button("Explain Code"):

    if not code.strip():
        st.warning("Paste some code to explain.")

    else:
        st.subheader("📘 Line-by-Line Explanation")

        explanations = line_by_line_explanation(code)

        for exp in explanations:
            st.write("•", exp)

        st.subheader("🤖 AI Explanation")

        ai_text, debug_tips = smart_ai_explanation_with_debug(code)

        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.15);
            border: 2px solid rgba(255,255,255,0.4);
            padding: 12px;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            margin-bottom: 10px;">
            {ai_text}
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🛠 AI Smart Debugging")

        if debug_tips:
            for tip in debug_tips:
                st.warning(tip)
        else:
            st.markdown("""
            <div style="
                background: rgba(255,255,255,0.15);
                border: 2px solid rgba(255,255,255,0.4);
                padding: 12px;
                border-radius: 12px;
                color: white;
                font-weight: 600;">
                ✅ No errors detected!
            </div>
            """, unsafe_allow_html=True)

        chat_manager.save_chat(
            "programming",
            user_id,
            code,
            ai_text
        )

# =========================================================
# 🛠 AI DEBUG BUTTON
# =========================================================

if st.button("AI Debug Code"):

    if not code.strip():
        st.warning("Paste some code first.")

    else:
        st.subheader("🛠 AI Debug Suggestions")

        suggestions = debug_code(code)

        for s in suggestions:
            st.write("•", s)

# =========================================================
# ▶ RUN CODE
# =========================================================

if st.button("Run (Simulated)"):

    if not code.strip():
        st.warning("Provide code to run.")

    else:
        output = run_code_simulated(code)

        st.subheader("▶ Execution Output (Simulated)")
        st.code(output)

        chat_manager.save_chat(
            "programming",
            user_id,
            code,
            f"Run output:\n{output}"
        )
