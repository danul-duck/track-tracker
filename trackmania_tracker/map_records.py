"""" Util to get the map records data"""
import requests
import json
import os


def live_auth():
    _track_user = os.environ.get('TRACK_USERNAME',"failed")
    _track_password = os.environ.get('TRACK_PASSWORD',"failed")

    level2_auth = requests.post(
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth = (_track_user, _track_password),
        url="https://prod.trackmania.core.nadeo.online/v2/authentication/token/basic",
        data= {
            "audience" :"NadeoLiveServices"
        }
)
    access = json.loads(level2_auth.content)['accessToken']
    return access 

def get_zone_leaders(mapUid, zoneId, access):
    records = requests.get(
        url = f"https://live-services.trackmania.nadeo.live/api/token/leaderboard/group/Personal_Best/map/{mapUid}/top?onlyWorld=false&zoneId={zoneId}",
        headers = {"Authorization": f"nadeo_v1 t={access}"}
    )
    data = json.loads(records.content)
    leader_board = {
        data['tops'][0]['zoneName'] :  data['tops'][0]['top']
    }
    return leader_board

def get_leaderboards(mapUid):
    access =  live_auth()
    zones = {
        "Yorkshire" : "3022a92a-7e13-11e8-8060-e284abfd2bc4",
        "NorthWest" : "3022a6c1-7e13-11e8-8060-e284abfd2bc4",
        "England" : "3022a3c9-7e13-11e8-8060-e284abfd2bc4",
        "UK": "3022a1b2-7e13-11e8-8060-e284abfd2bc4",
        "Europe": "301e2106-7e13-11e8-8060-e284abfd2bc4"
    }
    leader_board = []
    for zone in zones.values():
        leader_board.append(get_zone_leaders(mapUid, zone, access))
    
    #Get World Records 
        records = requests.get(
            url = f"https://live-services.trackmania.nadeo.live/api/token/leaderboard/group/Personal_Best/map/{mapUid}/top?onlyWorld=true&length=5",
            headers = {"Authorization": f"nadeo_v1 t={access}"}
    )
    data = json.loads(records.content)
    worldLeader = {
        data['tops'][0]['zoneName'] :  data['tops'][0]['top']
    }
    leader_board.append(worldLeader)
    print(leader_board)
    return leader_board
        