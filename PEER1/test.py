import requests
# from peer import *
from utils import *

def start_api():
        url= "http://localhost:3000/tracker/start"
        lists = get_magnetTexts_from_torrent()
        print(type(lists))
        list = [listM for listM in lists]
        print(list)
        params = {
            "peerIp": "123",
            "peerPort": 123,
            "magnetList": list
        }
        
        response = requests.post(url, json=params)
        print(response.json())

def get_all_file_api():
    url= "http://localhost:3000/tracker/getAllTorrents"
    response = requests.get(url)
    print(response.json()[0]["filename"])
    
def exit_api():
    url = "http://localhost:3000/tracker/exit"
    param ={
        "peerIp":"1",
        "peerPort": 6880
    }
    response = requests.post(url, json=param)
    print(response.json())

def upload_api(filename = "text.txt"):
    try:
        data = generate_Torrent(filename) 
        if data is None:
            return
       
        data = json.loads(data)
        url = "http://localhost:3000/tracker/upload"

        param = {
            "peerIp": "12",
            "peerPort": 6880,
            "Torrent": data
        }
        

        response = requests.post(url, json=param)
        print((response.status_code))
    except Exception:
        print(Exception)
    
def download_torrent_from_tracker_api(magnettext):
    url = "http://localhost:3000/tracker/download"
    param ={
        "peerIp": "1",
        "peerPort": 6880,
        "magnetText": magnettext
    }
    response = requests.get(url, json=param)
    
    print(type(response.json()['listPeer']))
    print(type(response.json()['torrent']))
    
    
    
# start_api()
# get_all_file_api()
# exit_api()
# upload_api()
download_torrent_from_tracker_api("71c5f41076ce5d94666964d1c507b537d82f7c7b8697cccaf3fac0dfdb2df505")
