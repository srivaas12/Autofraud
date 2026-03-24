import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
import time

import streamlit as st
from security.guards import require_permission
require_permission("can_train")

# ===============================
# GLOBAL THEME STATE
# ===============================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# ===============================
# THEME TOGGLE (SIDEBAR)
# ===============================
with st.sidebar:
    st.markdown("### 🎨 Theme")
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


st.markdown("##  Step 3: Baseline Risk Learning")

# ===============================
# SAFETY CHECK
# ===============================
if "X_scaled" not in st.session_state:
    st.warning("""
    Preprocessed data not found.

    This step depends on Step 2.
    Please complete preprocessing first.
    """)
    st.stop()

X = st.session_state.X_scaled
y = st.session_state.y

st.markdown("""
At this stage, the system learns **baseline risk patterns**.

This step always runs, but the learning strategy depends on
whether fraud labels are available.
""")

st.divider()

# ===============================
# MODE SELECTION
# ===============================
if y is None:
    # -------------------------------------------------
    # UNLABELED MODE (MOST REALISTIC CASE)
    # -------------------------------------------------
    st.subheader("Unlabeled Dataset Detected")
    st.markdown("""
    Fraud labels are not available.

    Instead of skipping learning, the system models **normal transaction behavior**
    and assigns a **risk score** to each transaction.
    """)

    with st.spinner("Learning baseline transaction risk patterns..."):
        time.sleep(1)
        model = IsolationForest(
            n_estimators=150,
            contamination=0.05,
            random_state=42
        )
        model.fit(X)

    # Higher score = higher risk
    risk_scores = -model.decision_function(X)
    risk_scores = (risk_scores - risk_scores.min()) / (
        risk_scores.max() - risk_scores.min()
    )

    st.session_state.baseline_risk = risk_scores
    st.session_state.baseline_model = model
    st.session_state.baseline_mode = "unsupervised"

    st.success("Baseline risk model trained successfully.")

    # -------------------------------
    # VISUALIZATION
    # -------------------------------
    st.markdown("###  Baseline Risk Distribution")
    st.bar_chart(np.histogram(risk_scores, bins=40)[0])

    st.markdown("""
    **Interpretation**

    Most transactions appear low-risk.
    A smaller subset deviates from typical behavior and is treated as higher risk.
    """)

else:
    # -------------------------------------------------
    # LABELED MODE
    # -------------------------------------------------
    st.subheader(" Labeled Dataset Detected")
    st.markdown("""
    Fraud labels are available.

    The system trains a supervised model
    to learn known fraud patterns.
    """)

    with st.spinner("Training supervised fraud classifier..."):
        time.sleep(1)
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)

    fraud_prob = model.predict_proba(X)[:, 1]

    st.session_state.baseline_risk = fraud_prob
    st.session_state.baseline_model = model
    st.session_state.baseline_mode = "supervised"

    st.success("Supervised fraud model trained successfully.")

    # -------------------------------
    # VISUALIZATION
    # -------------------------------
    st.markdown("###  Fraud Probability Distribution")
    st.bar_chart(np.histogram(fraud_prob, bins=40)[0])

    st.markdown("""
    **Interpretation**

    Transactions with higher predicted probabilities
    are more likely to be fraudulent based on historical patterns.
    """)

st.divider()

# ===============================
# HUMAN EXPLANATION
# ===============================
st.markdown("""
###  Why this step matters

Real-world fraud systems cannot rely on labels alone.

This step provides a **baseline risk signal** that:
- Captures known fraud (when labels exist)
- Captures suspicious behavior (when labels do not)

This signal is later combined with anomaly detection
to make the final decision.
""")

st.success("Baseline risk signal forwarded to next stage.")

if st.button(" Continue to Step 4: Anomaly Detection"):
    st.switch_page("pages/4_Autoencoder_Anomaly.py")
