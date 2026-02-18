from twilio.rest import Client

# Your exact credentials from your workers
TW_SID = 'AC2e9c9be175911cce282ad3109c53ade5'
TW_AUTH = '0820479e9367a679294fce8a615f11bf'

client = Client(TW_SID, TW_AUTH)

try:
    # This fetches your unique sandbox settings
    sandbox = client.messaging.v1.sessions.fetch('default') # Standard for trial
    print("\n--- TWILIO SANDBOX KEYWORD ---")
    print("Go to WhatsApp on your phone.")
    print("Send a message to: +1 415 523 8886")
    print(f"Message content: join [YOUR_KEYWORD_HERE]")
    print("------------------------------\n")
    print("Note: If the code above is blank, look for the 'join' words in your Twilio Dashboard.")
except:
    # Fallback: Most common way to find it via API
    print("Could not fetch automatically. Please check the 'Messaging' -> 'Try it Out' page one last time.")