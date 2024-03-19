from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
@dataclass
class player:
    player_id: str
    player_name: str 
    nickname: str

@dataclass
class track:
    track_id: str
    track_name: str
    image_url: Optional[str] =None
    bronze: Optional[int] = None
    silver: Optional[int] = None
    gold: Optional[int] = None
    author: Optional[int] = None
    leader_boards: Optional[List] = None
    

# @dataclass
# class TrackRecord():
#     track_name: str
#     time: dict(str)
#     user_name: str
#     isotime: str
    
#     def __post_init__(self):
#         self.dttm: datetime.fromisoformat(self.isotime)

