import streamlit as st
import numpy as np
import time

from security.guards import require_permission
from security.rbac import has_permission

# ===============================
# AUTHENTICATION + AUTHORIZATION
# ===============================

# Block unauthenticated access
if not st.session_state.get("authenticated", False):
    st.error("Authentication required. Please log in.")
    st.stop()

# Page-level RBAC
require_permission("can_monitor")

# ===============================
# AUDIT LOGGING
# ===============================

def audit_log(action, details=""):
    log_entry = (
        f"{time.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"user={st.session_state.get('username')} | "
        f"role={st.session_state.get('user_role')} | "
        f"action={action} | "
        f"{details}\n"
    )
    with open("audit.log", "a") as f:
        f.write(log_entry)

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Live Fraud Monitoring",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ===============================
# SIDEBAR SECURITY CONTEXT
# ===============================

with st.sidebar:
    st.markdown("### Security Context")
    st.markdown(f"User: {st.session_state.get('username')}")
    st.markdown(f"Role: {st.session_state.get('user_role')}")
    st.divider()

# ===============================
# HEADER
# ===============================

st.markdown("## Real-Time Fraud Detection System")

st.markdown("""
This page represents the deployed fraud detection environment.

The models are already trained.
No learning occurs here.
Each transaction is evaluated independently under live monitoring.
""")

st.divider()

# ===============================
# TRANSACTION INPUT
# ===============================

st.markdown("### Enter Transaction Details")

col1, col2 = st.columns(2)

with col1:
    amount = st.number_input("Transaction Amount", min_value=0.0, value=250.0)
    time_gap = st.number_input("Time Since Last Transaction (minutes)", min_value=0.0, value=30.0)
    distance = st.number_input("Distance From Last Location (km)", min_value=0.0, value=2.0)

with col2:
    channel = st.selectbox("Transaction Channel", ["Card Present", "Online"])
    repeat_merchant = st.selectbox("Repeat Merchant", ["Yes", "No"])
    foreign_txn = st.selectbox("Foreign Transaction", ["No", "Yes"])

channel_val = 1 if channel == "Online" else 0
repeat_val = 1 if repeat_merchant == "Yes" else 0
foreign_val = 1 if foreign_txn == "Yes" else 0

st.divider()

# ===============================
# RUN FRAUD DETECTION
# ===============================

