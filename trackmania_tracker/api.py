import requests
import os 
import json
from itertools import groupby
import logging
from . models import track
from .map_records import get_leaderboards
from flask import current_app
def auth(app,_track_user, _track_password):

    response = requests.post(
        url="https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic",
        headers= {
            "Content-Type": "application/json"
        },
        auth = (_track_user, _track_password),
        json= {"audience" : "NadeoServices"}

    )
    if response.status_code != 200:
        raise Exception(f'Failed to get access token \n [{response.status_code}] \n {response.content}')
    jwt = json.loads(response.content)
    access_token = jwt.get('accessToken')
    refresh_token = jwt.get('refreshToken')
    return refresh_token, access_token

def refresh_token(token):
    response = requests.get(
        url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/refresh",
        headers = {"Authorization": f"nadeo_v1 t={token[0]}"}
    )  
    if response.status_code != 200:
       raise Exception(f'Failed to refresh token, giving up')
    
    jwt = json.loads(response.content)
    access_token = jwt.get('accessToken')
    refresh_token = jwt.get('refreshToken')
    
    return refresh_token, access_token

def get_tracktimes(app,mapList, acct_list, token):    
    
    app.logger.debug("Searaching for the following players {}".format(acct_list))
    app.logger.debug("On the following tracks {}".format(mapList))
    response = requests.get(
        url = f"https://prod.trackmania.core.nadeo.online/mapRecords/?accountIdList={','.join(acct_list)}&mapIdList={','.join(mapList)}",
        headers = {"Authorization": f"nadeo_v1 t={token[1]}"}
    )
    if response.status_code != 200:
        print('Unknown error occured')
        raise Exception(f"[{response.status_code}]: {response.content}")
    data = json.loads(response.content)
    sort = sorted(data, key=lambda x: x.get('mapId'))
    grouped = groupby(sort, lambda x: x.pop('mapId') )
    
    trackRecords = {}
    for map, records in grouped:
        trackRecords[map] = []
        for row in records:
            trackRecords[map].append( {
                                    "player":row.get('accountId'), 
                                    "time" : row.get('recordScore',{}).get('time',-1), 
                                    "medal": str(row.get('medal')),
                                    "isotime":row.get('timestamp')
                                    } )
    app.logger.debug(trackRecords)
    return trackRecords

def get_map(app, map_id, token):
    current_app.logger.debug(f"Seeking map data from https://prod.trackmania.core.nadeo.online/maps?mapIdList={map_id}")
    response = requests.get(
        url = f"https://prod.trackmania.core.nadeo.online/maps?mapIdList={map_id}",
        headers = {"Authorization": f"nadeo_v1 t={token[1]}"}
    )
    if response.status_code != 200:
        print('Unknown error occured')
        raise Exception(f"[{response.status_code}]: {response.content}")
    
    data = json.loads(response.content)[0]

    return track(track_id=map_id,
                 track_name=data['name'],
                 image_url=data['thumbnailUrl'],
                 bronze=data['bronzeScore'],
                 silver=data['silverScore'],                 
                 gold=data['goldScore'],
                 author=data['authorScore'], 
                 leader_boards = get_leaderboards(data['mapUid'])
            )

if __name__ == '__main__':
    
   
    print("authorising...")
    token = auth()
    print("---------")
    trackRecords = get_tracktimes(["a93f902b-16a1-4448-ad34-65cf32d41425","7b9373ad-b754-4c6d-9abf-7304517ba96e"],
                                  ['45abb7ea-fb19-4d82-bf22-87afd7f69354','3e3ebf52-90fb-4c88-bf85-c02e3a0a9e6d','303fcb4e-ccac-4a03-a63b-e562ef818aa3'],token)
    