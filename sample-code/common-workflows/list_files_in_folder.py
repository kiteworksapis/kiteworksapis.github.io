import requests

from get_access_token import KWOAuthClient

"""
Generate list of files in a specific folder.

User Inputs:
  1. folder_id: ID of the folder.
"""

def list_files_in_folder(base_url, access_token, folder_id):

    url = f"{base_url}/rest/folders/{folder_id}/files"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Accellion-Version': '28',
        'Content-Type': 'application/json'
    }
    # Optional query parameters
    params = {
        # 'name': 'exampleFileName',  # Uncomment and set the file name to filter by name
        # 'userId': 'exampleUserId',  # Uncomment and set the user ID to filter by creator
        # 'limit': 10,  # Uncomment and set the limit of files to retrieve
        # 'offset': 0,  # Uncomment and set the offset for pagination
        # 'orderBy': 'name:asc',  # Uncomment and set the order by criteria
        # 'returnEntity': 'false'  # Uncomment and set to 'true' if you want to return the entity
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return response.status_code, response.text

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    parent_folder_id = input("Enter parent folder ID: ")
    files = list_files_in_folder(base_url, access_token, parent_folder_id)
    print(files)

if __name__ == "__main__":
    main()
