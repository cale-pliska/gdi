import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Determine the environment
environment = os.getenv('ENVIRONMENT', 'local')

# Set up Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

if environment == 'github_actions':
    # In GitHub Actions, credentials are provided via environment variable
    credentials_info = json.loads(os.getenv('GOOGLE_SHEETS_CREDENTIALS'))
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
else:
    # Locally, use the credentials.json file
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

# Replace with your actual spreadsheet ID and range
SPREADSHEET_ID = '1fssSPKsK8vsXuqh50WYXOE6l5tT-ila9oXsvwKMS1xs'
RANGE = 'main!A1:K999'

# Clear the contents of output.json
open('output.json', 'w').close()

# Read data from Google Sheets
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
values = result.get('values', [])

# Save data as JSON
output = {
    "spreadsheet_id": SPREADSHEET_ID,
    "data": values,
}

with open('output.json', 'w') as json_file:
    json.dump(output, json_file)

print(json.dumps(output, indent=2))  # Print for debug/logging