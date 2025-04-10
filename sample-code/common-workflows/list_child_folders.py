import requests

from get_access_token import KWOAuthClient

"""
Generate list of subfolders in a specific folder.

User Inputs:
  1. parent_folder_id: ID of the parent folder
"""

def list_child_folders(base_url, access_token, parent_folder_id):

    url = f"{base_url}/rest/folders/{parent_folder_id}/folders"
    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # Optional query parameters
    params = {
        # 'name': 'exampleFolderName',  # Uncomment and set value to filter by exact folder name
        # 'name:contains': 'partOfName',  # Uncomment and set value to search folders containing specific characters
        # 'userId': 'user123',  # Uncomment and set value to filter by creator's user ID
        # 'created': '2023-01-01',  # Uncomment and set value to filter by creation date
        # 'modified': '2023-01-02',  # Uncomment and set value to filter by modification date
        # 'deleted': 'false',  # Uncomment and set value to filter by deletion status
        # 'secure': 'false',  # Uncomment and set value to filter by secure flag
        # 'orderBy': ['name'],  # Uncomment and set value to sort results
        # 'offset': 0,  # Uncomment and set value to specify offset
        # 'limit': 10,  # Uncomment and set value to limit the number of results returned
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    folder_id = input("Enter Parent Folder ID: ")
    folders = list_child_folders(base_url, access_token, folder_id)
    print(folders)

if __name__ == "__main__":
    main()
