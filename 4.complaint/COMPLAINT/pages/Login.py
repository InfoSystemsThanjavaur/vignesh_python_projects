import streamlit as st

st.title("🔐 Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "admin123":
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success("Login Successful!")
        st.switch_page("Dashboard.py")
    else:
        st.error("Invalid login details!")