from urllib.parse import quote
import requests
from get_access_token import KWOAuthClient

"""
Download a file from a specified location in Kiteworks.
  - User Inputs
      1. kw_path_to_file: path to the file on Kiteworks ending in the file name.
      2. dest_file_path: path that downloaded file will reside ending in the file name.
"""

def download_file(base_url, access_token, kw_path_to_file, dest_file_path):
    # Constructing the header
    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f'Bearer {access_token}',
    }

    # Get file id from file path
    kw_path_to_file = quote(kw_path_to_file)
    search_folder_url = f"{base_url}/rest/search?path={kw_path_to_file}"

    search_response = requests.get(search_folder_url, headers=headers)
    search_response_data = search_response.json()

    file_id = ""
    if search_response_data and search_response_data["files"]:
        file_id = search_response_data["files"][0]["id"]
    else:
        print("Incorrect path specified. File does not exist.")

    # Constructing the URL for downloading a file
    url = f'{base_url}/rest/files/{file_id}/content'

    res= requests.get(url, headers=headers)

    if res.status_code == 200:
        with open(dest_file_path, "wb") as file:
            file.write(res.content)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {res.status_code}")

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    kw_path_to_file = input("Enter path to the file on Kiteworks ending in the file name: ")
    dest_file_path = input("Enter path that downloaded file will reside: ")

    download_file(base_url, access_token, kw_path_to_file, dest_file_path)

if __name__ == "__main__":
    main()