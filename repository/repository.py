from database.connect import crashes, daily_crashes, weekly_crashes, monthly_crashes, areas, injuries_by_area_info, \
    crashes_causes


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