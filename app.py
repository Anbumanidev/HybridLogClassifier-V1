import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Hybrid Log Classifier", layout="wide")
st.title("📊 Hybrid Log Classifier")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose task", ["Classify Single Log", "Classify CSV File"])

st.markdown("""
    <style>
    .stSelectbox > div[data-baseweb="select"] {
        max-width: 250px;
    }
    .box {
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: blue;
        font-weight: bold;
    }
    .blue-box {background-color: #1f77b4;}
    .green-box {background-color: #2ca02c;}
    .orange-box {background-color: #ff7f0e;}
    </style>
""", unsafe_allow_html=True)

SOURCES = ["ModernCRM", "AnalyticsEngine", "ModernHR", "BillingSystem", "ThirdPartyAPI","LegacyCRM",]

# ====Single log classifier=====
if page == "Classify Single Log":
    st.header("🔍 Classify a Single Log Message",)
    source = st.selectbox("Select Log Source", SOURCES, index=None, placeholder="Select log source...")
    log_message = st.text_area("Enter Log Message", height=150, placeholder="Type or paste your log message here...")
    if st.button("Classify"):
        try:
            if not source or not log_message:
                st.error("Please select a log source and enter a log message.")
            
            print("Model Running...")
            response = requests.post(f"{API_URL}/predict", params={"source": source, "log_message": log_message})
            
            if response.status_code == 200:
                label = response.json().get("label")
                st.success(f"**predicted label:** {label}")
            else:
                st.error(f"Error from API: {response.text}")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")



# =====CSV file classifier=====
elif page =="Classify CSV File":
    st.header("📁 Classify Log Messages from a CSV File")
    col_left, col_right = st.columns([2, 1])
    
    # ========== LEFT SIDE ==========
    with col_left:
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        
        if uploaded_file:
            try:
                print("Model Running...")
            
                response = requests.post(f"{API_URL}/predict_csv", files={"file": uploaded_file})
                
                if response.status_code == 200:
                    results = response.json()
                    df = pd.DataFrame(results, columns=["Source", "Log Message", "Predicted Label"])
                    st.dataframe(df, use_container_width=True)
                    
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button("Download Results as CSV", data=csv, file_name="classified_logs.csv", mime="text/csv")
                else:
                    st.error(f"Error from API: {response.text}")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
    # ========== RIGHT SIDE ==========
    with col_right:
        st.subheader("📑 Example CSV Format")

        # Load a local example CSV
        csv = pd.read_csv("test/test_logs.csv")   # <-- FIXED

        st.dataframe(csv)

        # Allow user to download it
        with open("test/test_logs.csv", "r") as f:
            st.download_button(
                label="⬇ Download Example CSV",
                data=f,
                file_name="example.csv",
                mime="text/csv"
            )
