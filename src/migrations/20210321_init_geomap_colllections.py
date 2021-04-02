import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# region mongodb
print("Connecting to mongodb...")
mongo_client = MongoClient(os.getenv("MONGO_DB_URL"))
if "default" not in mongo_client.list_database_names():
    print("Database not found... exiting...")
    mongo_client.close()
    sys.exit()
mongo_db = mongo_client["defaultDb"]
mongo_col = mongo_db["geomaps"]
print("Connection successful...")
# endregion mongodb

with open("input/geojson/ph-prov.geojson") as file:
    geo_data = json.load(file)
data_dict = dict(name="ph-prov", geo=geo_data)

mongo_col.insert_one(data_dict)