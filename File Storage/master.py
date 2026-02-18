import os, requests, time, subprocess, pyautogui
from datetime import datetime  # <--- THE MISSING PIECE
import surf_worker 
import sky_worker  

# ============================================================
# CONTROL PANEL
# ============================================================
REPORT_TYPE = "Surf"  
LOCATION_SEARCH = "Phillip Island"
WHATSAPP_PHONE = "+61409139355" # Your reference number

def get_coords(query):
    headers = {'User-Agent': 'SentinelSystem/1.0'}
    try:
        url = f"https://photon.komoot.io/api/?q={query}&limit=1"
        r = requests.get(url, headers=headers, timeout=10).json()
        if r['features']:
            feat = r['features'][0]
            lon, lat = feat['geometry']['coordinates']
            name = feat['properties'].get('name', query)
            state = feat['properties'].get('state', "")
            return lat, lon, f"{name}, {state}"
        return None, None, None
    except:
        return None, None, None

def send_to_whatsapp(filepath, phone_number):
    """
    Opens WhatsApp, searches for the contact, sends a 'Jolt' text, 
    and then attaches the PDF report.
    """
    print(f"--- Dispatching to WhatsApp: {phone_number} ---")
    
    # 1. Open WhatsApp Desktop
    os.startfile("whatsapp://") 
    time.sleep(6) # Give it time to load the interface
    
    # 2. Focus Search and find contact
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.write(phone_number)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2) # Wait for the chat window to switch

    # 3. THE JOLT: Send text first to trigger phone vibration/notification
    pyautogui.write("🚀 Sentinel Report Incoming...")
    pyautogui.press('enter')
    time.sleep(2) # Short gap so the text and file don't clash
    
    # 4. SEND THE FILE: Copy file to clipboard via PowerShell and paste
    subprocess.run(['powershell', 'Set-Clipboard', '-Path', f'"{filepath}"'])
    pyautogui.hotkey('ctrl', 'v')
    
    # Give WhatsApp 4 seconds to generate the file preview/thumbnail
    time.sleep(4) 
    pyautogui.press('enter')
    
    print(f"DONE: Dispatch to {phone_number} complete.")

def run_sentinel():
    print(f"--- STARTING SENTINEL: {REPORT_TYPE} ---")
    
    # 1. Acquire Coordinates
    lat, lon, full_name = get_coords(LOCATION_SEARCH)
    if not lat:
        print(f"Error: Location '{LOCATION_SEARCH}' not found.")
        return

    # 2. Create Unique Filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"Sentinel_{REPORT_TYPE}_{timestamp}.pdf"
    full_path = os.path.abspath(filename)

    # 3. Trigger Worker
    success = False
    
    if REPORT_TYPE == "Surf":
        # Ensure your surf_worker also uses (path, lat, lon, name)
        success = surf_worker.create_report(full_path, lat, lon, full_name)
        
    elif REPORT_TYPE == "Nightsky":
        # FIXED: This line is now properly indented and uses the correct variable names
        success = sky_worker.create_report(full_path, lat, lon, full_name)

    # 4. Final Handoff
    if success:
        print(f"SUCCESS: {filename} generated.")
        send_to_whatsapp(full_path, WHATSAPP_PHONE)
    else:
        print("FAILED: Worker script encountered an error.")

if __name__ == "__main__":
    run_sentinel()
