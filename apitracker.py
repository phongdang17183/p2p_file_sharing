import requests
import json

TRACKER_URL = "http://localhost:8080"

"""
Tracker need return in format:
{
"Failure reason":  "" (may be null),
"Warning":  "" (may be null),
"Success": 
    {
    "Peer ID": tracker_id,
    "Peer IP": peer_ip,
    "Peer Port": peer_port,
    }
}
"""


class TrackerSite:
    """Interface to interact with tracker with api"""

    @staticmethod
    def post(data):
        """Post method to send data to tracker, return like this"""
        response = requests.post(TRACKER_URL, data)
        print(response.json())

    @staticmethod
    def get(data):
        """get method to send data to tracker, if ok return respone, else return None"""
        response = requests.get(TRACKER_URL, data)
