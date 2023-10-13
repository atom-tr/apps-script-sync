"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function

import os.path
import json


from google.oauth2.credentials import Credentials
from googleapiclient import errors
from googleapiclient.discovery import build


from manager_environment import EnvironmentManager as ENV
from manager_github import GitHubManager

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/script.projects']

MANIFEST = {
    "timeZone": f"{ENV.TIMEZONE}",
    "exceptionLogging": "CLOUD"
}


def main():
    """Calls the Apps Script API.
    """
    GitHubManager.prepare_github_env()
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token = {
        'refresh_token': ENV.REFRESH_TOKEN,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": ENV.CLIENT_ID,
        "client_secret": ENV.CLIENT_SECRET,
        "scopes": [
            "https://www.googleapis.com/auth/script.projects"
        ],
    }
    creds = Credentials.from_authorized_user_info(token, SCOPES)
    try:
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
        repo_path = f'repo/{ENV.PROJECT_PATH}'
        for file in os.listdir(repo_path):
            if file.endswith('.gs'):
                with open(os.path.join(repo_path, file), 'r') as f:
                    request['files'].append({
                        'name': file,
                        'type': 'SERVER_JS',
                        'source': f.read()
                    })
        service.projects().updateContent(body=request, scriptId=ENV.PROJECT_ID).execute()
    except errors.HttpError as error:
        # The API encountered a problem.
        print(error.content)


if __name__ == '__main__':
    main()
