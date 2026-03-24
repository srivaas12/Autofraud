import streamlit as st
ROLES = {
    "admin": {
        "can_train": True,
        "can_monitor": True,
        "can_escalate": True,
        "can_view": True
    },
    "analyst": {
        "can_train": False,
        "can_monitor": True,
        "can_escalate": True,
        "can_view": True
    },
    "auditor": {
        "can_train": False,
        "can_monitor": False,
        "can_escalate": False,
        "can_view": True
    }
}

def has_permission(role: str, permission: str) -> bool:
    return ROLES.get(role, {}).get(permission, False)

from security.rbac import has_permission

def require_permission(permission: str):
    role = st.session_state.get("user_role")

    if not role or not has_permission(role, permission):
        st.error("You are not authorized to access this section.")
        st.stop()
