#Script for oath app to get our map ids of the latest season

import requests 
import json
from os import environ 
import yaml

client_id = environ.get('TRACK_CLIENT_ID','')
client_secret = environ.get('TRACK_CLIENT_SECRET','')

def _get_map_data(uuid, access):
    map_data = requests.get(
        url = f"https://live-services.trackmania.nadeo.live/api/token/map/{uuid}",
        headers = {
            "Authorization": f"nadeo_v1 t={access}",
                "Accept":"application/json",
                }
    )
    return(json.loads(map_data.content)['mapId'])

level2_auth = requests.post(
    headers={"Content-Type": "application/x-www-form-urlencoded"},
    auth = (environ.get('TRACK_USERNAME',''), environ.get('TRACK_PASSWORD','')),
    url="https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic",
    data= {
        "audience" :"NadeoLiveServices"
    }
)
access = json.loads(level2_auth.content)['accessToken']
url = "https://live-services.trackmania.nadeo.live/api/token/campaign/official?offset=0&length=1"
campaigns = requests.get(
        url = url,
        headers = {
            "Authorization": f"nadeo_v1 t={access}",
                "Accept":"application/json",
                }
    )
campaigns= json.loads(campaigns.content)['campaignList'][0]
season = campaigns["name"]
maps = []
for map in campaigns['playlist']:
    _map = {}
    _map['name'] = map['position'] +1
    _map['id'] = _get_map_data(map['mapUid'], access)
    maps.append(_map)

print(f"\n MAP IDS FOR {season} \n")   
print(yaml.dump(maps))


