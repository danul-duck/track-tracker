import sqlite3 
import os


def get_records(sql:str): 
    """ Send data to the SQLITE db for analysis/visualing"""

    conn =  sqlite3.connect("main.db")
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

if __name__ == '__main__':
    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class track:
        track_id: str
        track_name: str
        image_url: Optional[str] =None
        bronze: Optional[int] = None
        silver: Optional[int] = None
        gold: Optional[int] = None
        author: Optional[int] = None
    
    map_data = track(track_id=1,
                track_name="1",
                image_url="localhost:443",
                bronze = 34000,
                silver=32000, 
                gold=30000,
                author=27000 
                )
    season = 'autumn_23'
    

    
    
    
    print(get_records(sql))