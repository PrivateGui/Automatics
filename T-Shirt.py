import requests
import json
import time
from pathlib import Path

# Configuration
API_KEY = "your_api_key_here"  # Replace with your Roblox Open Cloud API key
CREATOR_ID = "your_creator_id"  # Replace with User ID or Group ID (e.g., "Group:123456")
ASSET_NAME = "Automated T-Shirt"
ASSET_DESCRIPTION = "A T-shirt uploaded via Open Cloud API"
IMAGE_PATH = "path/to/tshirt.png"  # Path to your T-shirt image file (PNG)

# Roblox Open Cloud API endpoints
UPLOAD_ASSET_URL = "https://apis.roblox.com/assets/v1/assets"
OPERATION_STATUS_URL = "https://apis.roblox.com/cloud/v2/operations/{}"

def upload_tshirt():
    """Upload a T-shirt to Roblox."""
    headers = {
        "x-api-key": API_KEY,
    }
    
    # Read the image file
    image_path = Path(IMAGE_PATH)
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found at: {IMAGE_PATH}")

    # Prepare the multipart form data
    files = {
        "fileContent": (image_path.name, open(image_path, "rb"), "image/png"),
        "request": (None, json.dumps({
            "assetType": "TShirt",  # Try "Decal" if TShirt fails
            "displayName": ASSET_NAME,
            "description": ASSET_DESCRIPTION,
            "creationContext": {
                "creator": {
                    "userId": CREATOR_ID if not CREATOR_ID.startswith("Group") else None,
                    "groupId": CREATOR_ID.replace("Group:", "") if CREATOR_ID.startswith("Group") else None
                }
            }
        }))
    }

    try:
        # Send the POST request to upload the asset
        response = requests.post(UPLOAD_ASSET_URL, headers=headers, files=files)
        response.raise_for_status()
        result = response.json()
        
        if result.get("done"):
            asset_id = result.get("response", {}).get("assetId")
            print(f"T-shirt uploaded successfully! Asset ID: {asset_id}")
            return asset_id
        else:
            operation_id = result.get("operationId")
            print(f"Upload in progress. Operation ID: {operation_id}")
            return check_operation_status(operation_id)

    except requests.exceptions.HTTPError as e:
        print(f"Failed to upload T-shirt: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def check_operation_status(operation_id):
    """Poll the operation status until complete."""
    headers = {
        "x-api-key": API_KEY,
    }
    status_url = OPERATION_STATUS_URL.format(operation_id)

    while True:
        try:
            response = requests.get(status_url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result.get("done"):
                if result.get("response", {}).get("assetId"):
                    asset_id = result["response"]["assetId"]
                    print(f"T-shirt uploaded successfully! Asset ID: {asset_id}")
                    return asset_id
                else:
                    print(f"Upload failed: {result.get('response', {})}")
                    return None
            else:
                print(f"Operation still in progress: {operation_id}")
                time.sleep(5)  # Wait 5 seconds before polling again

        except requests.exceptions.HTTPError as e:
            print(f"Failed to check operation status: {e}")
            print(f"Response: {e.response.text}")
            return None
        except Exception as e:
            print(f"Unexpected error while checking status: {e}")
            return None

def main():
    try:
        asset_id = upload_tshirt()
        if asset_id:
            print(f"You can view the T-shirt at: https://www.roblox.com/catalog/{asset_id}")
        else:
            print("Failed to retrieve asset ID. Check the Creator Dashboard for details.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
