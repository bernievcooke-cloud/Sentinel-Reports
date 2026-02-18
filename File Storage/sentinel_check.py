import os
import sys
import time
import webbrowser
import pyautogui

def run_diagnostics():
    print("🚀 --- SENTINEL SYSTEM DIAGNOSTICS --- 🚀\n")

    # 1. Check Libraries
    libraries = ['requests', 'matplotlib', 'pandas', 'reportlab', 'pyautogui', 'streamlit']
    print("📦 1. LIBRARY CHECK:")
    for lib in libraries:
        try:
            __import__(lib)
            print(f"✅ {lib:12} : Installed")
        except ImportError:
            print(f"❌ {lib:12} : MISSING")

    # 2. Check OneDrive Path & Write Permissions
    BASE_DIR = r"C:\OneDrive\PublicReports"
    OUTPUT_DIR = os.path.join(BASE_DIR, "OUTPUT")
    print("\n📂 2. ONEDRIVE CONNECTIVITY:")
    
    if os.path.exists(BASE_DIR):
        print(f"✅ Base Directory : Found")
        try:
            if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
            test_file = os.path.join(OUTPUT_DIR, "connection_test.txt")
            with open(test_file, "w") as f:
                f.write(f"Sentinel Handshake Test: {time.ctime()}")
            print(f"✅ Write Permission: Granted (Test file created)")
        except Exception as e:
            print(f"❌ Write Permission: DENIED ({e})")
    else:
        print(f"❌ Base Directory : NOT FOUND (Check path: {BASE_DIR})")

    # 3. Automation "Ghost" Check
    print("\n🖱️ 3. AUTOMATION HANDSHAKE (Watch your mouse):")
    print("Moving mouse to (100, 100) in 2 seconds...")
    time.sleep(2)
    pyautogui.moveTo(100, 100, duration=1)
    print("✅ PyAutoGUI : Active")

    print("\n🌐 4. WEB DISPATCH CHECK:")
    print("Opening Google in 2 seconds to test browser link...")
    time.sleep(2)
    webbrowser.open("https://www.google.com")
    print("✅ WebBrowser : Link Sent")

    print("\n--- DIAGNOSTICS COMPLETE ---")
    print("If all ✅, your Merimbula test should run perfectly.")

if __name__ == "__main__":
    run_diagnostics()