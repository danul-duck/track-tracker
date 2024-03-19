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
url = "https://live-services.trackmania.nadeo.live/api/token/club?length=5&offset=3name=cloob"
clubs = requests.get(
        url = url,
        headers = {
            "Authorization": f"nadeo_v1 t={access}",
                "Accept":"application/json",
                }
    )

print(clubs.content)

