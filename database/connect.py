from pymongo import MongoClient


client = MongoClient('mongodb://172.31.210.8:27017')
crash_db = client['crash_db']


crashes = crash_db['crashes']
daily_crashes = crash_db['daily_crashes']
weekly_crashes = crash_db['weekly_crashes']
monthly_crashes = crash_db['monthly_crashes']
areas = crash_db['areas']
injuries_by_area_info = crash_db['injuries_info']
crashes_causes = crash_db['crashes_causes']