# utils/ui_components.py
import streamlit as st

def card(title: str, body: str):
    st.markdown(f"### {title}")
    st.write(body)

def two_column_layout(left_func, right_func, left_width=3, right_width=7):
    cols = st.columns([left_width, right_width])
    with cols[0]:
        left_func()
    with cols[1]:
        right_func()