import pyautogui
import time
import sys
import os
import glob
import pyperclip

def log_event(message):
    # Logs events to help us find the 'break' if it doesn't send
    with open("dispatch_log.txt", "a") as f:
        f.write(f"{time.ctime()}: {message}\n")

def dispatch():
    try:
        # Check if the Hub actually told us which location to send
        if len(sys.argv) < 2:
            log_event("Error: No location argument received.")
            return

        loc = sys.argv[1].strip()
        log_event(f"Starting dispatch for: {loc}")

        # 1. FIND THE FILE (The Handshake)
        target_folder = os.path.join(r"C:\OneDrive\PublicReports\OUTPUT", loc)
        files = glob.glob(os.path.join(target_folder, "*.pdf"))
        
        if not files:
            log_event(f"Error: No PDF found in {target_folder}")
            return
        
        latest_pdf = max(files, key=os.path.getctime)
        full_path = os.path.abspath(latest_pdf)
        log_event(f"Found file: {full_path}")

        # 2. FOCUS WHATSAPP
        # Clicks the chat area (1108, 400) to make window active
        pyautogui.click(301, 133)
        time.sleep(1)

        # 3. ATTACHMENT SEQUENCE
        pyautogui.click(1127, 777) '+' icon
        time.sleep(1.5)
        pyautogui.click(1540, 921)'Document' icon
        time.sleep(2)

        # 4. PASTE & OPEN (Windows Dialog)
        pyperclip.copy(full_path)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)
        pyautogui.press('enter')
        log_event("File path pasted into Windows dialog.")

        # 5. THE FINAL DISPATCH (The Triple-Enter Fix)
        # We wait 7 seconds because the 'flicking cursor' means it's loading
        print("Waiting for WhatsApp Preview...")
        time.sleep(7) 

        # Click the caption box to ensure focus is away from the search bar
        pyautogui.click(1127, 522)
        time.sleep(1)

        # Triple kick to force it through
        pyautogui.press('enter') 
        time.sleep(1.5)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter') 
        
        log_event("Final Dispatch Enters executed.")

    except Exception as e:
        log_event(f"CRITICAL ERROR: {str(e)}")

if __name__ == "__main__":
    dispatch()