import pymongo
import os 
import dotenv

dotenv.load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION"))
db3 = client["f2mon-data-v2"]

class db_instance:

    sites = db3["Sites"]
    upi_appearance_metadata = db3["UPI-appearance-metadata"]
    upi_master = db3["UPI-master"]

