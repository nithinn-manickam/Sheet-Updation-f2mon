import os
from mongo import db_instance
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from collections import defaultdict
import pymongo
import dotenv
from datetime import datetime
from config import google_sheet_configs


class ReportUpdater:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        self.credentials = service_account.Credentials.from_service_account_file(google_sheet_configs.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        
        self.spreadsheet_id = google_sheet_configs.EXISTING_SPREADSHEET_ID 

    def get_data(self):
        sites_list=db_instance.sites.distinct("site")
        sites_data=[]
        for i in sites_list:
            d=db_instance.sites.find_one({"site":i})
            total=d.get("total_upi_id_collected")
            today=d.get("upi_ids_collected_today")
            sites_data.append({i:[total,today]})
        return sites_data

    def add_new_worksheet(self):
        data=self.get_data()
        
        
        # Get new sheet        
        # Prepare data for new worksheet
        header = ["Sites", "Total UPI-ID Collected So Far", "UPI-ID Collected Today "]
        values = [header]
        
        for item in data:
            for site, counts in item.items():
                total_count, today_count = counts
                values.append([site, total_count, today_count])
        
        body = {
            'majorDimension': 'ROWS',
            'values': values
        }
        
        # Write data to new worksheet
        self.sheets_service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=f"UPI IDs Count!A1",
            valueInputOption='RAW',
            body=body
        ).execute()
        

# Example usage
if __name__ == "__main__":
    updater = ReportUpdater()
    updater.update_worksheet()