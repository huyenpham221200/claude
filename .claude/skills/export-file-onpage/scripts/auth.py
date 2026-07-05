"""OAuth2 helper for export-file-onpage. Reuses the OAuth client from
cro-setup (same Google Cloud project) but keeps its own token, scoped only
for Google Sheets — does not touch the GTM/GA4 token from cro-setup.

First run opens a browser for one-time consent; subsequent runs reuse the
saved token (auto-refreshes silently when expired).
"""
from __future__ import annotations

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SKILL_DIR = Path(__file__).parent.parent
CRED_DIR = SKILL_DIR / "credentials"
OAUTH_CLIENT_FILE = CRED_DIR / "oauth_client.json"
TOKEN_FILE = CRED_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_credentials() -> Credentials:
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        return creds

    if not OAUTH_CLIENT_FILE.exists():
        raise FileNotFoundError(
            f"Khong tim thay OAuth client tai {OAUTH_CLIENT_FILE}. "
            "Can copy file oauth_client.json vao thu muc credentials/ truoc."
        )

    flow = InstalledAppFlow.from_client_secrets_file(str(OAUTH_CLIENT_FILE), SCOPES)
    creds = flow.run_local_server(port=0)
    CRED_DIR.mkdir(exist_ok=True)
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return creds


if __name__ == "__main__":
    c = get_credentials()
    print("OAuth OK. Token da duoc luu, san sang su dung.")
