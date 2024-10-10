import csv
import os
from datetime import datetime, timedelta

from annotated_types.test_cases import cases

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
            "CRASH_DATE": crash_date,
            "OCCURRENCE_OF_BEAT": row["OCCURRENCE_OF_BEAT"],
            "TOTAL_INJURIES": row["TOTAL_INJURIES"],
            "FATAL_INJURIES": row["FATAL_INJURIES"],
            "INCAPACITATING_INJURIES": row["INCAPACITATING_INJURIES"],
            "INCAPACITATING_NON_INJURIES": row["INCAPACITATING_NON_INJURIES"],
            "PRIM_CONTRIBUTORY_CAUSE": row["PRIM_CONTRIBUTORY_CAUSE"],
            "SEC_CONTRIBUTORY_CAUSE": row["SEC_CONTRIBUTORY_CAUSE"]
        }

        crash_id = crashes.insert_one(crash).inserted_id

        # Update daily, weekly, monthly, and area collections
        update_collection(daily_crashes, daily_cash, crash_date, "date")
        update_collection(weekly_crashes, weekly_cash, get_week_range(crash_datetime)[0], "start_date")
        update_collection(monthly_crashes, monthly_cash, (crash_date.month, crash_date.year), "month")
        update_collection(areas, area_cash, crash["OCCURRENCE_OF_BEAT"], "area")

        if causes_cash.get(crash["PRIM_CONTRIBUTORY_CAUSE"]) is None:
            cause = {
                "PRIM_CONTRIBUTORY_CAUSE": crash["PRIM_CONTRIBUTORY_CAUSE"],
                "CRASHES_LIST": [crash_id],
                "TOTAL_INJURIES": crash["TOTAL_INJURIES"],
                "FATAL_INJURIES": crash["FATAL_INJURIES"],
                "INCAPACITATING_INJURIES": crash["INCAPACITATING_INJURIES"],
                "INCAPACITATING_NON_INJURIES": crash["INCAPACITATING_NON_INJURIES"]
            }
            causes_cash[crash["PRIM_CONTRIBUTORY_CAUSE"]] = 1
            crashes_causes.insert_one(cause)
        else:
            crashes_causes.update_one(
                {"PRIM_CONTRIBUTORY_CAUSE": crash["PRIM_CONTRIBUTORY_CAUSE"]},
                {
                    "$push": {"CRASHES_LIST": crash_id},
                    "$inc": {
                        "TOTAL_INJURIES": int(crash["TOTAL_INJURIES"]),
                        "FATAL_INJURIES": int(crash["FATAL_INJURIES"]),
                        "INCAPACITATING_INJURIES": int(crash["INCAPACITATING_INJURIES"]),
                        "INCAPACITATING_NON_INJURIES": int(crash["INCAPACITATING_NON_INJURIES"])
                    }
                }
            )

        if injuries_cash.get(crash["PRIM_CONTRIBUTORY_CAUSE"]) is None:
            injury = {
                "area": crash["OCCURRENCE_OF_BEAT"],
                "CRASHES_LIST": [crash_id],
                "injuries_case": crash["TOTAL_INJURIES"] - crash["FATAL_INJURIES"],
                "death_case": crash["FATAL_INJURIES"]
            }
            injuries_cash[crash["PRIM_CONTRIBUTORY_CAUSE"]] = 1
            injuries_by_area_info.insert_one(injury)
        else:
            injuries_by_area_info.update_one(
                {"PRIM_CONTRIBUTORY_CAUSE": crash["PRIM_CONTRIBUTORY_CAUSE"]},
                {
                    "$push": {"CRASHES_LIST": crash_id},
                    "$inc": {
                        "injuries_case": int(crash["TOTAL_INJURIES"]),
                        "death_case": int(crash["FATAL_INJURIES"])
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
        doc = {field_name: key, "amount": 1}
        cache[key] = 1
        collection.insert_one(doc)
    else:
        collection.update_one(
            {field_name: key},
            {"$inc": {"amount": 1}}
        )
