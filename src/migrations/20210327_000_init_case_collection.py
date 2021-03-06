import os
import sys
from pathlib import Path
from pymongo import MongoClient

import pandas as pd

from constants import CASE_INFO_CSV_DIR, MONGO_DB_URL, TZ
from models import prep_cases_df


def main():
    # Load initial data
    in_csv = CASE_INFO_CSV_DIR / "20200609_case_info.csv"
    if not in_csv.is_file():
        print("Error: Input file missing")
        sys.exit()
    in_df = pd.read_csv(in_csv, low_memory=False)
    # prep data
    in_df = prep_cases_df(in_df)

    date_str = in_csv.name.split("_")[0]
    in_df["createdAt"] = pd.to_datetime(date_str).tz_localize(TZ)

    # region mongodb
    print("Connecting to mongodb...")
    mongo_client = MongoClient(MONGO_DB_URL)
    mongo_db = mongo_client["defaultDb"]
    mongo_col = mongo_db["cases"]
    if "cases" in mongo_db.list_collection_names():
        # drop collection first
        print("Removing old data...")
        mongo_col.drop()

    print("Connection successful...")
    # endregion mongodb

    # insert data
    data_dict = in_df.to_dict("records")
    mongo_col.create_index(
        [
            ("caseCode", 1),
        ],
        unique=True,
    )
    mongo_col.insert_many(data_dict)


if __name__ == "__main__":
    main()
