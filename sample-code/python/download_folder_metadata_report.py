import requests
from get_access_token import KWOAuthClient

"""
Download a report of folder events.

User Inputs:
  1. folder_id: ID of the folder.
"""

def download_folder_metadata_report(base_url, access_token, folder_id):

    url = f"{base_url}/rest/folders/{folder_id}/activities/actions/exportCSV"

    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        # 'startTime': '1609459200',  # Example start time in unix timestamp
        # 'endTime': '1640995200',    # Example end time in unix timestamp
        'orderBy': 'created:desc',  # Order by creation date in descending order
        'type': 'all',              # Type of activities to include
        'limit': '100',             # Limit the number of results
        'returnEntity': 'false'     # Do not return the full entity details
        # Additional parameters can be added here as needed
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        with open('folder_metadata_report.csv', 'wb') as f:
            f.write(response.content)
        print("Report downloaded successfully.")
    else:
        print(f"Failed to download report: {response.status_code} - {response.text}")

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()
    folder_id = input("Input Folder ID: ")
    download_folder_metadata_report(base_url, access_token, folder_id)

if __name__ == "__main__":
    main()
