import os
from . import api
from flask import Blueprint, render_template, current_app
from .models import player, track 
from .db.update_records import update_records
import yaml

bp = Blueprint('app', __name__, url_prefix='/', template_folder='templates')

@bp.route('/')
def home():
    """Default Home list """
    with bp.open_resource('config.yaml','r') as f:
        config = yaml.safe_load(f)
    
    return render_template('home.html', seasons =config['tracks'].keys())

@bp.route('/times/<season>')
def times(season):

    with bp.open_resource('config.yaml','r') as f:
        config = yaml.safe_load(f)
    tracks = [track(track_id= x['id'], track_name = x['name']) for x in config['tracks'][season] ]
    players = [player(player_id=x['id'], player_name=x['name'], nickname = x['nickname']) for x in config['players']]
   
    
    _track_user = os.environ.get('TRACK_USERNAME',"failed")
    _track_password = os.environ.get('TRACK_PASSWORD',"failed")
    current_app.logger.info(f"Searching for times on [{len(tracks)}] tracks" )
    current_app.logger.info(f"For [{len(players)}] players ")
    token = api.auth(bp,_track_user, _track_password)
    track_times = api.get_tracktimes(current_app,
                                    mapList = [x.track_id for x in tracks],
                                    acct_list = [x.player_id for x in players],
                                    token=token
    )
    current_app.logger.debug('\n Found the following track times {}'.format(track_times))
    transposed = normalise_times(track_times, config=config,season=season)
    current_app.logger.debug('\n Transposed to {}'.format(track_times))
    current_app.logger.debug('Rendering template with:')
    current_app.logger.debug('Season: {}'.format(season))
    current_app.logger.debug('Data: {}'.format(dict(sorted(transposed.items()))))

    update_records(records=dict(transposed.items()), season=season)
    return render_template('season.html', season = season, data = dict(sorted(transposed.items()))) 
    

@bp.route('/track/<season>/<track_name>')
def map(season,track_name):

    # Get Map Info:
    current_app.logger.debug(f"Getting map spec for {track_name}")
    with bp.open_resource('config.yaml','r') as f:
        config = yaml.safe_load(f)
    
    track_id = [track['id'] for track in config['tracks'][season] if str(track['name']) == str(track_name) ][0]
    current_app.logger.debug(f"Found id to be {track_id}")
    _track_user = os.environ.get('TRACK_USERNAME',"failed")
    _track_password = os.environ.get('TRACK_PASSWORD',"failed")
    token = api.auth(bp,_track_user, _track_password)
    map_data = api.get_map(bp, track_id, token)
    
    # Then build a graph of the map 
    from .graphs import generate_map_chart
    graph_data = generate_map_chart(season=season,map_name=track_name, map_data=map_data)
    
    return render_template('map.html', data = map_data, chart_data=graph_data)


def normalise_times(raw:dict, config:dict,season:str) -> dict:
    # ToDo : This is a mess, needs a redesign 
    map_names = {}
    for map_uuid in raw.keys():
        for map in config['tracks'][season]: #This should be extensible in 3 months
            if map['id'] == map_uuid:
                map_names[map['name']] = raw[map_uuid]
    player_names = {}
    for track_name in map_names:
        player_names[track_name] = []
        for track_time in map_names[track_name]:
            for player in config['players']:
                if track_time['player'] == player['id']:
                    track_time['nickname'] = player['nickname']
                    player_names[track_name].append (dict(track_time))

    return player_names


if __name__ == "__main__":
    current_app.run(debug=True, host="192.168.68.104", port=5000, threaded=False)
