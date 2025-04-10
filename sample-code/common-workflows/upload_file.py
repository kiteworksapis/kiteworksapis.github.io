import os
import requests
import json
from urllib.parse import quote
from get_access_token import KWOAuthClient

"""
Upload a file to a specified location in Kiteworks.

User Inputs:
    1. path_to_file: Local file path of the file you want to upload
    2. path_to_upload_folder: Path to the folder on Kiteworks that the file is uploaded to
    3. new_file_name: Name of the attachment you want that file to be called.
"""

def upload_file(base_url, access_token, path_to_file, path_to_upload_folder, new_file_name):

    headers = {
        "x-accellion-version": "28",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": 'application/json'
    }

    # Step 1: Get folder id
    path_to_upload_folder = quote(path_to_upload_folder)
    search_folder_url = f"{base_url}/rest/search?path={path_to_upload_folder}"

    search_response = requests.get(search_folder_url, headers=headers)
    search_response_data = search_response.json()

    folder_id = ""
    if search_response_data and search_response_data["folders"]:
        folder_id = search_response_data["folders"][0]["id"]
    else:
        print("Incorrect path specified. Folder does not exist.")

    # Step 2: Initiate the file upload
    file_size = os.path.getsize(path_to_file)

    initiate_upload_url = f"{base_url}/rest/folders/{folder_id}/actions/initiateUpload"
    initiate_upload_payload = {
        "totalChunks": 1,
        "totalSize": file_size,
        "filename": new_file_name
    }

    del headers["Content-Type"]
    initiate_upload_response = requests.post(initiate_upload_url, headers=headers, json=initiate_upload_payload)
    initiate_upload_data = initiate_upload_response.json()
    upload_id = initiate_upload_data["id"]

    # Step 3: Upload the file chunk
    upload_url = f"{base_url}/rest/uploads/{upload_id}?returnEntity=True"

    compression_mode = "NORMAL"  # Available options: "NORMAL", "GZIP", "ZLIB"
    compression_size = file_size  # Assuming no compression, set to original file size
    original_size = file_size

    payload = {
        "compressionMode": (None, compression_mode),
        "compressionSize": (None, str(compression_size)),
        "originalSize": (None, str(original_size)),
        "content": (new_file_name, open(path_to_file, "rb"))
        # "index": (None, "1"),  # Optional: Chunk index, starts from 1
        # "lastChunk": (None, "1")  # Optional: Indicate if this is the last chunk
    }

    upload_response = requests.post(upload_url, headers=headers, files=payload)

    if upload_response.status_code == 201:
        uploaded_file_data = upload_response.json()
        print("File uploaded successfully.")
        print("Uploaded file details:")
        print(json.dumps(uploaded_file_data, indent=2))
    else:
        print(f"File upload failed with status code: {upload_response.status_code}")
        print(upload_response.text)

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    path_to_file = input("Enter path to local file: ")
    path_to_upload_folder = input("Enter path to KW folder for file to be uploaded to: ")
    new_file_name = input("Enter the file's new name on KW: ")

    upload_file(base_url, access_token, path_to_file, path_to_upload_folder, new_file_name)

if __name__ == "__main__":
    main()