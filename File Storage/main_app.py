import streamlit as st
import subprocess, os, sys, glob

st.set_page_config(page_title="SENTINEL STRATEGY HUB", layout="wide")

# --- SIDEBAR: SYSTEM HEALTH & VERIFICATION ---
with st.sidebar:
    st.header("🛡️ SENTINEL STATUS")
    
    # Dynamic Confirmation Check
    st.subheader("📍 TARGET LOCK")
    if st.session_state.get('loc_input'):
        st.info(f"Target: **{st.session_state.loc_input}**")
        st.info(f"Dispatch: **{st.session_state.phone_input}**")
    else:
        st.warning("No Target Selected")

    st.markdown("---")
    st.subheader("📂 RECENT DISPATCHES")
    report_path = r"C:\OneDrive\PublicReports\OUTPUT\*.pdf"
    files = sorted(glob.glob(report_path), key=os.path.getmtime, reverse=True)
    for f in files[:5]:
        st.caption(f"✅ {os.path.basename(f)}")

# --- MAIN INTERFACE ---
st.title("📡 SENTINEL STRATEGY HUB")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    location = st.text_input("🎯 TARGET LOCATION", value="Torquay, VIC", key="loc_input", help="Type town and state (e.g., Merimbula, NSW)")
    strategy = st.selectbox("📊 STRATEGY TYPE", ["Surf Strategy", "Night Sky"])
    phone = st.text_input("📲 DISPATCH TO", value="61400000000", key="phone_input", help="International format: 61... (no +)")

with col2:
    st.write("### ⚙️ SYSTEM CHECKS")
    st.checkbox("Generate 3-Chart Tactical PDF", value=True, disabled=True)
    st.checkbox("Auto-Sync to OneDrive", value=True, disabled=True)
    st.checkbox("WhatsApp Dispatch (Direct Attach)", value=True, disabled=True)

st.markdown("---")

if st.button("🚀 LAUNCH SENTINEL DISPATCH", use_container_width=True):
    target_loc = st.session_state.loc_input
    target_phone = st.session_state.phone_input
    
    with st.status(f"🛰️ Processing {strategy} for {target_loc}...", expanded=True) as status:
        script = "surf_worker.py" if strategy == "Surf Strategy" else "sky_worker.py"
        python_exe = sys.executable
        
        # HANDSHAKE: Sending data to the Engine
        subprocess.Popen([python_exe, script, target_loc, target_phone])
        
        st.write(f"✅ Variable Handshake: {target_loc}")
        st.write(f"✅ Engine Triggered: {script}")
        st.write("🕒 *System will now open WhatsApp Web and attach the PDF...*")
        status.update(label="STRATEGY ENGINE ACTIVE", state="complete")
        st.balloons()