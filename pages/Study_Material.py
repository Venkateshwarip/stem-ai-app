import streamlit as st
import os
import fitz  # PyMuPDF
from PIL import Image
from utils.theme import apply_theme
apply_theme()

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(layout="wide")

# =========================================================
# 🔒 PROTECT DIRECT ACCESS
# =========================================================
if "selected_topic" not in st.session_state:
    st.error("Please select a topic from Programming Tutor.")
    st.stop()

topic = st.session_state["selected_topic"].strip().lower()

# =========================================================
# 📚 HEADER + QUIZ BUTTON
# =========================================================
col1, col2 = st.columns([8, 2])

with col1:
    st.title("📚 Study Materials")
    st.subheader(f"📌 Topic: {topic.title()}")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📝 Take Quiz"):
        st.session_state["quiz_topic"] = topic.title()
        st.switch_page("pages/Quiz.py")

st.divider()

# =========================================================
# 📁 TOPIC → FOLDER MAP
# =========================================================
folder_map = {
    # 🔹 Programming Topics
    "control flow": "control_flow",
    "data structures": "data_structures",
    "oops concepts": "oops",
    "exception handling": "exception_handling",
    "file handling": "file_handling",

    # 🔹 New Science Python Topics
    "python biology": "python_biology",
    "python botany": "python_botany",
    "python chemistry": "python_chemistry",
    "python maths": "python_maths",
    "python physics": "python_physics",
    "python zoology": "python_zoology"
}

base_path = os.path.join("assets", "study_material")
topic_folder = folder_map.get(topic)

if not topic_folder:
    st.error("Invalid topic selected.")
    st.stop()

folder_path = os.path.join(base_path, topic_folder)

if not os.path.exists(folder_path):
    st.warning("Study material folder not found.")
    st.stop()

files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]

if not files:
    st.info("No study material uploaded yet.")
    st.stop()

# =========================================================
# 📄 DISPLAY PDF CONTENT INLINE
# =========================================================
for file in files:
    file_path = os.path.join(folder_path, file)

    st.markdown(f"## 📄 {file}")

    doc = fitz.open(file_path)
    st.success(f"Pages: {len(doc)}")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            colorspace=fitz.csRGB
        )
        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )
        st.image(img, use_container_width=True)

    with open(file_path, "rb") as f:
        st.download_button(
            label="⬇ Download PDF",
            data=f,
            file_name=file,
            mime="application/pdf"
        )

    st.divider()
