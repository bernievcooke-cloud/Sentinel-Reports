import subprocess
import os
import sys
import time
from twilio.rest import Client

# --- CREDENTIALS ---
ACCOUNT_SID = 'AC2e9c9be175911cce282ad3109c53ade5'
AUTH_TOKEN = '0820479e9367a679294fce8a615f11bf'
FROM_WHATSAPP = 'whatsapp:+14155238886'
TO_WHATSAPP = 'whatsapp:+61409139355' 

# --- GITHUB SETTINGS ---
GH_USER = "YOUR_GITHUB_USERNAME"  # <--- Change this
GH_REPO = "Sentinel-Reports"      # <--- Change this
BASE_URL = f"https://{GH_USER}.github.io/{GH_REPO}/"

def sync_to_github(loc, local_path):
    try:
        # Move to the directory and run Git commands
        os.chdir(r"C:\OneDrive\PublicReports")
        
        # 1. Stage the specific file
        subprocess.run(["git", "add", "."], check=True)
        # 2. Commit the change
        subprocess.run(["git", "commit", "-m", f"Update {loc} report"], check=True)
        # 3. Push to the web
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print(f"File synced to GitHub for {loc}")
        return True
    except Exception as e:
        print(f"Git Sync Failed: {e}")
        return False

def dispatch_cloud():
    loc = sys.argv[1].strip() if len(sys.argv) > 1 else "Unknown"
    
    # Trigger the Web Sync first
    if sync_to_github(loc, ""):
        # Wait 2 seconds for GitHub to refresh its "Pages"
        time.sleep(2)
        
        # This is the magic link Twilio will use to "Grab" the PDF
        # Note: We use the actual filename logic from your worker
        datestr = time.strftime("%Y-%m-%d")
        file_name = f"Surf_{loc}_{datestr}.pdf"
        pdf_url = f"{BASE_URL}OUTPUT/{loc}/{file_name}"

        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        
        message = client.messages.create(
            body=f"🚀 *SENTINEL STRATEGY: {loc.upper()}*",
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP,
            media_url=[pdf_url] # This attaches the PDF as a document
        )
        print(f"Direct PDF Dispatched: {message.sid}")
    else:
        print("Failed to sync to GitHub. Aborting Twilio.")

if __name__ == "__main__":
    dispatch_cloud()