import streamlit as st
from security.rbac import ROLES


st.set_page_config(page_title="Fraud Detection System", layout="wide")

# -------------------------------
# AUTH STATE INITIALIZATION
# -------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None


if not st.session_state.authenticated:
    st.markdown("## Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # DEMO CREDENTIALS (acceptable for academic project)
        users = {
            "admin_user": ("admin", "admin123"),
            "analyst_user": ("analyst", "analyst123"),
            "auditor_user": ("auditor", "auditor123")
        }

        if username in users and password == users[username][1]:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_role = users[username][0]
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()


# ===============================
# GLOBAL THEME STATE
# ===============================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if st.session_state.get("go_to_main", False):
    del st.session_state.go_to_main




# ===============================
# THEME TOGGLE (SIDEBAR)
# ===============================
with st.sidebar:
    st.markdown("###  Theme")
    theme_toggle = st.toggle(
        "Dark Mode",
        value=(st.session_state.theme == "dark")
    )

    st.session_state.theme = "dark" if theme_toggle else "light"


st.set_page_config(
    page_title="AutoFraud Ops",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===============================
# APPLY THEME
# ===============================
if st.session_state.theme == "dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0f172a;
            color: #e5e7eb;
        }

        h1, h2, h3, h4, h5, h6, p, span, label {
            color: #e5e7eb !important;
        }

        .stButton>button {
            background-color: #1e293b;
            color: white;
            border-radius: 8px;
            border: none;
        }

        .stButton>button:hover {
            background-color: #334155;
        }

        .stSidebar {
            background-color: #020617;
        }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #000000;
        }

        h1, h2, h3, h4, h5, h6, p, span, label {
            color: #000000 !important;
        }

        .stSidebar {
            background-color: #f8fafc;
        }
        </style>
    """, unsafe_allow_html=True)


# ===============================
# MAIN HEADER
# ===============================
st.markdown("""
<h1 style='text-align:center;'>AutoFraud Ops</h1>
<h3 style='text-align:center;color:gray;'>
Explainable Fraud Detection System
</h3>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""

""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===============================
# BIG NAVIGATION BUTTONS
# ===============================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div style="
        padding:30px;
        border-radius:18px;
        background:linear-gradient(135deg,#1e3a8a,#2563eb);
        color:white;
        text-align:center;
        box-shadow:0 10px 30px rgba(0,0,0,0.4);
    ">
        <h2> Model Training & Explainability</h2>
        <p>
        Explore dataset understanding, preprocessing,
        supervised learning, anomaly detection,
        and decision logic
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(" Go to Training Pipeline", use_container_width=True):
        st.switch_page("pages/1_Dataset_Understanding.py")

with col2:
    st.markdown("""
    <div style="
        padding:30px;
        border-radius:18px;
        background:linear-gradient(135deg,#065f46,#16a34a);
        color:white;
        text-align:center;
        box-shadow:0 10px 30px rgba(0,0,0,0.4);
    ">
        <h2> Real-Time Fraud Detection</h2>
        <p>
        Use the trained system to
        evaluate real-time transactions
        like a production banking system
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(" Go to Real-Time Detection", use_container_width=True):
        st.switch_page("pages/6_Live_Fraud_Detection.py")

# ===============================
# FOOTER
# ===============================
st.markdown("<br><hr><br>", unsafe_allow_html=True)

st.markdown("""

""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Session")
    st.markdown(f"User: {st.session_state.username}")
    st.markdown(f"Role: {st.session_state.user_role}")

    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()

