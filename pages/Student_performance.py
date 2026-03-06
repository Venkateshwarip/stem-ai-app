# ==========================================================
# 📊 STUDENT PERFORMANCE ANALYSIS MODULE
# ==========================================================

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.theme import apply_theme

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Student Performance", layout="wide")
apply_theme()
st.title("📊 Student Performance Analysis")

# ------------------ CHECK LOGIN ------------------
if "username" not in st.session_state:
    st.error("⚠️ Please login first.")
    st.stop()

current_student = st.session_state["username"]

# ------------------ DATABASE CONNECTION ------------------
conn = sqlite3.connect("tutor.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ FETCH DATA (ONLY CURRENT USER) ------------------
cursor.execute("""
    SELECT student_name, topic, score, total, date
    FROM quiz_marks
    WHERE student_name = ?
    ORDER BY date
""", (current_student,))

rows = cursor.fetchall()

# If no quiz attempts
if not rows:
    st.warning("📌 You have not attempted any quiz yet.")
    st.stop()

# ------------------ DATAFRAME ------------------
df = pd.DataFrame(rows, columns=["Student", "Topic", "Score", "Total", "Date"])
df["Percentage"] = (df["Score"] / df["Total"]) * 100


# ==========================================================
# 📘 TOPIC-WISE PERFORMANCE (BAR GRAPH)
# ==========================================================

st.subheader("📘 Topic-wise Performance")

topic_summary = df.groupby("Topic").agg({
    "Score": "sum",
    "Total": "sum"
}).reset_index()

topic_summary["Percentage"] = (topic_summary["Score"] / topic_summary["Total"]) * 100

fig_bar = px.bar(
    topic_summary,
    x="Topic",
    y="Percentage",
    text="Percentage",
    color="Percentage",
    color_continuous_scale="Viridis",
    labels={"Percentage": "Score (%)"}
)

fig_bar.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_bar.update_layout(yaxis=dict(range=[0, 100]))

st.plotly_chart(fig_bar, use_container_width=True)


# ==========================================================
# 📈 PERFORMANCE IMPROVEMENT (LINE GRAPH)
# ==========================================================

st.subheader("📈 Performance Improvement")

df = df.sort_values("Date").reset_index(drop=True)
df["Attempt"] = range(1, len(df) + 1)

fig_line = go.Figure()

fig_line.add_trace(go.Scatter(
    x=df["Attempt"],
    y=df["Percentage"],
    mode="lines+markers",
    name=current_student
))

fig_line.update_layout(
    xaxis_title="Attempt Number",
    yaxis_title="Score (%)",
    yaxis=dict(range=[0, 100])
)

st.plotly_chart(fig_line, use_container_width=True)


# ==========================================================
# 📋 DETAILED ATTEMPTS TABLE
# ==========================================================

st.subheader("📋 Detailed Attempts")

st.dataframe(
    df[["Date", "Topic", "Score", "Total", "Percentage"]],
    use_container_width=True
)


# ==========================================================
# 🤖 AI-BASED LEARNING RECOMMENDATIONS
# ==========================================================

st.subheader("🤖 Personalized Learning Recommendations")

topic_avg = df.groupby("Topic")["Percentage"].mean().reset_index()
overall_avg = df["Percentage"].mean()

st.write(f"📌 Overall Average Score: {overall_avg:.2f}%")

st.write("📚 Average Performance by Topic:")
st.dataframe(topic_avg, use_container_width=True)

# ------------------ CLASSIFICATION ------------------

weak_topics = topic_avg[topic_avg["Percentage"] < 40]["Topic"].tolist()
medium_topics = topic_avg[
    (topic_avg["Percentage"] >= 40) & (topic_avg["Percentage"] < 70)
]["Topic"].tolist()
strong_topics = topic_avg[topic_avg["Percentage"] >= 70]["Topic"].tolist()

if weak_topics:
    st.warning("⚠️ Topics needing immediate revision:")
    for t in weak_topics:
        st.write("👉", t)

if medium_topics:
    st.info("📖 Topics that need more practice:")
    for t in medium_topics:
        st.write("👉", t)

if strong_topics:
    st.success("🎉 Strong topics:")
    for t in strong_topics:
        st.write("👉", t)

st.divider()


# ==========================================================
# 🧠 AI LEARNING PATH GENERATOR
# ==========================================================

st.subheader("🧠 AI Suggested Learning Path")

topic_sorted = topic_avg.sort_values("Percentage")

for _, row in topic_sorted.iterrows():

    if row["Percentage"] < 40:
        status = "🔴 Weak"
    elif row["Percentage"] < 70:
        status = "🟡 Average"
    else:
        status = "🟢 Strong"

    st.write(f"➡️ {row['Topic']} — {status} ({row['Percentage']:.1f}%)")


# ==========================================================
# 🔥 TOPIC WEAKNESS HEATMAP
# ==========================================================

st.subheader("🔥 Learning Weakness Heatmap")

heatmap_data = df.pivot_table(
    index="Student",
    columns="Topic",
    values="Percentage",
    aggfunc="mean"
)

fig_heat = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale="RdYlGn",
    labels=dict(color="Score %")
)

st.plotly_chart(fig_heat, use_container_width=True)


# ==========================================================
# 📊 OVERALL FEEDBACK
# ==========================================================

if overall_avg < 40:
    st.error("❗ Overall performance is low. Focus on basics and revise regularly.")
elif overall_avg < 70:
    st.warning("🙂 Good progress! Practice more to improve.")
else:
    st.success("🚀 Excellent performance! Try advanced challenges.")
