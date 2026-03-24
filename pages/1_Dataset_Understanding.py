import streamlit as st
import pandas as pd
import numpy as np

# ===============================
# PAGE SETUP
# ===============================
st.markdown("##  Step 1: Dataset Upload & Understanding")

st.markdown("""
Before building any fraud detection model,  
we first need to understand **what kind of data we are working with**.

This step focuses on **observing**, not predicting.
""")

st.divider()

# ===============================
# DATASET UPLOAD
# ===============================
uploaded_file = st.file_uploader(
    "Upload a transaction dataset (CSV format)",
    type=["csv"]
)

if uploaded_file is None:
    st.info("Please upload a CSV file to begin.")
    st.stop()

# Load dataset
df = pd.read_csv(uploaded_file)
st.session_state.df = df

st.success("Dataset uploaded successfully.")

st.divider()

# ===============================
# BASIC OVERVIEW
# ===============================
st.markdown("###  Dataset Overview")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Transactions", f"{df.shape[0]:,}")
    st.metric("Total Columns", df.shape[1])

with col2:
    st.markdown("**Column Names**")
    st.write(list(df.columns))

st.markdown("###  Sample Records")
st.dataframe(df.head(10), use_container_width=True)

st.divider()

# ===============================
# DATASET CHARACTER ANALYSIS
# ===============================
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
has_labels = "Class" in df.columns

fraud_ratio = None
if has_labels:
    fraud_ratio = df["Class"].mean() * 100

st.markdown("###  What the system understands from this dataset")

with st.expander(
    " How this dataset will be processed in the next steps",
    expanded=True
):
    st.markdown(f"""
    **Basic Characteristics**
    - Total records: **{df.shape[0]:,}**
    - Numeric features usable for modeling: **{len(numeric_cols)}**
    """)

    if has_labels:
        st.markdown(f"""
        **Fraud Labels Detected**
        - Target column: `Class`
        - Fraud rate: **{fraud_ratio:.2f}%**

         In the next stage, the system will **train a supervised model**
        to learn patterns from known fraud cases.
        """)
    else:
        st.markdown("""
        **No Fraud Labels Detected**

         The system will **not stop or fail**.
        Instead, it will learn **baseline risk behavior**
        from transaction patterns using unsupervised techniques.
        """)

    st.markdown("""
    ---
    **How the pipeline will proceed**

    **Step 2 – Data Preprocessing**
    - Numeric features will be normalized
    - Scale differences will be removed
    - This prevents certain features from dominating learning

    **Step 3 – Baseline Risk Learning**
    - If labels exist → supervised fraud learning
    - If labels do not exist → unsupervised risk modeling

    **Step 4 – Anomaly Detection**
    - Learns what *normal transactions* look like
    - Flags unusual or rare behavior

    **Step 5 – Decision Engine**
    - Combines multiple risk signals
    - Produces a final fraud risk score

    **Step 6 – Live Fraud Detection**
    - Uses trained logic only
    - Evaluates transactions one at a time
    - No dataset required
    """)

st.caption(
    "The pipeline adapts automatically based on the dataset characteristics."
)

st.divider()

# ===============================
# NAVIGATION
# ===============================
if st.button("Continue to Step 2: Data Preprocessing"):
    st.switch_page("pages/2_Preprocessing_Engine.py")
