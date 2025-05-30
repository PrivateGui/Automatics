import requests
import json
import time
import random

config = ["zonercm was here","this is an automated message."]
rname = random.choice(config)

# Configuration variables
ROBLOX_COOKIE = "enter your roblox cookie"
CONVERSATION_ID = "5abf40ea-be20-52e8-b43f-26dae8cb7fd8"
MESSAGE = f"{rname}"
API_URL = "https://apis.roblox.com/platform-chat-api/v1/send-messages"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

def get_csrf_token():
    """
    Correctly fetches X-CSRF-Token by making a dummy POST request.
    """
    headers = {
        "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Roblox/WinInet"
    }

    for attempt in range(RETRY_ATTEMPTS):
        try:
            # Dummy POST to trigger CSRF token response
            response = requests.post("https://auth.roblox.com/v2/logout", headers=headers, timeout=10)
            if response.status_code == 403 and 'x-csrf-token' in response.headers:
                csrf_token = response.headers['x-csrf-token']
                print("✅ CSRF token fetched successfully.")
                return csrf_token
            else:
                print(f"❌ Attempt {attempt + 1}: CSRF token not found. Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️ Attempt {attempt + 1}: Error - {e}")

        time.sleep(RETRY_DELAY)
    
    print("❌ Failed to obtain CSRF token after multiple retries.")
    return None

def send_roblox_message():
    csrf_token = get_csrf_token()
    if not csrf_token:
        print("Aborting: CSRF token fetch failed.")
        return

    headers = {
        "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}",
        "Content-Type": "application/json",
        "X-CSRF-Token": csrf_token,
        "Accept": "application/json",
        "User-Agent": "Roblox/WinInet"
    }

    payload = {
        "conversation_id": CONVERSATION_ID,
        "messages": [
            {
                "content": MESSAGE
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            print("✅ Message sent successfully!")
            print("📩 Response:", response.json())
        else:
            print(f"❌ Failed to send message. Status: {response.status_code}")
            print("🔍 Response:", response.text)
    except requests.RequestException as e:
        print(f"⚠️ Network error: {e}")

if __name__ == "__main__":
    if not CONVERSATION_ID:
        print("⚠️ Please set a valid CONVERSATION_ID.")
    elif not MESSAGE:
        print("⚠️ Please set a non-empty MESSAGE.")
    else:
        send_roblox_message()
