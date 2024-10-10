import csv
import os
from datetime import datetime, timedelta

from database.connect import crashes, daily_crashes, weekly_crashes, monthly_crashes, areas, injuries_by_area_info, \
    crashes_causes

daily_cash: dict = {}
weekly_cash: dict = {}
monthly_cash: dict = {}
area_cash: dict = {}
causes_cash: dict = {}
injuries_cash:dict = {}

def read_csv(csv_path):
   with open(csv_path, 'r') as file:
       csv_reader = csv.DictReader(file)
       for row in csv_reader:
           yield row

def init_db():
    csv_path = './data/fake.csv'
    crashes.drop()
    daily_crashes.drop()
    weekly_crashes.drop()
    monthly_crashes.drop()
    areas.drop()
    injuries_by_area_info.drop()
    crashes_causes.drop()

    for row in read_csv(csv_path):
        crash_datetime = parse_date(row["CRASH_DATE"])
        crash_date = crash_datetime.date()

        # Create crash document
        crash = {
            "CRASH_RECORD_ID": row["CRASH_RECORD_ID"],
            "CRASH_DATE": str(crash_date),
            "BEAT_OF_OCCURRENCE": row["BEAT_OF_OCCURRENCE"],
            "TOTAL_INJURIES": row["INJURIES_TOTAL"],
            "FATAL_INJURIES": row["INJURIES_FATAL"],
            "INCAPACITATING_INJURIES": row["INJURIES_INCAPACITATING"],
            "INCAPACITATING_NON_INJURIES": row["INJURIES_NON_INCAPACITATING"],
            "PRIM_CONTRIBUTORY_CAUSE": row["PRIM_CONTRIBUTORY_CAUSE"],
            "SEC_CONTRIBUTORY_CAUSE": row["SEC_CONTRIBUTORY_CAUSE"]
        }

        crash_id = crashes.insert_one(crash).inserted_id

        # Update daily, weekly, monthly, and area collections
        update_collection(daily_crashes, daily_cash, crash_date, "date")
        update_collection(weekly_crashes, weekly_cash, get_week_range(crash_datetime)[0], "start_date")
        update_collection(monthly_crashes, monthly_cash, (crash_date.month, crash_date.year), "month")
        update_collection(areas, area_cash, crash["BEAT_OF_OCCURRENCE"], "area")

        if causes_cash.get(crash["PRIM_CONTRIBUTORY_CAUSE"]) is None:
            cause = {
                "PRIM_CONTRIBUTORY_CAUSE": crash["PRIM_CONTRIBUTORY_CAUSE"],
                "CRASHES_LIST": [crash_id],
                "TOTAL_INJURIES": int(crash["TOTAL_INJURIES"]),
                "FATAL_INJURIES": int(crash["FATAL_INJURIES"]),
                "INCAPACITATING_INJURIES": int(crash["INCAPACITATING_INJURIES"]),
                "INCAPACITATING_NON_INJURIES": int(crash["INCAPACITATING_NON_INJURIES"])
            }
            causes_cash[crash["PRIM_CONTRIBUTORY_CAUSE"]] = 1
            crashes_causes.insert_one(cause)
        else:
            crashes_causes.update_one(
                {"PRIM_CONTRIBUTORY_CAUSE": crash["PRIM_CONTRIBUTORY_CAUSE"]},
                {
                    "$push": {"CRASHES_LIST": crash_id},
                    "$inc": {
                        "TOTAL_INJURIES": safe_int(crash["TOTAL_INJURIES"]),
                        "FATAL_INJURIES": safe_int(crash["FATAL_INJURIES"]),
                        "INCAPACITATING_INJURIES": safe_int(crash["INCAPACITATING_INJURIES"]),
                        "INCAPACITATING_NON_INJURIES": safe_int(crash["INCAPACITATING_NON_INJURIES"])
                    }
                }
            )

        if injuries_cash.get(crash["PRIM_CONTRIBUTORY_CAUSE"]) is None:
            injury = {
                "area": crash["BEAT_OF_OCCURRENCE"],
                "CRASHES_LIST": [crash_id],
                "injuries_case": safe_int(crash["TOTAL_INJURIES"]) - safe_int(crash["FATAL_INJURIES"]),
                "death_case": safe_int(crash["FATAL_INJURIES"])
            }
            injuries_cash[crash["PRIM_CONTRIBUTORY_CAUSE"]] = 1
            injuries_by_area_info.insert_one(injury)
        else:
            injuries_by_area_info.update_one(
                {"PRIM_CONTRIBUTORY_CAUSE": crash["PRIM_CONTRIBUTORY_CAUSE"]},
                {
                    "$push": {"CRASHES_LIST": crash_id},
                    "$inc": {
                        "injuries_case": safe_int(crash["TOTAL_INJURIES"]),
                        "death_case": safe_int(crash["FATAL_INJURIES"])
                    }
                }
            )




def parse_date(date_str: str):
    has_seconds = len(date_str.split(' ')) > 2
    date_format = '%m/%d/%Y %H:%M:%S %p' if has_seconds else '%m/%d/%Y %H:%M'
    return datetime.strptime(date_str, date_format)

def get_week_range(date):
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return start.date(), end.date()

def update_collection(collection, cache, key, field_name):
    if cache.get(key) is None:
        doc = {field_name: str(key), "amount": 1}
        cache[key] = 1
        collection.insert_one(doc)
    else:
        collection.update_one(
            {field_name: str(key)},
            {"$inc": {"amount": 1}}
        )

def safe_int(value, default=0):
    try:
        return int(value) if value.strip() else default
    except ValueError:
        return default
