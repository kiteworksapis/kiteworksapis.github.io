import os
import requests
from get_access_token import KWOAuthClient

"""
Compose an email, attach a file to the email, and send the message.

User Inputs:
    1. file_path: Local file path of the file you want to upload
    2. file_name: Name of the attachment you want that file to be called.
    3. subject: Subject of email
    4. body: Message body of email
"""

def send_mail(base_url, access_token, file_name, file_path, subject, body, recipient):
    headers = {
        "X-Accellion-Version": '28',
        "Authorization": f"Bearer {access_token}"
    }

    # Step 1: Create the email
    url_create_email = f"{base_url}/rest/mail/actions/sendFile?returnEntity=True"

    # Request body
    data_create_email = {
        "subject": subject,
        "body": body, #Change email body
        "to": [recipient], #Change recipients here
        "draft": "true",
        "secureBody": "false"
    }

    # Make the POST request to create the email and get the email ID
    create_email_response = requests.post(url_create_email, headers=headers, json=data_create_email)
    # Check the response
    if create_email_response.status_code != 201:
        print("Failed to send email:", create_email_response.text)
        return

    create_mail_json = create_email_response.json()
    mail_id = create_mail_json["id"]

    # Step 2: Initiate the file upload

    initiate_upload_url = f"{base_url}/rest/mail/{mail_id}/actions/initiateUpload?returnEntity=true"
    file_size = os.path.getsize(file_path)
    initiate_upload_payload = {
        "totalChunks": 1,
        "totalSize": file_size,
        "filename": file_name
    }

    initiate_upload_response = requests.post(initiate_upload_url, headers=headers, json=initiate_upload_payload)
    initiate_upload_data = initiate_upload_response.json()
    upload_url = initiate_upload_data["uri"]

    # Step 2: Upload the file chunk
    upload_url = f"{base_url}/{upload_url}?returnEntity=True"

    compression_mode = "NORMAL"  # Available options: "NORMAL", "GZIP", "ZLIB"
    compression_size = file_size  # Assuming no compression, set to original file size
    original_size = file_size

    payload = {
        "compressionMode": (None, compression_mode),
        "compressionSize": (None, str(compression_size)),
        "originalSize": (None, str(original_size)),
        "content": (file_name, open(file_path, "rb"))
        # "index": (None, "1"),  # Optional: Chunk index, starts from 1
        # "lastChunk": (None, "1")  # Optional: Indicate if this is the last chunk
    }

    upload_response = requests.post(upload_url, headers=headers, files=payload)

    if upload_response.status_code == 201:
        uploaded_file_data = upload_response.json()
        print("File uploaded successfully.")
        file_id = uploaded_file_data["id"]

    # Step 3: Send the email
        url_send_email = f"{base_url}/rest/mail/{mail_id}/actions/sendFile?returnEntity=True"
        data_send_email = {
            "files": [file_id],
            "draft": "false",
            "uploading": 0
        }

        # Make the PUT request to send the email
        send_email_response = requests.put(url_send_email, headers=headers, json=data_send_email)
        # Check the response
        if send_email_response.status_code == 200:
            print("Email sent successfully")
        else:
            print("Failed to send email:", send_email_response.text)

def main():
    base_url = input("Enter Base URL for Kiteworks Instance: ")
    client = KWOAuthClient(base_url)
    access_token = client.get_access_token()

    file_path = input("Enter local file path of file to upload: ")
    file_name = input("Enter name of attachment: ")
    subject = input("Enter Email Subject: ")
    body = input("Enter Email Message Body: ")
    recipient = input("Enter email address of recipient: ")

    send_mail(base_url, access_token, file_name, file_path, subject, body, recipient)

if __name__ == "__main__":
    main()
