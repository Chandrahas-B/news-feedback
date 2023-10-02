from pymongo import MongoClient
import datetime
import pytz


client = MongoClient("localhost", 27017, username='root', password='example')


db = client["PIB"]

pib_releases = db['PIB Releases']

def insert_document_to_pib_releases(pib_heading: str) -> bool:
    tz = pytz.timezone('Asia/Kolkata')
    post = {
        "author": pib_heading,
        "time": datetime.datetime.now(tz = tz)
    }
    
    insert_post = pib_releases.insert_one(post).inserted_id
    
    print(f"Inserted {insert_post}")
    
    return True