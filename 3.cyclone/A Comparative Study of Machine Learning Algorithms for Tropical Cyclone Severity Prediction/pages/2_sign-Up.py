import streamlit as st
from database import add_user

st.title("Create a New Account")

with st.form("signup_form"):
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        if new_username and new_password:
            if add_user(new_username, new_password):
                st.success("Account created successfully! Please login.")
            else:
                st.error("This username is already taken. Please choose another one.")
        else:
            st.warning("Please fill out all fields.")