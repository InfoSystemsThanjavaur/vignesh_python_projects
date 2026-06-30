import streamlit as st
import sqlite3
import pickle
import pandas as pd
from xgboost import XGBClassifier
import joblib

rf_model = joblib.load("rf_model.pkl")
svm_model = joblib.load("svm_model.pkl")

xgb_model = XGBClassifier()
xgb_model.load_model("stress_model.json")

# ==========================
# Page Config
# ==========================
st.set_page_config(page_title="Stress Detection System", layout="wide")

# ==========================
# Custom CSS (Modern UI)
# ==========================
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1, h2, h3 {
    color: #FFFFFF;
}
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
}
.stTextInput>div>div>input {
    background-color: #1E1E1E;
    color: white;
}
.stSelectbox>div>div {
    background-color: #1E1E1E;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# Load Model
# ==========================
model = XGBClassifier()
model.load_model("stress_model.json")

scaler = pickle.load(open("scaler.pkl", "rb"))
encoders = pickle.load(open("encoders.pkl", "rb"))

# ==========================
# Database
# ==========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)""")
c.execute("""CREATE TABLE IF NOT EXISTS predictions(
    username TEXT, age INTEGER, stress_level TEXT, probability REAL)""")
conn.commit()

# ==========================
# Functions
# ==========================
def add_user(u, p):
    c.execute("INSERT INTO users VALUES (?,?)", (u, p))
    conn.commit()

def login_user(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

def save_prediction(username, age, stress_level, prob):
    c.execute(
        "INSERT INTO predictions VALUES (?,?,?,?)",
        (username, age, stress_level, float(prob))
    )
    conn.commit()
def get_history(u):
    c.execute("SELECT age, stress_level, probability FROM predictions WHERE username=?", (u,))
    return c.fetchall()

# ==========================
# Session State
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================
# TOP NAVIGATION
# ==========================

if not st.session_state.logged_in:
    nav = st.radio("Navigation", ["Home", "About", "Login", "Signup"], horizontal=True)
else:
    nav = st.radio("Navigation", ["Dashboard", "Predict Stress", "History", "Logout"], horizontal=True)

# ==========================
# HOME PAGE
# ==========================
if nav == "Home":

    # Advanced Hero Section
    st.markdown("""
    <style>
    .hero {
        padding: 40px;
        border-radius: 15px;
        background: linear-gradient(135deg, #1f1c2c, #928dab);
        text-align: center;
        color: white;
    }
    .feature-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        margin-top: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <h1>🧠 Automated Stress Detection System</h1>
        <h4>AI-Powered Behavioral Stress Prediction for IT Professionals</h4>
        <p>
        A machine learning driven platform designed to detect stress levels 
        using behavioral indicators, probability-based classification, 
        and predictive analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Accuracy Highlight Section
    col1, col2, col3 = st.columns(3)

    col1.metric("Random Forest Accuracy", "93.14%")
    col2.metric("SVM Accuracy", "92.74%")
    col3.metric("XGBoost Accuracy", "91.93%")

    st.write("")

    # Feature Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Behavioral Analysis</h4>
            <p>
            Evaluates workplace indicators including remote work, 
            company benefits, treatment history, and organizational support.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 Machine Learning Engine</h4>
            <p>
            Powered by ensemble learning and gradient boosting algorithms 
            to ensure high prediction accuracy and model stability.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>📈 Probability Risk Scoring</h4>
            <p>
            Provides Low, Medium, and High stress classification 
            based on predicted probability thresholds.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # System Workflow Section
    st.markdown("### 🔄 System Workflow")

    st.markdown("""
    1. User Authentication  
    2. Behavioral Data Input  
    3. Feature Encoding & Scaling  
    4. Machine Learning Prediction  
    5. Probability-Based Stress Classification  
    6. Database Storage & History Tracking  

    This structured workflow ensures secure, accurate, and interpretable 
    stress level predictions.
    """)

    st.write("")

    st.success("🚀 Designed for early stress risk detection in IT professionals.")

# ==========================
# ABOUT PAGE
# ==========================
elif nav == "About":

    st.title("📘 About This Project")

    st.markdown("""
    ### 📌 Project Overview

    The **Automated Stress Detection System for IT Professionals** is an intelligent
    machine learning-based application designed to identify stress levels using 
    behavioral indicators and predictive analytics techniques.

    In modern IT environments, professionals are exposed to high workload,
    tight deadlines, remote work challenges, and work-life imbalance. 
    This system aims to analyze such behavioral attributes and predict
    stress levels in a structured and data-driven manner.

    The model processes user-provided inputs such as age, work environment,
    treatment history, organizational support factors, and mental health indicators
    to generate a probability-based stress classification.
    """)

    st.markdown("---")

    st.markdown("""
    ### 🤖 Machine Learning Algorithms Used

    This project experimented with multiple supervised machine learning models
    to identify the most accurate classifier for stress detection:

    #### 1️⃣ Random Forest Classifier
    Random Forest is an ensemble learning algorithm that builds multiple
    decision trees and merges their outputs to improve predictive accuracy.
    It reduces overfitting and performs well with categorical behavioral features.

    **Achieved Accuracy:** ~93.14%

    #### 2️⃣ Support Vector Machine (SVM)
    SVM works by finding the optimal hyperplane that separates stress
    and non-stress classes in feature space. It is effective for binary
    classification problems with well-separated classes.

    **Achieved Accuracy:** ~92.74%

    #### 3️⃣ XGBoost Classifier (Final Model)
    XGBoost is a powerful gradient boosting algorithm that sequentially
    builds decision trees and minimizes prediction error using boosting
    techniques. It handles feature interactions effectively and improves
    performance through regularization.

    **Achieved Accuracy:** ~91.93%

    After performance comparison, Random Forest demonstrated the highest
    validation accuracy and stability. However, XGBoost was selected
    for deployment due to its scalability and probability prediction capabilities.
    """)

    st.markdown("---")

    st.markdown("""
    ### 📊 Model Performance Evaluation

    The system was evaluated using:

    - Accuracy Score
    - Train-Test Split Validation
    - Probability-based Risk Classification
    - Confusion Matrix Analysis

    The final deployed model achieved approximately **93% prediction accuracy**, 
    indicating strong reliability in stress classification based on 
    behavioral indicators.

    Stress levels are categorized as:

    - 🟢 Low Stress (Probability < 40%)
    - 🟡 Medium Stress (40% – 70%)
    - 🔴 High Stress (> 70%)

    This probability-based approach ensures better interpretability
    and risk-level understanding for end users.
    """)

    st.markdown("---")

    st.markdown("""
    ### 🔐 System Features

    - Secure User Authentication (Login & Signup)
    - Behavioral Feature-Based Stress Prediction
    - Probability-Based Risk Level Classification
    - SQLite Database Storage
    - User Prediction History Tracking
    - Interactive Web Interface using Streamlit
    - Advanced Machine Learning Backend (XGBoost)

    This system can be extended further with sentiment analysis,
    real-time monitoring integration, and dashboard analytics for
    enterprise-level stress management systems.
    """)

    st.success("Developed for stress prediction and early risk detection in IT professionals.")


# ==========================
# SIGNUP
# ==========================
elif nav == "Signup":
    st.subheader("Create New Account")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Signup"):
        add_user(u, p)
        st.success("Account Created Successfully!")

# ==========================
# LOGIN
# ==========================
elif nav == "Login":
    st.subheader("Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(u, p):
            st.session_state.logged_in = True
            st.session_state.username = u
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Credentials")

# ==========================
# DASHBOARD
# ==========================
# ==========================
# DASHBOARD
# ==========================
# ==========================
# DASHBOARD
# ==========================
elif nav == "Dashboard":

    st.title("📊 Dashboard Overview")

    history = get_history(st.session_state.username)

    # If no history at all
    if not history:
        st.info("No predictions available yet. Please use the Predict Stress page.")
    else:

        # Create DataFrame
        df = pd.DataFrame(history, columns=["Age", "Stress Level", "Probability"])

        # Convert Probability safely to numeric
        df["Probability"] = pd.to_numeric(df["Probability"], errors="coerce")

        # Remove invalid rows
        df = df[df["Probability"].notna()]

        if len(df) == 0:
            st.info("No valid prediction data available.")
        else:

            # Convert to percentage
            df["Probability"] = df["Probability"] * 100

            # ==========================
            # KPI METRICS
            # ==========================
            col1, col2, col3 = st.columns(3)

            total_predictions = len(df)
            avg_stress = round(float(df["Probability"].mean()), 2)
            high_stress_count = len(df[df["Stress Level"] == "High Stress"])

            col1.metric("Total Predictions", total_predictions)
            col2.metric("Average Stress Probability", f"{avg_stress}%")
            col3.metric("High Stress Cases", high_stress_count)

            st.markdown("---")

            # ==========================
            # PIE CHART
            # ==========================
            st.subheader("Stress Level Distribution")

            import plotly.express as px

            stress_counts = df["Stress Level"].value_counts()

            fig_pie = px.pie(
                names=stress_counts.index,
                values=stress_counts.values,
                hole=0.4,
                title="Stress Distribution"
            )

            st.plotly_chart(fig_pie, width="stretch")

            st.markdown("---")

            # ==========================
            # LINE CHART
            # ==========================
            st.subheader("Stress Probability Trend")

            df["Record"] = range(1, len(df) + 1)

            fig_line = px.line(
                df,
                x="Record",
                y="Probability",
                markers=True,
                title="Stress Trend Over Time"
            )

            st.plotly_chart(fig_line, width="stretch")

            st.markdown("---")

            # ==========================
            # LATEST PREDICTION
            # ==========================
            st.subheader("Latest Stress Evaluation")

            latest_row = df.iloc[-1]

            latest_level = latest_row["Stress Level"]
            latest_prob = float(latest_row["Probability"])
            latest_age = latest_row["Age"]

            st.info(f"""
            🔹 Latest Stress Level: {latest_level}  
            🔹 Probability: {round(latest_prob,2)}%  
            🔹 Age: {latest_age}
            """)

            st.markdown("---")

            # ==========================
            # RISK INDICATOR
            # ==========================
            st.subheader("Current Risk Indicator")

            st.progress(int(latest_prob))

            if latest_prob < 40:
                st.success("🟢 Low Risk Level")
            elif latest_prob < 70:
                st.warning("🟡 Medium Risk Level")
            else:
                st.error("🔴 High Risk Level")


# ==========================
# PREDICT PAGE
# ==========================
elif nav == "Predict Stress":

    st.title("Stress Prediction Form")

    age = st.slider(
    "Age",
    18, 60, 25,
    help="Select your current age. Age can influence workplace stress patterns.")
    
    gender = st.selectbox(
        "Gender",
        ["male", "female", "other"],
        help="Select your gender identity."
    )
    
    family_history = st.selectbox(
        "Family History",
        ["Yes", "No"],
        help="Do you have a family history of mental health conditions?"
    )
    
    treatment = st.selectbox(
        "Treatment",
        ["Yes", "No"],
        help="Have you ever sought treatment for mental health issues?"
    )
    
    remote_work = st.selectbox(
        "Remote Work",
        ["Yes", "No"],
        help="Do you currently work remotely (fully or partially)?"
    )
    
    tech_company = st.selectbox(
        "Tech Company",
        ["Yes", "No"],
        help="Are you employed in a technology-based company?"
    )
    
    benefits = st.selectbox(
        "Benefits",
        ["Yes", "No", "Don't know"],
        help="Does your employer provide mental health benefits?"
    )
    
    care_options = st.selectbox(
        "Care Options",
        ["Yes", "No", "Not sure"],
        help="Are you aware of care options provided by your employer?"
    )
    
    anonymity = st.selectbox(
        "Anonymity",
        ["Yes", "No", "Don't know"],
        help="Does your employer protect anonymity when discussing mental health?"
    )
    
    leave = st.selectbox(
        "Leave Difficulty",
        ["Very easy", "Somewhat easy", "Somewhat difficult", "Very difficult", "Don't know"],
        help="How easy is it to take leave for mental health reasons in your workplace?"
    )


     # 🔴 EVERYTHING BELOW MUST BE INSIDE BUTTON
    if st.button("Predict Stress"):

        # ---------------------------
        # 1️⃣ Prepare Input
        # ---------------------------
        user_input = pd.DataFrame([{
            'Age': age,
            'Gender': gender,
            'family_history': family_history,
            'treatment': treatment,
            'remote_work': remote_work,
            'tech_company': tech_company,
            'benefits': benefits,
            'care_options': care_options,
            'anonymity': anonymity,
            'leave': leave
        }])

        # Apply encoders
        for col in user_input.columns:
            if col in encoders:
                user_input[col] = encoders[col].transform(user_input[col])

        # Scale input
        user_scaled = scaler.transform(user_input)

        # ---------------------------
        # 2️⃣ Predict with Models
        # ---------------------------
        rf_prob = rf_model.predict_proba(user_scaled)[0][1]
        svm_prob = svm_model.predict_proba(user_scaled)[0][1]
       
        xgb_prob = xgb_model.predict_proba(user_scaled)[0][1]

        rf_percent = round(rf_prob * 100, 2)
        svm_percent = round(svm_prob * 100, 2)
        xgb_percent = round(xgb_prob * 100, 2)

        # ---------------------------
        # 3️⃣ Final Prediction Display
        # ---------------------------
        st.subheader("Final Stress Prediction")

        if xgb_percent < 40:
            level = "Low Stress"
        elif xgb_percent < 70:
            level = "Medium Stress"
        else:
            level = "High Stress"

        st.success(f"Stress Level: {level}")
        st.info(f"Stress Probability: {xgb_percent}%")

        # ---------------------------
        # 4️⃣ Algorithm Comparison
        # ---------------------------
        st.markdown("---")
        st.subheader("📊 Algorithm Comparison")

        col1, col2, col3 = st.columns(3)
        col1.metric("Random Forest", f"{rf_percent}%")
        col2.metric("SVM", f"{svm_percent}%")
        col3.metric("XGBoost (Final)", f"{xgb_percent}%")
        
# ==========================
# HISTORY PAGE
# ==========================
elif nav == "History":

    st.title("Your Prediction History")

    data = get_history(st.session_state.username)

    if data:
        df = pd.DataFrame(data, columns=["Age", "Stress Level", "Probability"])
        df["Probability"] = df["Probability"] * 100
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No previous records found.")        
# ==========================
# LOGOUT
# ==========================
elif nav == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged Out Successfully")
    st.rerun()
