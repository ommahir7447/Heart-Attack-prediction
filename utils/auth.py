import streamlit as st
import bcrypt
from utils.db import get_users_collection

_COOKIE_NAME = "hg_session_email"
_COOKIE_EXPIRY_DAYS = 30


def get_cookie_manager():
    """Returns a CookieManager — call at module/app top level, not inside cached fns."""
    import extra_streamlit_components as stx
    return stx.CookieManager(key="hg_cookie_mgr")


def login_user(email, password):
    users_collection = get_users_collection()
    user = users_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        st.session_state.logged_in = True
        st.session_state.user = user.get('name', email.split('@')[0])
        st.session_state.user_email = email
        # Persist login across refreshes via cookie
        try:
            from datetime import datetime, timedelta
            cm = get_cookie_manager()
            cm.set(_COOKIE_NAME, email,
                   expires_at=datetime.now() + timedelta(days=_COOKIE_EXPIRY_DAYS))
        except Exception:
            pass
        return True
    return False


def signup_user(name, email, password, confirm_password):
    users_collection = get_users_collection()
    if password != confirm_password:
        return False, "Passwords do not match!"
    if users_collection.find_one({"email": email}):
        return False, "Email already registered."

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_pw
    })
    return True, "Account created successfully!"


def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_email = None
    # Clear the persistent cookie
    try:
        cm = get_cookie_manager()
        cm.delete(_COOKIE_NAME)
    except Exception:
        pass


def restore_session_from_cookie():
    """Call once at app startup to auto-login from a saved cookie."""
    if st.session_state.get("logged_in"):
        return  # already logged in
    try:
        cm = get_cookie_manager()
        saved_email = cm.get(_COOKIE_NAME)
        if saved_email:
            users_collection = get_users_collection()
            user = users_collection.find_one({"email": saved_email})
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user.get('name', saved_email.split('@')[0])
                st.session_state.user_email = saved_email
    except Exception:
        pass
