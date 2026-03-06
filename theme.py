import streamlit as st

def apply_theme():
    st.markdown("""
    <style>

    /* ================= MAIN APP ================= */
    .stApp {
        background: linear-gradient(135deg,#1a1a2e,#2a1b5f,#4b2ca3,#7b61ff);
        color:white;
        font-family:'Segoe UI',sans-serif;
    }

    h1,h2,h3,label {
        color:white !important;
        font-weight:700;
    }

    /* ================= SIDEBAR BACKGROUND ================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#1a1a2e,#2a1b5f,#4b2ca3) !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
        font-weight:600;
    }

    /* ================= SIDEBAR MENU TITLES BOLD ================= */

    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        font-weight: 800 !important;   
        font-size: 16px !important;    
        letter-spacing: 0.3px;
    }

    /* Selected item highlight */

    section[data-testid="stSidebar"] .css-1d391kg {
        background: rgba(255,255,255,0.15) !important;
        border-radius:8px;
    }

    /* Sidebar buttons */

    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(90deg,#7b61ff,#e91e63) !important;
        color: white !important;
        border-radius:16px;
    }

    /* ================= SELECTBOX ================= */

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #cccccc !important;
        border-radius:10px !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {
        color:#000000 !important;
        font-weight:600 !important;
        -webkit-text-fill-color:#000000 !important;
    }

    div[data-baseweb="select"] input::placeholder {
        color:#000000 !important;
        opacity:0.7 !important;
    }

    div[data-baseweb="select"] svg {
        fill:#000000 !important;
    }

    /* ================= TEXTAREA ================= */

    textarea {
        color:black !important;
        background:#f4f6ff !important;
        border-radius:14px;
        border:2px solid #e91e63 !important;
        font-family:Consolas,monospace;
    }

    /* ================= BUTTON ================= */

    .stButton > button {
        background:linear-gradient(90deg,#7b61ff,#e91e63);
        color:white;
        border-radius:18px;
        padding:10px 28px;
        border:none;
        font-weight:600;
    }

    /* ================= DOWNLOAD BUTTON FIX ================= */

    div[data-testid="stDownloadButton"] > button {
        background: linear-gradient(90deg,#7b61ff,#e91e63) !important;
        color: white !important;
        border-radius: 18px !important;
        padding: 10px 26px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
    }

    div[data-testid="stDownloadButton"] > button:hover {
        transform: scale(1.05);
        opacity: 0.9;
    }

    /* ================= SUCCESS FORCE WHITE ================= */

    div[data-testid="stSuccess"] * {
        color: #ffffff !important;
    }

    div[data-testid="stSuccess"] {
        background: rgba(255,255,255,0.15) !important;
        border: 2px solid rgba(255,255,255,0.4) !important;
        border-radius:12px;
        font-weight:600;
    }

    /* ================= WARNING ================= */

    div[data-testid="stWarning"] {
        background: rgba(255,193,7,0.15) !important;
        border: 2px solid #ffc107 !important;
        color:#ffc107 !important;
        border-radius:12px;
        font-weight:600;
    }

    /* ================= QUIZ RADIO BUTTON TEXT WHITE ================= */

    div[role="radiogroup"] label {
        color: #ffffff !important;
        font-size: 16px;
        font-weight: 600;
    }

    div[data-testid="stRadio"] * {
        color: white !important;
    }

    div[role="radiogroup"] svg {
        fill: white !important;
        stroke: white !important;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.12);
        border-radius: 8px;
        padding: 4px;
    }

    </style>
    """, unsafe_allow_html=True)
