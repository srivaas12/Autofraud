import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
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


st.markdown("## Step 2: Data Preprocessing Engine")

if "df" not in st.session_state:
    st.warning("Please upload a dataset in Step 1 first.")
    st.stop()

df = st.session_state.df.copy()

# ===============================
# Feature / Target Separation
# ===============================
if "Class" in df.columns:
    X = df.drop(columns=["Class"]).select_dtypes(include=np.number)
    st.session_state.y = df["Class"]
else:
    X = df.select_dtypes(include=np.number)
    st.session_state.y = None

st.session_state.feature_names = list(X.columns)

# ===============================
# Raw Distribution
# ===============================
st.markdown("### Raw Feature Distribution")
feature = st.selectbox("Select feature", X.columns)
st.bar_chart(np.histogram(X[feature], bins=40)[0])

# ===============================
# Scaling
# ===============================
with st.spinner("Normalizing feature space..."):
    time.sleep(1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)

st.session_state.X_scaled = X_scaled_df
st.session_state.scaler = scaler

# ===============================
# After Scaling
# ===============================
st.markdown("### After Scaling")
st.bar_chart(
    np.histogram(X_scaled_df[feature], bins=40)[0]
)

# ===============================
# PCA Visualization
# ===============================
st.markdown("### Feature Geometry (PCA)")
sample = min(1000, len(X_scaled_df))
pca = PCA(n_components=2)
proj = pca.fit_transform(X_scaled_df.iloc[:sample])

st.scatter_chart(
    pd.DataFrame(proj, columns=["PC1", "PC2"])
)

# ===============================
# Explanation
# ===============================
st.markdown("""
**Why preprocessing is critical**

- Machine learning models are sensitive to feature scale  
- Without normalization, distance-based logic becomes unreliable  
- This step ensures all features contribute fairly
""")

st.success("Preprocessing complete. Data ready for modeling.")

if st.button(" Continue to Step 3: Supervised Model"):
    st.switch_page("pages/3_Supervised_Model.py")
