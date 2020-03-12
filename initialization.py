from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://mail.google.com/']

def initialization():

    creds = None

    if os.path.exists('gmail-autotests/token.pickle'):
        with open('gmail-autotests/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'gmail-autotests/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('gmail-autotests/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
    return service
