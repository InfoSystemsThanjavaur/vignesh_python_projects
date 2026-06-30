import streamlit as st
import mysql.connector
import joblib
import pandas as pd
from datetime import datetime
import hashlib
import os
import plotly.express as px  
import urllib.parse
import streamlit.components.v1 as components
# Create 'uploads' directory for saving images if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Complaint Portal", page_icon="🏛️", layout="wide")

# --- 2. MYSQL DATABASE CONNECTION SETTINGS ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Update your MySQL username
    'password': 'root',  # Update your MySQL password
    'database': 'complaint_system_db'
}

def get_db_connection():
    temp_conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cursor = temp_conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    temp_conn.commit()
    temp_conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY, 
                    password VARCHAR(255) NOT NULL, 
                    role VARCHAR(20) NOT NULL)''')
                    
    # Updated Complaints Table with New Features
    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    username VARCHAR(50), 
                    description TEXT NOT NULL, 
                    category VARCHAR(100),
                    confidence FLOAT,
                    location VARCHAR(255),
                    pincode VARCHAR(10),
                    image_path VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'Pending', 
                    date DATETIME,
                    FOREIGN KEY (username) REFERENCES users(username))''')
    conn.commit()
    return conn

# Initialize Database
try:
    get_db_connection().close()
except Exception as e:
    st.error(f"⚠️ MySQL Connection Error. Details: {e}")
    st.stop()

# --- 3. HELPER FUNCTIONS ---
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def add_user(username, password, role):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        return False 
    finally:
        conn.close()

def login_user(username, password):
    conn = get_db_connection()
    c = conn.cursor(dictionary=True)
    c.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    data = c.fetchall()
    conn.close()
    return data

# --- 4. ML MODEL LOADING ---
@st.cache_resource
def load_model():
    return joblib.load('complaint_model.pkl')

try:
    model = load_model()
except Exception as e:
    st.error("⚠️ Model not found! Please run 'train_model.py' first.")
    st.stop()

# --- 5. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'role' not in st.session_state:
    st.session_state['role'] = ''

