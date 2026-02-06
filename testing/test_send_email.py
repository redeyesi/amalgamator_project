import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    creds = None
    # token.json stores the user's access and refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_message():
    service = get_gmail_service()

    # Create the email content
    message = EmailMessage()
    message.set_content("This is a test email sent from the Gmail API using Python!")
    message["To"] = "simongreen1@gmail.com"  # <-- Change this
    message["From"] = "your-email@gmail.com"  # <-- Change this
    message["Subject"] = "Automated Python Email"

    # Encode the message in base64
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}

    try:
        send_result = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_result["id"]} sent successfully!')
    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    send_message()
