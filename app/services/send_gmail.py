#Import email data encoding
import base64
from pathlib import Path
from datetime import datetime, timezone
from email.message import EmailMessage
import os

#Import Credentials class to assign the token as inheritor
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def get_credentials():
    try:
        scope = ["https://www.googleapis.com/auth/gmail.send"]
        project_root = Path(__file__).resolve().parents[-2]
        local_token_file = project_root/"secrets"/"token.json"

        token_file = Path(os.getenv("gmail_token_file", str(local_token_file)))

    except Exception as e:
        print(f"Error while looking for the token file, details: {e}")

        return False
    
    credentials = Credentials.from_authorized_user_file(
        token_file,
        scope
    )

    if credentials.expired and credentials.refresh_token:
        print("\nRefreshing token..")
        credentials.refresh(Request())

        temporary_file = token_file.with_suffix(".tmp")
        with temporary_file.open('w', encoding = 'utf-8') as file:
            file.write(credentials.to_json())
        temporary_file.replace(token_file)

    if not credentials.valid:
        raise RuntimeError("Credentials are invalid, please run authorization script again!")

    return credentials

def send_email(
        event_id: str,
        source: str,
        owner_email: str,
        message: str,
        timestamp: datetime):
    
    credentials = get_credentials()

    email_service = build(
        "gmail",
        "v1",
        credentials = credentials,
        cache_discovery = False
    )

    email_message = EmailMessage()

    email_message["To"] = owner_email
    email_message["Subject"] = f"Alert from System {source}"

    email_message.set_content(
        f"""A new system alert has been sent from the external system monitor:
        Event ID: {event_id}
        Message: {message}
        Time of Event: {str(timestamp)}

        Please check the alert and investigate ASAP!"""
    )

    encoded_email = base64.urlsafe_b64encode(
        email_message.as_bytes()
    ).decode('utf-8')

    sent_message = (
        email_service.users().messages().send(
            userId = "me",
            body = {
                "raw": encoded_email
            } 
        ).execute()
    )

    return sent_message["id"]

if __name__ == "__main__":
    message_id = send_email(
        event_id = "evt_0001",
        source = "Server 1",
        owner_email = "thelastofusp2.ii@gmail.com",
        message = "HIGH CPU USAGE",
        timestamp = datetime.now(timezone.utc))

    print(message_id)