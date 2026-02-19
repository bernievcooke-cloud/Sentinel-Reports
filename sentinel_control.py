import os
import subprocess
import glob
from twilio.rest import Client
from dotenv import load_dotenv  # <--- Add this

# 1. Load the "Secret Lockbox"
load_dotenv(r"C:\OneDrive\PublicReports\File Storage\.env")

# 2. Assign the keys from the lockbox
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# 3. Rest of your Config
GITHUB_USER = "bernievcooke-cloud"
REPO_NAME = "Sentinel-Access"
BASE_PATH = r"C:\OneDrive\PublicReports\OUTPUT"
FROM_WHATSAPP = 'whatsapp:+14155238886'
TO_WHATSAPP = 'whatsapp:+61409139355'

# ... (rest of your functions below)

# --- CONFIG ---
GITHUB_USER = "bernievcooke-cloud"
REPO_NAME = "Sentinel-Access"
BASE_PATH = r"C:\OneDrive\PublicReports\OUTPUT"

# Twilio Credentials
ACCOUNT_SID = 'AC2e9c9be175911cce282ad3109c53ade5'
AUTH_TOKEN = '0d045827ba9d8e4b3fd86381ef0eee12' 
FROM_WHATSAPP = 'whatsapp:+14155238886'
TO_WHATSAPP = 'whatsapp:+61409139355'

def get_latest_report(location):
    search_path = os.path.join(BASE_PATH, location, "*.pdf")
    files = glob.glob(search_path)
    return max(files, key=os.path.getmtime) if files else None

def deploy_and_notify(location):
    report_path = get_latest_report(location)
    if not report_path:
        print(f"❌ No PDF found in OUTPUT/{location}")
        return

    filename = os.path.basename(report_path)
    print(f"🚀 Processing: {filename}")

    try:
        # 1. GitHub Sync - Using a simpler logic to avoid "nothing to commit" errors
        subprocess.run(["git", "add", "."], check=True)
        # The '|| true' part (or passing check=False) prevents the script from crashing if there's nothing new
        subprocess.run(f'git commit -m "Auto-Sync: {filename}"', shell=True) 
        subprocess.run(["git", "push", "origin", "main", "--force"], check=True)
        
        # 2. Build URL
        live_url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/OUTPUT/{location}/{filename}".replace(" ", "%20")
        
        # 3. WhatsApp Dispatch
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages.create(
            body=f"🌊 *Sentinel Report Ready*\nLocation: {location}\n\nView: {live_url}",
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print(f"✅ WhatsApp Sent! SID: {message.sid}")
        
    except Exception as e:
        print(f"⚠️ Sync Note: {e} (Continuing to WhatsApp...)")
        # Try sending WhatsApp anyway if Git says "already up to date"
        send_only_whatsapp(location, filename)

def send_only_whatsapp(location, filename):
    live_url = f"https://{GITHUB_USER}.github.io/{REPO_NAME}/OUTPUT/{location}/{filename}".replace(" ", "%20")
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        client.messages.create(
            body=f"🌊 *Sentinel Report Ready*\nLocation: {location}\n\nView: {live_url}",
            from_=FROM_WHATSAPP,
            to=TO_WHATSAPP
        )
        print("✅ WhatsApp sent using existing cloud file.")
    except Exception as e:
        print(f"❌ Twilio still failing: {e}")
        print(f"🔗 But your link is LIVE: {live_url}")
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP
    
    print("✅ WhatsApp sent using existing cloud file.")

def main_menu():
    while True:
        print("\n--- Sentinel Access: User Selection ---")
        print("1. Phillip Island (Latest)")
        print("2. Bells Beach (Latest)")
        print("3. Exit")
        choice = input("Select (1-3): ")
        if choice == '1': deploy_and_notify("PhillipIsland")
        elif choice == '2': deploy_and_notify("BellsBeach")
        elif choice == '3': break

if __name__ == "__main__":
    main_menu()