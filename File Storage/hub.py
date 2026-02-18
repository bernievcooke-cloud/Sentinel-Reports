import streamlit as st
import subprocess
import sys

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sentinel Strategy Hub", page_icon="📡", layout="centered")

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #0077b6; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 SENTINEL STRATEGY HUB")
st.subheader("Professional Grade Surf & Sky Intelligence")

# --- USER INPUTS ---
col1, col2 = st.columns(2)
with col1:
    report_type = st.selectbox("Select Strategy", ["Surf Strategy", "Sky Strategy"])
with col2:
    location = st.text_input("Target Location", "Phillip Island")

phone = st.text_input("WhatsApp Number (with +61)", "+61")

# --- THE COMMERCIAL LOGIC ---
st.info("Direct Delivery: Your report will be sent via WhatsApp immediately after generation.")

# In a live setup, you'd replace this with a Stripe link check
if st.button(f"Generate & Send {report_type}"):
    if len(phone) < 10:
        st.error("Please enter a valid WhatsApp number.")
    else:
        with st.spinner(f"Engaging Sentinel Workers for {location}..."):
            # Determine which worker to call
            worker_script = "surf_worker.py" if "Surf" in report_type else "sky_worker.py"
            
            try:
                # RUN THE WORKER SCRIPT IN THE BACKGROUND
                # Passes Location and Phone as sys.argv[1] and [2]
                process = subprocess.run(
                    [sys.executable, worker_script, location, phone],
                    capture_output=True, text=True
                )
                
                if process.returncode == 0:
                    st.success(f"🚀 Success! Sentinel has dispatched your {report_type} to {phone}.")
                    st.balloons()
                else:
                    st.error(f"Worker Error: {process.stderr}")
                    
            except Exception as e:
                st.error(f"System Error: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Sentinel Engine V4.0 | AWS S3 Vault | Twilio API")