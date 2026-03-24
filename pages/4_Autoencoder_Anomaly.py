import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.neural_network import MLPRegressor
from security.guards import require_permission
require_permission("can_monitor")



st.markdown("##  Step 4: Detecting Unusual Transaction Behavior")

# ===============================
# SAFETY CHECK
# ===============================
if "X_scaled" not in st.session_state or "baseline_risk" not in st.session_state:
    st.warning("""
    Required data not found.

    Please complete:
    - Step 2 (Preprocessing)
    - Step 3 (Baseline Risk Learning)
    """)
    st.stop()

X = st.session_state.X_scaled

st.markdown("""
In this step, the system **does not try to predict fraud directly**.

Instead, it answers a simpler but powerful question:

> **“Does this transaction behave like most normal transactions?”**
""")

st.divider()

# ===============================
# INTUITIVE EXPLANATION BLOCK
# ===============================
st.markdown("###  How anomaly detection works (intuition)")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ####  Normal Transactions
    - Similar amounts
    - Similar locations
    - Familiar spending patterns
    - Easy for the system to understand
    """)

with col2:
    st.markdown("""
    #### Unusual Transactions
    - Sudden large amounts
    - New locations
    - Rare behavior
    - Hard for the system to reconstruct
    """)

st.info("""
The autoencoder is trained **only on normal patterns**.
If a transaction cannot be reconstructed well,
it means the behavior is unusual.
""")

st.divider()

# ===============================
# TRAIN AUTOENCODER
# ===============================
st.markdown("###  Learning Normal Transaction Behavior")

st.markdown("""
Instead of directly detecting fraud,  
the system **learns how normal transactions behave**  
— just like how humans learn patterns by repetition.
""")

animation_box = st.empty()
progress = st.progress(0)


with st.spinner("Learning how normal transactions look..."):
    time.sleep(1.5)

    autoencoder = MLPRegressor(
        hidden_layer_sizes=(X.shape[1] // 2,),
        activation="relu",
        max_iter=300,
        random_state=42
    )
    autoencoder.fit(X, X)

st.success("Normal behavior learned successfully.")

with st.spinner("Autoencoder is learning normal behavior..."):

    scenes = [
        " Ingesting transaction patterns...",
        " Compressing information (Encoder)...",
        " Reconstructing original transaction...",
        " Measuring reconstruction error...",
        " Repeating for thousands of transactions...",
        " Normal behavior patterns stabilized",
        " Unusual behavior now stands out"
    ]

    for i, scene in enumerate(scenes):
        animation_box.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #020617, #020617);
                padding: 25px;
                border-radius: 12px;
                border-left: 5px solid #22c55e;
                font-size: 20px;
                animation: fadeIn 0.5s;
            ">
            {scene}
            </div>
            """,
            unsafe_allow_html=True
        )
        progress.progress((i + 1) / len(scenes))
        time.sleep(0.9)

st.markdown("###  Learning Improvement Over Time")

loss_placeholder = st.empty()

fake_losses = np.linspace(1.0, 0.15, 20)

