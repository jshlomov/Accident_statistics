from datetime import datetime

from database.connect import crashes, daily_crashes, weekly_crashes, monthly_crashes, areas, injuries_by_area_info, \
    crashes_causes
from repository.csv_repository import get_week_range


def get_all_crashes():
    return list(crashes.find())

def get_all_daily_crashes():
    return list(daily_crashes.find())

def get_all_weekly_crashes():
    return list(weekly_crashes.find())

def get_all_monthly_crashes():
    return list(monthly_crashes.find())

def get_all_areas():
    return list(areas.find())

def get_all_injuries_by_area():
    return list(injuries_by_area_info.find())

def get_all_crash_causes():
    return list(crashes_causes.find())


def get_daily_crashes_by_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    return list(daily_crashes.find({"date": date_obj}))

def get_weekly_crashes_by_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    start_week, _ = get_week_range(date_obj)
    return list(weekly_crashes.find({"start_date": start_week}))

def get_monthly_crashes_by_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return list(monthly_crashes.find({"month": (date_obj.month, date_obj.year)}))

def get_injuries_by_area(area_name):
    return list(injuries_by_area_info.find({"area": area_name}))
