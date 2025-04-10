import requests

from get_access_token import KWOAuthClient

"""
Lists all the top-level folders in Kiteworks
"""

def list_top_level_folders(base_url, access_token):

    url = f"{base_url}/rest/folders/top"
    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    # Optional parameters can be included in the query string if needed
    params = {
        # 'orderBy': 'name:asc',  # Sorting options: name, modified, created, size
        # 'offset': 0,  # Pagination offset
        # 'limit': 10,  # Pagination limit
        # 'deleted': 'false',  # Include deleted: true, false, none
        # 'with': '',  # Additional data to include
        # 'returnEntity': 'false'  # Whether to return the entity in the response
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Failed to retrieve folders: {response.status_code} - {response.text}"

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    folders_data = list_top_level_folders(base_url, access_token)
    print(folders_data)

if __name__ == "__main__":
    main()
