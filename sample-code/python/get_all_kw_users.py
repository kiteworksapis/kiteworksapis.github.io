import requests
from get_access_token import KWOAuthClient

"""
Generate a list of Kiteworks users.
"""

def get_all_kw_users(access_token, base_url):

    url = f"{base_url}/rest/admin/users"
    headers = {
        'X-Accellion-Version': '28',
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }

    all_users = []
    offset = 0
    limit = 100  # Assuming a batch size of 100 users per request

    while True:
        params = {
            'offset': offset,
            'limit': limit,
            # Optional parameters
            #'email': '',
            #'email:contains': '',
            #'name': '',
            #'name:contains': '',
            #'metadata': '',
            #'metadataContains': '',
            #'deleted': 'false',
            #'active': 'true',
            #'verified': 'false',
            #'suspended': 'false',
            #'isRecipient': 'false',
            #'allowsCollaboration': 'true',
            #'created': '',  # Format: date
            #'created:gt': '',
            #'created:gte': '',
            #'created:lt': '',
            #'created:lte': '',
            #'orderBy': '',
            #'locate_id': 0,
            #'with': '',
        }

        response = requests.get(url, headers=headers, params=params)
        response_data = response.json()

        if not response_data['data']:
            break  # Exit loop if no more users are returned

        all_users.extend(response_data['data'])
        offset += limit  # Increment the offset to fetch the next batch of users

    return all_users

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()
    users = get_all_kw_users(access_token, base_url)
    print(users)

if __name__ == "__main__":
    main()
