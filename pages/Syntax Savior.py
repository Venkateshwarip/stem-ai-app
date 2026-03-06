import streamlit as st
import time
from utils.theme import apply_theme

apply_theme()

st.title("🐞 Syntax Savior - Level Challenge")

# -------------------------
# Question Bank
# -------------------------
question_bank = {
    "Easy": [
        {"code": "print 'Hello'", "answer": "Missing parentheses"},
        {"code": "for i in range(5)\n    print(i)", "answer": ":"},
        {"code": "x = 5\nif x == 5\n    print(x)", "answer": ":"},
        {"code": "print(5+)", "answer": "SyntaxError"},
        {"code": "a = 10\nb = '5'\nprint(a + b)", "answer": "TypeError"}
    ],
    "Moderate": [
        {"code": "def add(a,b):\nreturn a+b", "answer": "Indentation error"},
        {"code": "x = 10\nif x = 5:\n    print(x)", "answer": "Use =="},
        {"code": "numbers = [1,2,3]\nprint(numbers[3])", "answer": "IndexError"},
        {"code": "import maths", "answer": "Module name is math"},
        {"code": "print(len(5))", "answer": "TypeError"}
    ],
    "Hard": [
        {"code": "x = [1,2,3]\nprint(x.remove(2))", "answer": "remove returns None"},
        {"code": "def func():\n    try:\n        return 1/0\n    except:\n        pass", "answer": "ZeroDivisionError"},
        {"code": "print(bool('False'))", "answer": "Output is True"},
        {"code": "a = {1,2,3}\na[0]", "answer": "TypeError"},
        {"code": "print(0.1 + 0.2 == 0.3)", "answer": "Floating point precision"}
    ]
}

levels = ["Easy", "Moderate", "Hard"]

# -------------------------
# Session State
# -------------------------
if "current_level" not in st.session_state:
    st.session_state.current_level = "Easy"
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.feedback = None
    st.session_state.start_time = time.time()

current_level = st.session_state.current_level
questions = question_bank[current_level]

st.subheader(f"🔓 Current Level: {current_level}")
st.write(f"### 🏆 Current Score: {st.session_state.score}")

# -------------------------
# Display Question
# -------------------------
if st.session_state.q_index < 5:

    q = questions[st.session_state.q_index]

    # TIMER
    time_limit = 15
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = time_limit - elapsed

    # Progress bar
    progress = remaining / time_limit
    st.progress(max(progress, 0.0))

    # Time Up Logic
    if remaining <= 0:
        st.session_state.feedback = ("time", q["answer"])
        st.session_state.q_index += 1
        st.session_state.start_time = time.time()
        st.rerun()

    st.write(f"⏳ Time Remaining: {remaining} seconds")
    st.code(q["code"], language="python")

    user_answer = st.text_input("Identify the error:", key="answer_input")

    if st.button("Submit Answer"):

        if user_answer.strip().lower() in q["answer"].lower():
            st.session_state.score += 10
            st.session_state.feedback = ("correct", None)
        else:
            st.session_state.feedback = ("wrong", q["answer"])

        st.session_state.q_index += 1
        st.session_state.start_time = time.time()
        st.rerun()

    # -------------------------
    # White Feedback Card
    # -------------------------
    if st.session_state.feedback:

        status, answer = st.session_state.feedback

        if status == "correct":
            message = "✅ Correct! +10 points"
            border_color = "#00ff88"

        elif status == "wrong":
            message = f"❌ Wrong! Correct Answer: {answer}"
            border_color = "#ffa500"

        elif status == "time":
            message = f"⏰ Time's Up! Correct Answer: {answer}"
            border_color = "#ff4b4b"

        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:10px;
                background-color:rgba(0,0,0,0.6);
                color:white;
                font-size:18px;
                font-weight:600;
                border-left:6px solid {border_color};
                margin-top:15px;
            ">
            {message}
            </div>
            """,
            unsafe_allow_html=True
        )

    time.sleep(1)
    st.rerun()

# -------------------------
# Level Completed
# -------------------------
else:

    st.success(f"🎉 Level {current_level} Completed!")
    st.write(f"### Final Score: {st.session_state.score}")

    current_index = levels.index(current_level)

    if current_index < 2:
        next_level = levels[current_index + 1]

        if st.button(f"🔓 Go to {next_level} Level"):
            st.session_state.current_level = next_level
            st.session_state.q_index = 0
            st.session_state.feedback = None
            st.session_state.start_time = time.time()
            st.rerun()
    else:
        st.balloons()
        st.success("🏆 You Completed All Levels!")

    if st.button("🔄 Restart Game"):
        st.session_state.current_level = "Easy"
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.feedback = None
        st.session_state.start_time = time.time()
        st.rerun()
