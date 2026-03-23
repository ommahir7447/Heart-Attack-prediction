import streamlit as st
import bcrypt
from utils.db import get_users_collection

def login_user(email, password):
    users_collection = get_users_collection()
    user = users_collection.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        st.session_state.logged_in = True
        st.session_state.user = user.get('name', email.split('@')[0])
        st.session_state.user_email = email
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
