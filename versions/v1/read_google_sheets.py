import os
import json
from typing import List, Any
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from parse_data import parse_data, process_data  # Import functions from parse_data.py

# Constants
SCOPES: List[str] = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID: str = '1fssSPKsK8vsXuqh50WYXOE6l5tT-ila9oXsvwKMS1xs'
RANGE: str = 'main!A1:K999'
OUTPUT_FILE: str = 'output.json'

def get_credentials(environment: str) -> Credentials:
    """
    Retrieve Google Sheets API credentials based on the environment.

    Args:
        environment (str): The environment (e.g., 'github_actions', 'local').

    Returns:
        Credentials: Google API credentials.
    """
    if environment == 'github_actions':
        credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
        if not credentials_json:
            raise ValueError("Environment variable 'GOOGLE_SHEETS_CREDENTIALS' is missing.")
        credentials_info = json.loads(credentials_json)
        return Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    else:
        service_account_file = 'credentials.json'
        if not os.path.exists(service_account_file):
            raise FileNotFoundError("Missing 'credentials.json' file in the local environment.")
        return Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

def fetch_sheet_data(service: Any, spreadsheet_id: str, range_name: str) -> List[List[Any]]:
    """
    Fetch data from a Google Sheet.

    Args:
        service (Any): Google Sheets API service instance.
        spreadsheet_id (str): The ID of the spreadsheet.
        range_name (str): The range to fetch data from.

    Returns:
        List[List[Any]]: The fetched data from the sheet.
    """
    try:
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result.get('values', [])
    except HttpError as e:
        raise RuntimeError(f"HTTP error while fetching data from Google Sheets: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching data: {e}")

def main() -> None:
    """
    Main function to execute the script.

    Returns:
        None
    """
    # Determine the environment
    environment: str = os.getenv('ENVIRONMENT', 'local')

    try:
        # Get credentials
        credentials: Credentials = get_credentials(environment)
        
        # Build the Google Sheets service
        service: Any = build('sheets', 'v4', credentials=credentials)
        
        # Fetch raw data from the Google Sheet
        raw_data: List[List[Any]] = fetch_sheet_data(service, SPREADSHEET_ID, RANGE)
        
        # Parse and process the data
        parsed_data = parse_data(raw_data)
        processed_data = process_data(parsed_data)
        
        # Save processed data to JSON
        with open(OUTPUT_FILE, 'w') as json_file:
            json.dump(processed_data, json_file, indent=2)
        
        # Print for debugging/logging
        print(json.dumps(processed_data, indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
