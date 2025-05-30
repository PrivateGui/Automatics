import requests
import time
import json

# Configuration
ROBLOX_COOKIE = "enter your cookie"
CHAT_LOG_FILE = "chat_log.txt"
CHAT_ENDPOINT = "https://apis.roblox.com/platform-chat-api/v1/get-user-conversations?include_user_data=true&pageSize=200"
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

def get_csrf_token():
    """
    Fetch CSRF token by intentionally triggering a 403 on logout POST request.
    """
    headers = {
        "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Roblox/WinInet"
    }

    for attempt in range(RETRY_ATTEMPTS):
        try:
            response = requests.post("https://auth.roblox.com/v2/logout", headers=headers, timeout=10)
            if response.status_code == 403 and 'x-csrf-token' in response.headers:
                print("✅ CSRF token obtained.")
                return response.headers['x-csrf-token']
            else:
                print(f"❌ Attempt {attempt + 1}: CSRF token not found.")
        except requests.RequestException as e:
            print(f"⚠️ Error on attempt {attempt + 1}: {e}")
        time.sleep(RETRY_DELAY)

    print("❌ Failed to retrieve CSRF token.")
    return None

def fetch_chat_log():
    """
    Fetch user conversations and save them into a txt file.
    """
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

    try:
        response = requests.get(CHAT_ENDPOINT, headers=headers, timeout=15)

        if response.status_code == 200:
            conversations = response.json()
            with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
                f.write(json.dumps(conversations, indent=2, ensure_ascii=False))
            print(f"✅ Chat log saved to {CHAT_LOG_FILE}")
        else:
            print(f"❌ Failed to fetch chat log. Status: {response.status_code}")
            print("🔍 Response:", response.text)

    except requests.RequestException as e:
        print(f"⚠️ Request error: {e}")

if __name__ == "__main__":
    
        fetch_chat_log()
