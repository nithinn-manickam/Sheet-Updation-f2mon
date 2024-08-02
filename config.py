import os
from dotenv import load_dotenv


load_dotenv(override=True)

getenv = os.getenv

class google_sheet_configs:

    SERVICE_ACCOUNT_FILE = getenv("SERVICE_ACCOUNT_FILE")
    EXISTING_SPREADSHEET_ID = getenv("PARENT_FOLDER_ID")

class path_configs:

    LOGS_PATH = getenv("LOGS_PATH")

