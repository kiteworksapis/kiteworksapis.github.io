import requests

from get_access_token import KWOAuthClient

"""
Retrieves the metadata of the current user.
"""

def get_current_user(base_url, access_token):

    url = f"{base_url}/rest/users/me"
    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to get user details: {response.status_code} - {response.text}"

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    user_details = get_current_user(base_url, access_token)
    print(user_details)

if __name__ == "__main__":
    main()