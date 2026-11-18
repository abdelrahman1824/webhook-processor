from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow #Library for installing OAuth Consent Screen Flow

#Get the secrets directory
try:
    parent_directory = Path(__file__).resolve().parents[-2]
    secrets_file = parent_directory/"secrets"
    credentials_file = secrets_file/"credentials.json"
    token_file = secrets_file/"token.json"
except Exception as e:
    print(f"Error while loading credentials, details: {e}")

def authorize_gmail():
    scope = ["https://www.googleapis.com/auth/gmail.send"]

    flow = InstalledAppFlow.from_client_secrets_file(
        str(credentials_file),
        scope
    )

    credentials = flow.run_local_server(
        host = "localhost",
        port = 0,
        open_browser = True 
    )

    token_file.write_text(credentials.to_json(),
                          encoding = 'utf-8')

if __name__ == "__main__":
    try:
        authorize_gmail()
        print(f"Gmail authorized successfully, token saved in {token_file}")
    except Exception as e:
        print(f"Couldn't authorize gmail, details:{e}")