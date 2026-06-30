import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 Complaint Monitoring Dashboard")
st.markdown("---")

# Load sample data
df = pd.DataFrame({
    "Complaint": [
        "Street light not working",
        "Garbage not collected",
        "Road full of potholes"
    ],
    "Category": ["Electricity Issue", "Garbage Issue", "Road Issue"],
    "Priority": ["High", "Medium", "High"]
})

tab1, tab2 = st.tabs(["📝 Prediction", "📚 History"])

# ---------------- TAB 1 ----------------
with tab1:
    st.header("📝 Enter Complaint")
    complaint = st.text_area("Complaint Text:", height=150)

    if st.button("Predict Now"):
        st.session_state["complaint_text"] = complaint
        st.switch_page("predict_result.py")

# ---------------- TAB 2 ----------------
with tab2:
    st.header("📚 Complaint History (Sample)")
    st.dataframe(df)