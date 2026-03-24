import streamlit as st
from security.rbac import has_permission

def require_permission(permission):
    role = st.session_state.get("user_role")

    if not role or not has_permission(role, permission):
        st.error("Access denied. You are not authorized to view this page.")
        st.stop()
