import streamlit as st
from database import check_user

st.title("Login to Your Account")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Login")

    if submit_button:
        if check_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome back, {username}!")
            st.info("You can now access the 'Dashboard' from the sidebar.")
        else:
            st.error("Incorrect username or password.")