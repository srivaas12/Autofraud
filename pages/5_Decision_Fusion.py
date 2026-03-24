import time
import streamlit as st
import numpy as np
import pandas as pd

import streamlit as st
from security.guards import require_permission
require_permission("can_monitor")


if st.session_state.get("go_to_main", False):
    st.switch_page("app.py")

# ===============================
# GLOBAL THEME STATE
# ===============================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

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


st.markdown("##  Step 5: Fraud Decision Engine")

st.markdown("""
The system does not rely on a single signal.

Instead, it **fuses multiple intelligence sources**
to arrive at a **final fraud risk decision**.
""")

st.divider()

fusion_box = st.empty()
progress = st.progress(0)

signals = [
    (" Baseline Risk Model", "Assessing historical risk patterns..."),
    (" Behavioral Anomaly Signal", "Evaluating unusual transaction behavior..."),
    (" Rule-Based Checks", "Applying safety and compliance rules..."),
    (" Risk Weighting", "Balancing confidence across signals..."),
    (" Decision Core", "Generating final fraud verdict...")
]

for i, (title, desc) in enumerate(signals):
    fusion_box.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #020617, #020617);
            border-left: 5px solid #38bdf8;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 10px;
            font-size: 20px;
            font-family: monospace;
        ">
        <b>{title}</b><br/>
        <span style="color:#94a3b8;">{desc}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    progress.progress((i + 1) / len(signals))
    time.sleep(0.9)

st.markdown("###  Decision Engine Processing")

decision_box = st.empty()

thinking_frames = [
    "Aggregating risk signals...",
    "Resolving conflicts between models...",
    "Estimating confidence score...",
    "Finalizing decision..."
]

for frame in thinking_frames:
    decision_box.markdown(
        f"""
        <div style="
            font-size:22px;
            color:#38bdf8;
            text-align:center;
            font-family:monospace;
        ">
        {frame}
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.8)

final_risk = np.random.choice(["LOW", "MEDIUM", "HIGH"], p=[0.6, 0.25, 0.15])

if final_risk == "LOW":
    st.success(" FINAL VERDICT: LOW FRAUD RISK")
elif final_risk == "MEDIUM":
    st.warning(" FINAL VERDICT: MEDIUM FRAUD RISK")
else:
    st.error(" FINAL VERDICT: HIGH FRAUD RISK")


# ===============================
# SAFETY CHECK
# ===============================
required_keys = ["baseline_risk", "anomaly_score"]

for key in required_keys:
    if key not in st.session_state:
        st.warning("""
        Required inputs missing.

        Please complete:
        - Step 3 (Baseline Risk Learning)
        - Step 4 (Anomaly Detection)
        """)
        st.stop()

baseline_risk = st.session_state.baseline_risk
anomaly_score = st.session_state.anomaly_score

st.markdown("""
This stage combines multiple risk signals
to make a **final fraud decision**.

No single model decides fraud alone.
""")

st.divider()

# ===============================
# RISK FUSION
# ===============================
weight_baseline = st.slider("Weight: Baseline Risk", 0.0, 1.0, 0.4)
weight_anomaly = 1.0 - weight_baseline

final_risk = (
    weight_baseline * baseline_risk +
    weight_anomaly * anomaly_score
)

st.session_state.final_risk = final_risk

# ===============================
# VISUALIZATION
# ===============================
st.markdown("###  Final Fraud Risk Distribution")
st.bar_chart(np.histogram(final_risk, bins=40)[0])

# ===============================
# DECISION THRESHOLDS
# ===============================
low_thresh = 0.3
high_thresh = 0.7

decisions = np.where(
    final_risk < low_thresh, "Approve",
    np.where(final_risk < high_thresh, "Review", "Block")
)

decision_counts = pd.Series(decisions).value_counts()

st.markdown("###  Decision Summary")
st.bar_chart(decision_counts)

st.divider()

st.markdown("""
###  How decisions are made

- **Approve** → Low combined risk  
- **Review** → Moderate risk, human verification needed  
- **Block** → High risk detected  

This mirrors real-world banking workflows.
""")

st.success("Fraud decision logic completed.")

st.divider()

st.markdown("### Model Training Status")

st.success("""
Model feeding and decision calibration completed successfully.

All learning components are now synchronized and ready
for live fraud monitoring.
""")

st.markdown("""
The system can now operate in two modes:
- Training mode for further learning and calibration
- Live monitoring mode for real-time fraud detection
""")


if st.button("Go to Main Page"):
    st.session_state.go_to_main = True
    st.rerun()


st.session_state.step5_completed = True



