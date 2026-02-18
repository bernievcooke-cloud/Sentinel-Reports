from twilio.rest import Client

TW_SID = 'AC2e9c9be175911cce282ad3109c53ade5'
TW_AUTH = '0820479e9367a679294fce8a615f11bf'
# Use the number provided in your Twilio Console - it might be different than the sandbox one now
TW_FROM = 'whatsapp:+14155238886' 
MY_MOBILE = 'whatsapp:+61409139355' # <--- CHANGE THIS

client = Client(TW_SID, TW_AUTH)

try:
    msg = client.messages.create(
        from_=TW_FROM,
        body="SENTINEL UPGRADE: Paid account detected. Connection Live.",
        to=MY_MOBILE
    )
    print(f"SUCCESS! Message SID: {msg.sid}")
    print(f"Status: {msg.status}")
except Exception as e:
    print(f"STILL BLOCKED: {e}")