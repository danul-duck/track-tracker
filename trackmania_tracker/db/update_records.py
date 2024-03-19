import sqlite3 
import os


def update_records(records: dict, season:str): 
    """ Send data to the SQLITE db for analysis/visualing"""
  
    data = _build_values(records)
    sql = """
        INSERT INTO {season} 
        VALUES(?,?,?,?,?) 
        ON CONFLICT DO NOTHING;
    """.format(season=season)
    conn =  sqlite3.connect("main.db")
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()

def _build_values(records):
    import pprint
    from datetime import datetime
    pprint.pprint(records) 

    data = [] 
    for track in records.keys():
        for time in records[track]:
            x = (track, 
                time['nickname'], 
                1, 
                int(datetime.fromisoformat(time['isotime']).timestamp()),
                time['time'] /1000
            )
            data.append(x)

    return data

