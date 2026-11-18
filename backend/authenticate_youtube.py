import os
import sys
import webbrowser
import logging

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
except ImportError:
    print("Google OAuth libraries not installed. Run: pip install google-auth-oauthlib google-api-python-client")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YouTubeAuth")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(base_dir, "client_secret.json")
    token_file = os.path.join(base_dir, "youtube_token.json")

    if not os.path.exists(secrets_file):
        print(f"[ERROR] client_secret.json not found at: {secrets_file}")
        print("Please ensure your Google Cloud OAuth 2.0 Client credentials file is placed there.")
        sys.exit(1)

    print("=" * 60)
    print("🚀 ClipFlow AI — YouTube 1-Click Channel Authorization")
    print("=" * 60)
    print("Starting local OAuth authorization server...")
    print("A browser window will open automatically asking you to log into Google and grant upload permission.")
    print("-" * 60)

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            secrets_file,
            scopes=SCOPES
        )
        # run_local_server runs a temporary local web server to catch OAuth redirect
        creds = flow.run_local_server(
            host="localhost",
            port=8080,
            authorization_prompt_message="Open this link in your browser if it doesn't open automatically:\n{url}",
            success_message="✅ YouTube Authentication Successful! You can close this browser tab now and return to ClipFlow AI.",
            open_browser=True
        )

        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())

        print("\n" + "=" * 60)
        print("🎉 SUCCESS! YouTube channel authorization is complete!")
        print(f"Credentials safely saved to: {token_file}")
        print("Automated 30-minute Short uploads are now fully enabled!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[ERROR] Authentication failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