# --- 6. MAIN APPLICATION LOGIC ---
def main():
    st.sidebar.title("Navigation 🧭")
    
    if not st.session_state['logged_in']:
        menu = ["Home", "Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)
        # ... (Home, Signup, Login logic remains exactly the same as previous code) ...
        # (Included here briefly for completeness)
        if choice == "Home":
            # --- INDEX PAGE (Project Description) ---
            st.title("🏛️ Smart Public Complaint Portal")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)
            st.markdown("### Welcome to the AI-Powered Civic Issue Tracker")
            st.info("👈 Please use the Sidebar menu to Login or Sign Up to get started.")
            
            st.divider()
            
            # Detailed Project Description
            st.markdown("""
            #### 📖 About the Project
            The rapid growth of digital governance has increased the need for transparent, secure, and efficient platforms for handling public grievances. Traditional complaint registration systems are often manual, time-consuming, and lack proper tracking mechanisms. 
            
            To address these challenges, we have developed this **Smart Public Complaint Portal**. It is designed to streamline the process of complaint submission, tracking, and resolution through a centralized, AI-driven web platform.

            #### 🚀 How Our AI System Works
            Our system completely automates the grievance routing process:
            1. **Citizen Submission:** Users log in and describe their civic issue (e.g., broken streetlights, water leaks, uncollected garbage) in simple, natural language.
            2. **AI Processing:** Instead of users manually guessing and selecting departments, our integrated **Machine Learning Model** reads the complaint text and instantly predicts the exact government department responsible for the issue.
            3. **Secure Storage & Tracking:** The complaint, along with location data and photo evidence, is saved securely in our database. Citizens can track the status (Pending, In Progress, Resolved) in real-time.
            4. **Admin Resolution:** Government officials have a dedicated, role-based dashboard to view, manage, and resolve registered complaints efficiently.

            #### ⭐ Key Features
            * **Automated Categorization:** Powered by Natural Language Processing (NLP) to avoid manual misrouting.
            * **Multimedia Support:** Citizens can upload photo evidence and provide precise location details (Pincode/Street).
            * **Role-Based Access Control:** Distinct and secure portals for standard Users (Citizens) and Administrators (Officials).
            * **Local Community Feed:** Users can search their Pincode to view other registered issues in their locality.
            * **Smart Notifications:** Real-time alerts to the user when an official updates the status of their complaint.

            #### 🛠️ Technology Stack
            * **Frontend & UI:** Streamlit (Python) for a highly responsive, modern interface.
            * **Backend Logic:** Core Python programming.
            * **Machine Learning Engine:** Scikit-Learn (TF-IDF Vectorization & Logistic Regression) trained on real-world civic issue datasets.
            * **Database Management:** MySQL for secure, relational, and scalable data storage.
            """)
            
            st.divider()
            st.caption("Designed and Developed as a Secure Web Application for Public Grievance Management.")
        elif choice == "Sign Up":
            st.subheader("Create New Account 📝")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type='password')
            role = st.selectbox("Role", ["User", "Admin"])
            if st.button("Sign Up"):
                if new_user and new_password:
                    if add_user(new_user, make_hashes(new_password), role):
                        st.success("Account created successfully! Please go to Login.")
                    else:
                        st.error("Username exists.")
        elif choice == "Login":
            st.subheader("Login 🔐")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                result = login_user(username, make_hashes(password))
                if result:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['role'] = result[0]['role']
                    st.rerun()
                else:
                    st.warning("Incorrect Credentials")

    else:
        # --- SIDEBAR REDESIGN ---
        # 1. User Profile Avatar
        st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.sidebar.success(f"Welcome back, **{st.session_state['username']}**!")
        st.sidebar.caption(f"Account Type: {st.session_state['role']}")
        
        st.sidebar.divider()
        
        # 2. Quick Guidelines for Users
        st.sidebar.markdown("### 💡 Quick Tips")
        st.sidebar.info(
            "• Provide exact landmarks.\n"
            "• Upload clear photos.\n"
            "• Track status in Notifications."
        )
        
        st.sidebar.divider()
        
        # 3. Emergency Contacts
        st.sidebar.markdown("### 📞 Emergency Contacts")
        st.sidebar.error(
            "👮 Police: 100\n"
            "🚑 Ambulance: 108\n"
            "🚒 Fire Rescue: 101"
        )
        
        st.sidebar.divider()

        # 4. Logout Button
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
            
        st.sidebar.caption("v1.0.0 | Smart City Portal")

      

        # ----------------------------------------
        # USER DASHBOARD (Citizen View)
        # ----------------------------------------
        if st.session_state['role'] == "User":
            st.title(f"👋 Welcome, {st.session_state['username']}!")
            tab1, tab2, tab3, tab4 = st.tabs(["📢 Register Complaint", "📋 My Complaints", "🌍 Local Issues", "🔔 Notifications"])
            
            with tab1:
                st.markdown("### Report a new issue")
                # ONLY this text goes to the ML Model
                complaint_text = st.text_area("📝 Describe your problem in detail:", height=150)
                
                # Extra Features (Goes only to Database)
                col1, col2 = st.columns(2)
                with col1:
                    location = st.text_input("📍 Exact Location (Street/Area)")
                with col2:
                    pincode = st.text_input("📌 Pincode")
                    
                uploaded_file = st.file_uploader("📸 Upload Photo Evidence (Optional)", type=['jpg', 'jpeg', 'png'])
                
                if st.button("🚀 Submit Complaint", type="primary"):
                    if complaint_text.strip() != "":
                        
                        # 1. ML Prediction & Confidence Calculation
                        predicted_category = model.predict([complaint_text])[0]
                        # Extract probabilities to calculate confidence score
                        probabilities = model.predict_proba([complaint_text])[0]
                        confidence_score = max(probabilities) * 100
                        
                        # 2. Handle Image Upload
                        image_path = "No Image"
                        if uploaded_file is not None:
                            image_path = os.path.join("uploads", uploaded_file.name)
                            with open(image_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # 3. Save everything to MySQL
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute('''INSERT INTO complaints 
                                     (username, description, category, confidence, location, pincode, image_path, status, date) 
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                  (st.session_state['username'], complaint_text, predicted_category, confidence_score, 
                                   location, pincode, image_path, "Pending", current_date))
                        conn.commit()
                        conn.close()
                        
                        # 4. Success UI & Progress Bar
                        st.success("✅ Complaint Registered Successfully!")
                        st.info(f"🤖 AI routed this to Department: **{predicted_category}**")
                        
                        st.write("📊 **AI Confidence Score:**")
                        st.progress(int(confidence_score))
                        st.caption(f"Our AI is {confidence_score:.2f}% sure about this category.")
                        
                        # 5. Download Receipt Feature
                        receipt_text = f"""
                        -----------------------------------------
                                COMPLAINT RECEIPT
                        -----------------------------------------
                        Date & Time : {current_date}
                        Citizen Name: {st.session_state['username']}
                        
                        Description : {complaint_text}
                        Location    : {location}, {pincode}
                        
                        AI Category : {predicted_category} (Confidence: {confidence_score:.2f}%)
                        Status      : Pending
                        -----------------------------------------
                        Thank you for your civic responsibility!
                        """
                        st.download_button(
                            label="📄 Download Complaint Receipt",
                            data=receipt_text,
                            file_name=f"Complaint_{current_date.replace(':', '-')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("⚠️ Please enter a complaint description.")
                        
            with tab2:
                st.markdown("### 🔍 Track your complaints")
                
                # 6. Filter "My Complaints" Feature
                filter_status = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Resolved", "Rejected"])
                
                conn = get_db_connection()
                c = conn.cursor(dictionary=True)
                
                if filter_status == "All":
                    c.execute("SELECT id, description, category, location, pincode, status, date FROM complaints WHERE username=%s", (st.session_state['username'],))
                else:
                    c.execute("SELECT id, description, category, location, pincode, status, date FROM complaints WHERE username=%s AND status=%s", (st.session_state['username'], filter_status))
                
                data = c.fetchall()
                conn.close()
                
                df = pd.DataFrame(data)
                if not df.empty:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info(f"No complaints found for status: {filter_status}")
            # --- TAB 3: LOCAL COMMUNITY FEED ---
            with tab3:
                st.markdown("### 🌍 Local Area Issues")
                st.write("Enter your area pincode to see what other issues people have registered nearby.")
                
                search_pin = st.text_input("🔍 Enter Pincode to search:", placeholder="e.g., 613009")
                
                if search_pin:
                    conn = get_db_connection()
                    c = conn.cursor(dictionary=True)
                    # Fetching complaints for this pincode, ordered by latest
                    c.execute("SELECT category, description, location, status, date FROM complaints WHERE pincode=%s ORDER BY date DESC", (search_pin,))
                    local_data = c.fetchall()
                    conn.close()
                    
                    if local_data:
                        st.success(f"📍 Found {len(local_data)} complaints in Pincode {search_pin}")
                        for item in local_data:
                            # Using expander to make it look like a neat feed
                            with st.expander(f"{item['category']} at {item['location']} - Status: {item['status']}"):
                                st.write(f"**Issue:** {item['description']}")
                                st.caption(f"Reported on: {item['date']}")
                    else:
                        st.info("No complaints have been registered in this pincode yet. The area is all clear!")

            # --- TAB 4: NOTIFICATIONS / ALERTS ---
            with tab4:
                st.markdown("### 🔔 Recent Notifications")
                st.write("You will receive alerts here when the Admin updates your complaint status.")
                
                conn = get_db_connection()
                c = conn.cursor(dictionary=True)
                # Fetch only complaints that are NOT pending (meaning admin has taken some action)
                c.execute("SELECT id, category, status, date FROM complaints WHERE username=%s AND status != 'Pending' ORDER BY date DESC", (st.session_state['username'],))
                alerts = c.fetchall()
                conn.close()
                
                if alerts:
                    for alert in alerts:
                        if alert['status'] == 'Resolved':
                            st.success(f"🎉 **Good News!** Your complaint #{alert['id']} ({alert['category']}) has been successfully **Resolved**.")
                        elif alert['status'] == 'In Progress':
                            st.info(f"🚧 **Update:** Your complaint #{alert['id']} ({alert['category']}) is currently **In Progress**. It will be fixed soon.")
                        elif alert['status'] == 'Rejected':
                            st.error(f"❌ **Alert:** Your complaint #{alert['id']} ({alert['category']}) has been **Rejected**.")
                else:
                    st.write("No new notifications. Once the Admin updates your complaints, they will appear here like a timeline!")
        # ----------------------------------------
        # ADMIN DASHBOARD
        # ----------------------------------------
        elif st.session_state['role'] == "Admin":
            st.title("🛡️ Admin Control Panel & Analytics")
            
            # Fetch all data once
            conn = get_db_connection()
            c = conn.cursor(dictionary=True)
            c.execute("SELECT * FROM complaints ORDER BY date DESC")
            data = c.fetchall()
            conn.close()
            
            df_all = pd.DataFrame(data)
            
            if not df_all.empty:
                # --- FEATURE 3: ADVANCED FILTERING ---
                st.markdown("### 🔍 Filter Complaints")
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    status_options = ["All"] + list(df_all['status'].unique())
                    filter_status = st.selectbox("Filter by Status:", status_options)
                with col_f2:
                    cat_options = ["All"] + list(df_all['category'].unique())
                    filter_cat = st.selectbox("Filter by Category:", cat_options)
                    
                # Apply Filters
                df_filtered = df_all.copy()
                if filter_status != "All":
                    df_filtered = df_filtered[df_filtered['status'] == filter_status]
                if filter_cat != "All":
                    df_filtered = df_filtered[df_filtered['category'] == filter_cat]

                # Top Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Filtered", len(df_filtered))
                col2.metric("Pending", len(df_filtered[df_filtered['status'] == 'Pending']))
                col3.metric("Resolved", len(df_filtered[df_filtered['status'] == 'Resolved']))
                
                st.divider()

                # --- FEATURE 1: VISUAL ANALYTICS (GRAPHS) ---
                st.markdown("### 📊 Complaint Analytics")
                if not df_filtered.empty:
                    chart_col1, chart_col2 = st.columns(2)
                    with chart_col1:
                        # Pie Chart for Status
                        status_counts = df_filtered['status'].value_counts().reset_index()
                        status_counts.columns = ['Status', 'Count']
                        fig_pie = px.pie(status_counts, names='Status', values='Count', hole=0.4, title="Status Distribution")
                        st.plotly_chart(fig_pie, use_container_width=True)
                        
                    with chart_col2:
                        # Bar Chart for Category
                        cat_counts = df_filtered['category'].value_counts().reset_index()
                        cat_counts.columns = ['Category', 'Count']
                        fig_bar = px.bar(cat_counts, x='Category', y='Count', title="Complaints by Category", color='Category')
                        st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No data available for the selected filters to show charts.")

                st.divider()

                # --- DISPLAY TABLE & FEATURE 4: EXPORT TO CSV ---
                col_t1, col_t2 = st.columns([3, 1])
                with col_t1:
                    st.markdown("### 📋 Complaint Records")
                with col_t2:
                    # CSV Download Button
                    if not df_filtered.empty:
                        csv_data = df_filtered.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download CSV Report",
                            data=csv_data,
                            file_name=f"Admin_Report_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    
                st.dataframe(df_filtered[['id', 'username', 'category', 'location', 'pincode', 'status', 'date']], use_container_width=True, hide_index=True)
                
                st.divider()

                # --- FEATURE 2: COMPLAINT INSPECTOR & PHOTO VIEWER ---
                st.markdown("### 📸 Complaint Inspector & Action Panel")
                if not df_filtered.empty:
                    insp_col1, insp_col2 = st.columns([1, 1])
                    
                    with insp_col1:
                        selected_id = st.selectbox("Select Complaint ID to Inspect/Update:", df_filtered['id'].tolist())
                        
                        # Get details of selected complaint
                        selected_row = df_filtered[df_filtered['id'] == selected_id].iloc[0]
                        
                        st.info(f"**Full Description:**\n\n{selected_row['description']}")
                        st.write(f"**🤖 AI Confidence:** {selected_row['confidence']:.2f}%")
                        st.write(f"**📌 Current Status:** {selected_row['status']}")
                        
                        # Action Panel
                        status_list = ["Pending", "In Progress", "Resolved", "Rejected"]
                        current_index = status_list.index(selected_row['status']) if selected_row['status'] in status_list else 0
                        new_status = st.selectbox("Update Status To:", status_list, index=current_index)
                        
                        if st.button("Save New Status", type="primary"):
                            conn = get_db_connection()
                            c = conn.cursor()
                            c.execute("UPDATE complaints SET status = %s WHERE id = %s", (new_status, selected_id))
                            conn.commit()
                            conn.close()
                            st.success(f"✅ Complaint #{selected_id} updated to {new_status}!")
                            st.rerun()
                            
                    with insp_col2:
                        st.markdown("**📍 Location Map:**")
                        st.write(f"{selected_row['location']} - {selected_row['pincode']}")
                        
                        # --- GOOGLE MAPS INTEGRATION ---
                        address_query = f"{selected_row['location']} {selected_row['pincode']}"
                        url_encoded_address = urllib.parse.quote(address_query)
                        map_url = f"https://maps.google.com/maps?q={url_encoded_address}&output=embed"
                        
                        components.html(
                            f'<iframe width="100%" height="250" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{map_url}"></iframe>',
                            height=250
                        )
                        
                        st.markdown("**📸 Uploaded Evidence (Photo):**")
                        img_path = selected_row['image_path']
                        
                        if pd.notna(img_path) and img_path != "No Image" and os.path.exists(img_path):
                            try:
                                # Try to load the image
                                st.image(img_path, use_container_width=True)
                            except Exception as e:
                                # If image is corrupted, show this error instead of crashing
                                st.error("⚠️ The uploaded image file is corrupted or not a valid image format.")
                        else:
                            st.warning("No photo was uploaded for this complaint.")
            else:
                st.info("🎉 No complaints registered yet in the system. Everything is clear!")

if __name__ == '__main__':
    main()