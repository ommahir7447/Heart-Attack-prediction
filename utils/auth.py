import streamlit as st
from utils.clerk_auth import clerk_signin, clerk_signup

_COOKIE_NAME = "hg_session_email"
_COOKIE_EXPIRY_DAYS = 30


def get_cookie_manager():
    """Returns a CookieManager — call at module/app top level, not inside cached fns."""
    import extra_streamlit_components as stx
    return stx.CookieManager(key="hg_cookie_mgr")


def _get_cm():
    """Retrieve the single app-level CookieManager stored in session_state."""
    return st.session_state.get("_hg_cookie_mgr")


def login_user(email, password):
    """Authenticate via Clerk and set session state."""
    success, msg, user_data = clerk_signin(email, password)
    if success and user_data:
        st.session_state.logged_in = True
        st.session_state.user = user_data["name"]
        st.session_state.user_email = user_data["email"]
        # Persist login via cookie
        try:
            from datetime import datetime, timedelta
            cm = _get_cm()
            if cm:
                cm.set(_COOKIE_NAME, email,
                       expires_at=datetime.now() + timedelta(days=_COOKIE_EXPIRY_DAYS))
        except Exception:
            pass
        return True, msg
    return False, msg


def signup_user(name, email, password, confirm_password):
    """Create account via Clerk."""
    if password != confirm_password:
        return False, "Passwords do not match!"
    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    success, msg, _ = clerk_signup(name, email, password)
    return success, msg


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_email = None
    try:
        cm = _get_cm()
        if cm:
            cm.delete(_COOKIE_NAME)
    except Exception:
        pass


def restore_session_from_cookie():
    """Call once at app startup to auto-login from a saved cookie."""
    if st.session_state.get("logged_in"):
        return
    try:
        cm = _get_cm()
        if not cm:
            return
        saved_email = cm.get(_COOKIE_NAME)
        if saved_email:
            # We trust the cookie — Clerk already verified credentials at login time
            st.session_state.logged_in = True
            st.session_state.user_email = saved_email
            # Try to get the name from Clerk
            try:
                from utils.clerk_auth import _get_clerk_client
                clerk = _get_clerk_client()
                users = list(clerk.users.list(email_address=[saved_email]))
                if users:
                    u = users[0]
                    st.session_state.user = f"{u.first_name or ''} {u.last_name or ''}".strip() or saved_email.split("@")[0]
                else:
                    st.session_state.user = saved_email.split("@")[0]
            except Exception:
                st.session_state.user = saved_email.split("@")[0]
    except Exception:
        pass