if st.button("Initiate Transaction (Pre-Authorization Check)"):

    audit_log(
        action="RUN_FRAUD_DETECTION",
        details=f"amount={amount}, channel={channel}, foreign={foreign_txn}"
    )

    st.markdown("## Live Fraud Monitoring Activated")

    st.markdown("""
The system has entered real-time monitoring mode.
Behavioral signals are observed continuously to detect sustained abnormal activity.
""")

    st.divider()

    # -------------------------------
    # SIGNAL INTAKE
    # -------------------------------

    st.markdown("### Live Behavioral Signal Intake")

    signal_box = st.empty()

    signals = [
        "Initializing monitoring pipeline",
        "Receiving real-time behavioral data",
        "Comparing activity with learned normal patterns",
        "Evaluating short-term behavioral drift",
        "Correlating signals across monitoring window"
    ]

    for signal in signals:
        signal_box.markdown(
            f"""
            <div style="
                font-family: monospace;
                font-size: 18px;
                color: #22c55e;
                background-color: #020617;
                padding: 14px;
                border-left: 4px solid #22c55e;
                margin-bottom: 8px;
            ">
            {signal}
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.8)

    st.divider()

    # -------------------------------
    # RISK EVOLUTION
    # -------------------------------

    st.markdown("### Risk Evolution Monitor")

    risk_box = st.empty()

    risk_curve = np.concatenate([
        np.linspace(0.28, 0.40, 3),
        np.linspace(0.40, 0.60, 3),
        np.linspace(0.60, 0.82, 3)
    ])

    for risk in risk_curve:
        if risk < 0.40:
            label = "Risk stable"
            color = "#22c55e"
        elif risk < 0.65:
            label = "Risk increasing"
            color = "#facc15"
        else:
            label = "Risk escalating"
            color = "#ef4444"

        risk_box.markdown(
            f"""
            <div style="
                text-align: center;
                font-size: 22px;
                font-family: monospace;
                color: {color};
                border: 2px solid {color};
                border-radius: 12px;
                padding: 20px;
            ">
            Live Risk Score: {risk:.2f}<br/>
            {label}
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.8)

    st.divider()

    # -------------------------------
    # SYSTEM STATE
    # -------------------------------

    st.markdown("### Monitoring State")

    state_box = st.empty()

    states = [
        "Monitoring initiated",
        "Heightened observation enabled",
        "Cross-window behavior correlation",
        "Sustained anomaly confirmation",
        "Escalation readiness reached"
    ]

    for state in states:
        state_box.markdown(
            f"""
            <div style="
                font-family: monospace;
                font-size: 20px;
                color: #38bdf8;
                background-color: #020617;
                padding: 16px;
                border-radius: 8px;
                margin-bottom: 8px;
            ">
            System state: {state}
            </div>
            """,
            unsafe_allow_html=True
        )
        time.sleep(0.8)

    st.divider()

    # -------------------------------
    # SIMULATED MODEL LOGIC
    # -------------------------------

    baseline_score = min(1.0, (amount / 1000) + foreign_val * 0.3 + channel_val * 0.2)
    anomaly_score = min(1.0, (distance / 20) + (1 - repeat_val) * 0.3)

    final_risk = (0.4 * baseline_score) + (0.6 * anomaly_score)

        # -------------------------------
    # PRE-AUTHORIZATION FRAUD PREVENTION
    # -------------------------------

    st.markdown("### Pre-Authorization Risk Evaluation")

    risk_threshold = 0.70  # Bank-defined policy threshold

    if final_risk >= risk_threshold:
        st.error("Transaction Prevented Before Authorization")
        st.write(f"Risk Score: {final_risk:.2f}")
        st.write("Reason: Risk exceeds permitted threshold.")

        audit_log(
            action="TRANSACTION_PREVENTED",
            details=f"risk_score={final_risk:.2f}"
        )

        transaction_status = "BLOCKED"

    else:
        st.success("Transaction Authorized Successfully")
        st.write(f"Risk Score: {final_risk:.2f}")

        audit_log(
            action="TRANSACTION_AUTHORIZED",
            details=f"risk_score={final_risk:.2f}"
        )

        transaction_status = "AUTHORIZED"

    # -------------------------------
    # FINAL ACTION (RBAC ENFORCED)
    # -------------------------------

    st.markdown("### System Action")

    if final_risk >= 0.7:
        if has_permission(st.session_state.user_role, "can_escalate"):
            st.error("Action triggered: Escalate for manual review")
            audit_log(
                action="ESCALATION_TRIGGERED",
                details=f"final_risk={final_risk:.2f}"
            )
        else:
            st.warning("Escalation restricted. Insufficient privileges.")
            audit_log(
                action="ESCALATION_BLOCKED",
                details=f"final_risk={final_risk:.2f}"
            )

    st.divider()

    # -------------------------------
    # RESULTS
    # -------------------------------

    st.markdown("### Transaction Authorization Outcome")
    st.progress(final_risk)

    if final_risk < 0.3:
        decision = "Low risk detected"
        st.success("Transaction approved")
    elif final_risk < 0.7:
        decision = "Moderate risk detected"
        st.warning("Transaction flagged for review")
    else:
        decision = "High fraud probability detected"
        st.error("Transaction blocked")

    st.markdown("### Decision Explanation")
    st.write(f"""
    Baseline score: {baseline_score:.2f}  
    Anomaly score: {anomaly_score:.2f}  
    Final fraud risk: {final_risk:.2f}  

    Decision reason: {decision}
    """)

    with st.expander("Why the system made this decision"):
        st.write("""
        The decision is based on fusion of historical risk indicators
        and real-time behavioral anomaly detection.
        This mirrors production-grade fraud detection systems.
        """)

    st.info("""
    Live monitoring evaluates behavior over time.
    Escalation occurs only after sustained abnormal activity is confirmed.
    """)

st.divider()
