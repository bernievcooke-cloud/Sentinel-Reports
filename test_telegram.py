import requests

# Your verified credentials
TOKEN = "8775524209:AAFVIpICTK1_Z3guFU_sBqKQtBA8YRKYtpc"
CHAT_ID = "8394071679"

def run_test():
    print("--- INITIATING SENTINEL SIGNAL TEST ---")
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": "🚀 *SENTINEL TEST:* Connection established. Ready for V3.32 deployment.",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("SUCCESS: Check your Telegram phone app now!")
        else:
            print(f"FAILED: {response.text}")
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")

if __name__ == "__main__":
    run_test()