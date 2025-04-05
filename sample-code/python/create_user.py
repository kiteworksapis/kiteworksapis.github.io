import json
import requests
from get_access_token import KWOAuthClient

"""
Create a user in Kiteworks

User Input:
  1. email - New User Email
  2. password - New User Password
"""

def create_user(base_url, access_token, user_data):
    url = f"{base_url}/rest/admin/users"

    headers = {
        "X-Accellion-Version": "28",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "returnEntity": "true"
    }

    res = requests.post(url, headers=headers, params=params, data=json.dumps(user_data))

    if res.status_code == 201:
        print("User created successfully.")
        print("User details:", res.json())
    else:
        print("Failed to create user. Status code:", res.status_code)
        print("Response:", res.text)

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    user_data = {
        "email": input("Enter New User Email: "),
        "name": "New User",
        "password": input("Enter New User Password: "),
        "userTypeId": 1,
        "verified": "false",
        "sendNotification": "false"
    }

    create_user(base_url, access_token, user_data)

if __name__ == "__main__":
    main()