import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Write credentials from environment variable into a JSON file
with open('credentials.json', 'w') as f:
    f.write(os.environ['GOOGLE_SHEETS_CREDENTIALS'])

# Set up Google Sheets API
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('sheets', 'v4', credentials=credentials)

# Replace with your actual spreadsheet ID and range
SPREADSHEET_ID = '1fssSPKsK8vsXuqh50WYXOE6l5tT-ila9oXsvwKMS1xs'
RANGE = 'Sheet1!A1:Z100'

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
