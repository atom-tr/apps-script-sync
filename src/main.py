"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function

import os.path
from os import getenv, environ
import json
from datetime import datetime

from google.oauth2.credentials import Credentials
# from googleapiclient import errors
from googleapiclient.discovery import build

from _github import GitHubManager
from _logger import Logger

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/script.projects']

# Get environment variables
TIMEZONE = getenv("INPUT_TIMEZONE", "Asia/Ho_Chi_Minh")

# Google Script
PROJECT_ID = environ["INPUT_PROJECT_ID"]
PROJECT_PATH = environ["INPUT_PROJECT_PATH"]
# Google app
CLIENT_TYPE = environ["INPUT_CLIENT_TYPE"]
CLIENT_ID = environ["INPUT_CLIENT_ID"]
CLIENT_SECRET = environ["INPUT_CLIENT_SECRET"]
REFRESH_TOKEN = environ["INPUT_REFRESH_TOKEN"]

MANIFEST = {
    "timeZone": f"{TIMEZONE}",
    "exceptionLogging": "CLOUD"
}
_TRUTHY = ["true", "1", "t", "y", "yes"]
logger = Logger("DEBUG" if getenv("DEBUG_RUN", "False").lower() in _TRUTHY else "INFO")


def main():
    """Calls the Apps Script API.
    """
    GitHubManager.prepare_github_env()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token = {
        'refresh_token': REFRESH_TOKEN,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scopes": [
            "https://www.googleapis.com/auth/script.projects"
        ],
    }
    creds = Credentials.from_authorized_user_info(token, SCOPES)
    service = build('script', 'v1', credentials=creds)
    # Call the Apps Script API
    # Upload two files to the project
    request = {
        'files': [{
            'name': 'appsscript',
            'type': 'JSON',
            'source': json.dumps(MANIFEST)
        }]
    }
    # loop through gs files in webflow directory
    repo_path = f'repo/{PROJECT_PATH}'
    for file in os.listdir(repo_path):
        if file.endswith('.gs'):
            logger.i("Found file $file.", file=file)
            with open(os.path.join(repo_path, file), 'r') as f:
                request['files'].append({
                    'name': file,
                    'type': 'SERVER_JS',
                    'source': f.read()
                })
        else:
            logger.i("Skipping file $file.", file=file)
    service.projects().updateContent(body=request, scriptId=PROJECT_ID).execute()


if __name__ == '__main__':
    start_time = datetime.now()
    logger.g("Program execution started at $date.", date=start_time)
    try:
        main()
        print("status=succeeded")
    except Exception as e:
        logger.p("Program execution failed with error: $error.", error=e)
        print("status=failed")
        
    end_time = datetime.now()
    logger.g("Program execution finished at $date.", date=end_time)
    logger.p("Program finished in $time.", time=end_time - start_time)
    