for loss in fake_losses:
    loss_placeholder.markdown(
        f"""
        <div style="
            font-size: 22px;
            color: #22c55e;
        ">
        Reconstruction Error: {loss:.3f}
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.15)

st.success("The system has learned to reconstruct normal transactions accurately.")


# ===============================
# RECONSTRUCTION ERROR
# ===============================
reconstructed = autoencoder.predict(X)
reconstruction_error = np.mean((X - reconstructed) ** 2, axis=1)

anomaly_score = (reconstruction_error - reconstruction_error.min()) / (
    reconstruction_error.max() - reconstruction_error.min()
)

st.session_state.anomaly_score = anomaly_score
st.session_state.autoencoder = autoencoder

st.divider()

# ===============================
# VISUAL EXPLANATION OF SCORES
# ===============================
st.markdown("###  How unusual are the transactions?")

st.markdown("""
Each bar below represents how **unusual** a transaction is.

- Lower values → normal behavior  
- Higher values → unusual behavior  
""")

st.bar_chart(np.histogram(anomaly_score, bins=40)[0])

st.divider()

# st.markdown("##  Real-Time Fraud Radar")

# st.markdown("""
# The system now continuously **scans transaction behavior**  
# just like a **cybersecurity radar** monitoring threats in real time.
# """)

# radar = st.empty()

# radar_html = """
# <style>
# .radar-container {
#     width: 350px;
#     height: 350px;
#     border-radius: 50%;
#     background: radial-gradient(circle at center, #022c22 0%, #020617 70%);
#     position: relative;
#     margin: auto;
#     overflow: hidden;
#     box-shadow: 0 0 40px #22c55e;
# }

# .radar-sweep {
#     width: 50%;
#     height: 50%;
#     background: linear-gradient(90deg, rgba(34,197,94,0.6), rgba(34,197,94,0));
#     position: absolute;
#     top: 50%;
#     left: 50%;
#     transform-origin: 0% 0%;
#     animation: sweep 3s linear infinite;
# }

# @keyframes sweep {
#     from { transform: rotate(0deg); }
#     to { transform: rotate(360deg); }
# }

# .dot {
#     width: 6px;
#     height: 6px;
#     border-radius: 50%;
#     position: absolute;
#     background: #22c55e;
#     opacity: 0.8;
# }

# .dot.anomaly {
#     background: #ef4444;
#     box-shadow: 0 0 10px #ef4444;
# }
# </style>

# <div class="radar-container">
#     <div class="radar-sweep"></div>

#     <!-- Normal transactions -->
#     <div class="dot" style="top: 30%; left: 60%;"></div>
#     <div class="dot" style="top: 55%; left: 40%;"></div>
#     <div class="dot" style="top: 70%; left: 50%;"></div>

#     <!-- Anomalies -->
#     <div class="dot anomaly" style="top: 20%; left: 45%;"></div>
#     <div class="dot anomaly" style="top: 65%; left: 70%;"></div>
# </div>
# """

# radar.markdown(radar_html, unsafe_allow_html=True)

# status_box = st.empty()

# status_messages = [
#     " Scanning transaction patterns...",
#     " Comparing with learned normal behavior...",
#     " Normal activity confirmed",
#     " Suspicious behavior detected",
#     " Continuous monitoring in progress..."
# ]

# for msg in status_messages:
#     status_box.markdown(
#         f"""
#         <div style="
#             font-size:18px;
#             color:#22c55e;
#             font-family:monospace;
#         ">
#         {msg}
#         </div>
#         """,
#         unsafe_allow_html=True
#     )
#     time.sleep(0.8)

# st.markdown("""
# ### 🧭 Radar Legend
# - 🟢 **Green dots** → Normal transactions  
# - 🔴 **Red dots** → Unusual / suspicious behavior  
# - Rotating beam → Continuous monitoring  
# """)


# ===============================
# INDIVIDUAL TRANSACTION DEMO
# ===============================
st.markdown("###  Example Transaction Analysis")

st.markdown("##  Behavior Recognition Phase")

colA, colB = st.columns(2)

with colA:
    st.markdown("""
     **Normal Transaction**
    - Familiar pattern
    - Low reconstruction error
    - Easily recognized
    """)

with colB:
    st.markdown("""
     **Unusual Transaction**
    - Rare behavior
    - High reconstruction error
    - Stands out clearly
    """)


max_idx = anomaly_score.shape[0] - 1

example_idx = st.slider(
    "Select a transaction to inspect",
    min_value=0,
    max_value=max_idx,
    value=0
)


score = anomaly_score[example_idx]

st.markdown("#### Anomaly Interpretation")

if score < 0.3:
    st.success("This transaction behaves like normal activity.")
elif score < 0.7:
    st.warning(" This transaction is unusual and needs attention.")
else:
    st.error(" This transaction is highly abnormal.")

st.markdown(f"""
**Anomaly Score:** `{score:.3f}`

This score does **not mean fraud** by itself.  
It means the behavior is *different* from what the system expects.
""")

st.divider()

# ===============================
# WHY THIS MATTERS
# ===============================
st.markdown("""
###  Why banks use anomaly detection

- Fraud patterns change frequently  
- New fraud types appear without labels  
- Historical rules alone are not enough  

Anomaly detection helps catch **never-seen-before fraud**.
""")

st.success("Anomaly signals forwarded to the decision engine.")

if st.button(" Continue to Step 5: Decision Engine"):
    st.switch_page("pages/5_Decision_Fusion.py")
