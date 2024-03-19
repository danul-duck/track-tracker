from datetime import datetime
import pytz
import logging

def check_new_record(dttm):
    record_time = datetime.fromisoformat(dttm)
    now = datetime.now(tz=pytz.utc)
    delta = now - record_time
    if delta.total_seconds() < 86400: #12 hours:
        return 'color:rgb(95, 186, 4)'

def format_local_timestamp(dttm):
    time = datetime.fromisoformat(dttm)
    return time.astimezone(pytz.timezone('Europe/London')).strftime("%Y/%m/%d %H:%M:%S")

def format_season(season):
    return season.replace('_',' ').capitalize()
