from .db.get_records import get_records
from itertools import groupby
def generate_map_chart(season,map_name, map_data):
    sql =f"SELECT player, DATETIME(dttm,'unixepoch'), record FROM {season} WHERE track = {map_name}"
    print(sql)
    records = get_records(sql)

    grouped = groupby(records, lambda x: x[0])

    records_dict = {}
    for player, record in grouped:
        records_dict[player] = [{'x':x[1],'y':x[2]} for x in record]
    
    for player in records_dict:
        print(player)
        print(records_dict[player])
    return records_dict



if __name__ == '__main__':
    from models import track

    map = track(track_id=1,
                track_name="1",
                image_url="localhost:443",
                bronze = 34000,
                silver=32000, 
                gold=30000,
                author=27000 
                )
    
    generate_map_chart('autumn_23',map)


