import requests
import os
import time

# Configuration
API_KEY = ""  # Replace with your Roblox API key
UNIVERSE_ID = ""  # Replace with your Universe ID
PLACE_ID = ""  # Replace with your Place ID
RBXL_FILE_PATH = ""  # Path to your .rbxl file
UPLOAD_URL = f"https://apis.roblox.com/universes/v1/{UNIVERSE_ID}/places/{PLACE_ID}/versions"
MAX_RETRIES = 4
TIMEOUT = 120  # Timeout in seconds
VERSION_TYPE = "Published"  # Set to "Published" or "Saved"

def upload_rbxl(file_path):
    """Upload an .rbxl file to Roblox with retry logic."""
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return False
    if not os.access(file_path, os.R_OK):
        print(f"Error: File {file_path} is not readable")
        return False

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with open(file_path, "rb") as file:
                headers = {
                    "x-api-key": API_KEY,
                    "Content-Type": "application/octet-stream"
                }
                # Add versionType query parameter
                params = {"versionType": VERSION_TYPE}
                response = requests.post(UPLOAD_URL, headers=headers, params=params, data=file, timeout=TIMEOUT)

            if response.status_code == 200:
                print(f"Successfully uploaded {file_path} to Roblox!")
                return True
            else:
                print(f"Attempt {attempt}: Failed to upload {file_path}. Status: {response.status_code}, Error: {response.text}")
                if attempt == MAX_RETRIES:
                    return False
        except requests.exceptions.Timeout:
            print(f"Attempt {attempt}: Request timed out for {file_path}")
            if attempt == MAX_RETRIES:
                print("Max retries reached. Upload failed.")
                return False
        except Exception as e:
            print(f"Attempt {attempt}: Error uploading {file_path}: {str(e)}")
            if attempt == MAX_RETRIES:
                return False
        time.sleep(2)  # Wait before retrying
    return False

if __name__ == "__main__":
    print(f"Uploading {RBXL_FILE_PATH}...")
    upload_rbxl(RBXL_FILE_PATH)
