import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

class JokeSheetHandler:
    def __init__(self):

        # Initialize credentials and authorize the client
        self.creds_path = 'exclude/sheets-credentials.json'
        self.sheet_id = '13mwxpcSWS5kcC-Up78OQ-qbAI4dH7EKUz7ZU__1dLI0'
        self.creds = Credentials.from_service_account_file(self.creds_path)

        # Define the required scopes
        self.scoped_creds = self.creds.with_scopes([
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ])

        # Authorize the gspread client
        self.client = gspread.authorize(self.scoped_creds)

        # Open the sheet
        self.sheet = self.client.open_by_key(self.sheet_id)
        self.worksheet = self.sheet.get_worksheet(0)  # Access the first sheet

    def get_first_unposted_joke(self):
        # Fetch data from the sheets
        rows = self.worksheet.get_all_records()

        # Iterate through the rows and return the first row without a PostedDate
        for idx, row in enumerate(rows):
            if not row.get('PostedDate'):
                return row, idx  # Returning the row and its index for further updates
        return None, -1  # If no unposted joke is found

    def update_posted_date(self, ID):
        # Update the PostedDate column with the current date for a specific row
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.worksheet.update_cell(ID + 1, self.worksheet.find("PostedDate").col, current_date)  

# Example usage
if __name__ == "__main__":
    # Initialize the GoogleSheetHandler class
    sheet_handler = JokeSheetHandler()
    # Get the first unposted joke
    joke, row_id = sheet_handler.get_first_unposted_joke()
    if joke:
        print("First unposted joke:", joke)

        # Update the posted date after using the joke
        sheet_handler.update_posted_date(row_id)
        print(f"Updated PostedDate for row {row_id + 2}.")
    else:
        print("No unposted jokes found.")
