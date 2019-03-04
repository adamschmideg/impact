# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import argparse
import json
import pickle
from os import environ
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
#SAMPLE_SPREADSHEET_ID = '1hjvBzOVRnybuAHkbgbJ1bURRmpUnxrmoxYbZPwLh3sw'
SPREADSHEET_ID = '1akipBBkbzSqwDr9YA3qn9enKLKCtOm6j-fo-VQfHdIc'
RANGE = 'Sheet1!A2:A5'

def make_credentials():
    creds = Credentials('dummy')
    creds._client_id = environ['CLIENT_ID']
    creds._client_secret = environ['CLIENT_SECRET']
    creds._refresh_token = environ['REFRESH_TOKEN']
    creds.token = environ['ACCESS_TOKEN']
    creds._token_uri = "https://oauth2.googleapis.com/token"
    creds._scopes = SCOPES
    return creds

def get_sheet():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            good_creds = pickle.load(token)
            import pdb
            creds = Credentials('foobar')
            creds.token = good_creds.token
            #pdb.set_trace()
            creds.refresh_token = good_creds.refresh_token
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists('credentials.json'):
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        else:
            creds = make_credentials()

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    return service.spreadsheets().values()

def get_args():
    parser = argparse.ArgumentParser(description='Save to a google sheet')
    parser.add_argument('--cell-range', dest='cell_range', required=True)
    parser.add_argument('--sheet-id', dest='sheet_id', default=SPREADSHEET_ID)
    parser.add_argument('--value', dest='value', required=True)
    return parser.parse_args()

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    sheet = get_sheet()
    args = get_args()
    print('args', args)
    resource = {
            #"majorDimension": "ROW", 
            "values": [[args.value]]}
    #result = sheet.append(spreadsheetId=SPREADSHEET_ID, range=RANGE, body=resource).execute()
    result = sheet.append(
            spreadsheetId=args.sheet_id,
            range=args.cell_range,
            body=resource,
            valueInputOption="USER_ENTERED"
            ).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()
