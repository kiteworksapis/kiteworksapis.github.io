import requests
import json
from get_access_token import KWOAuthClient

"""
Create a top-level folder in Kiteworks
"""

def create_folder(base_url, access_token, folder_data):

    url = f"{base_url}/rest/folders/0/folders"

    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    params = {
        "returnEntity": "true"
    }

    res = requests.post(url, headers=headers, params=params, data=json.dumps(folder_data))

    return res

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    folder_data = {
        "name": "The Top Level Folder",
        "description": "This is a top-level folder.",
        "secure": False,
        "syncable": False,
        # "clientId": "",  # Optional, provide if applicable
        # "vendorDocId": "",  # Optional, provide if applicable
        # "isFolderUpload": False,  # Optional, for internal use only
        # "expire": "",  # Optional, provide if applicable (format not defined)
        # "rename": False,  # Optional
        # "fileLifetime": 0  # Optional, provide if applicable
    }


    response = create_folder(base_url, access_token, folder_data)

    print(response.json())


if __name__ == "__main__":
    main()