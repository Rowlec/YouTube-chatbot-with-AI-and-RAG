"""
Authentication Manager
Handles YouTube API authentication
"""
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from colorama import Fore

# YouTube API scopes
SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]

API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_authenticated_service():
    """
    Authenticate with YouTube API and return service object
    
    Note: You need to create a Google Cloud project and download
    the client_secret.json file from Google Cloud Console.
    Place it in the config directory as 'client_secret.json'
    """
    credentials = None
    token_file = "config/token.pickle"
    client_secret_file = "config/client_secret.json"
    
    # Check if client_secret.json exists
    if not os.path.exists(client_secret_file):
        print(Fore.RED + "\nError: client_secret.json not found!" + Fore.RESET)
        print(Fore.YELLOW + "\nTo get started:" + Fore.RESET)
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable YouTube Data API v3")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download the JSON file and save as 'config/client_secret.json'")
        print()
        raise FileNotFoundError("client_secret.json not found in config directory")
    
    # Load saved credentials
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)
    
    # If credentials are invalid or don't exist, authenticate
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except Exception as e:
                print(Fore.YELLOW + f"Token refresh failed: {e}. Re-authenticating..." + Fore.RESET)
                credentials = None
        
        if not credentials:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file, SCOPES
            )
            credentials = flow.run_local_server(
                port=8080,
                prompt='consent',
                success_message='Authentication successful! You can close this window.'
            )
            
            # Save credentials for future use
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
            
            print(Fore.GREEN + "Authentication successful!" + Fore.RESET)
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
