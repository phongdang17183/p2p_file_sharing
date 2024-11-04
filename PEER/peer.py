import socket
from threading import Thread
# from message import *
import requests
import json
import os
# from utils import *
# from apitracker import TrackerSite


class Peer:

    def __init__(self, peer_host, peer_port):
        # self.peer_id = None
        self.peer_host = peer_host
        self.peer_port = peer_port

        self.__thread: dict[str, Thread]
        self.__thread["listen"] = Thread(target=self.listen, args=())
        # self.__thread["connectToAnotherPeer"] = Thread(target=)

    # def con
    def handle_incoming_connection(self, recv_socket, src_addr):
        """
        Handle a new connection and pass the message to the appropriate function (for peer connect peer ?!).
        include PING
        """
        print("handle_incoming_connection")

    def listen(self):
        """
        Listen on the opening socket and create a new thread whenever it accepts a connection (listen peer connect ?!).
        """
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.peer_host, self.peer_port))
        print(self.listen_socket.getsockname())
        self.listen_socket.listen(5)
        while True:
            try:
                recv_socket, src_addr = self.listen_socket.accept()
                new_thread = Thread(
                    target=self.handle_incoming_connection, args=(recv_socket, src_addr)
                )
                new_thread.start()
            except OSError:
                break

    # def connectToTrackerForPeerID(self, trackerId, trackerPort):
    #     self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.tracker_socket.connect((trackerId, trackerPort))
    #     print(f"Connected to tracker for peerId{trackerId}:{trackerPort}")
    #     # Gui request cho tracker
    #     self.tracker_socket.send(b"REQUEST_PEERID")  
    #     # Nhận peerID từ tracker
    #     peer_id = self.tracker_socket.recv(1024).decode()
    #     print(f"Received peerID: {peer_id}")
    #     # Lưu peerID vào thuộc tính
    #     self.peer_id = peer_id

    def send_torrent_hashcodes(self, trackerIP, trackerPort):
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.connect((trackerIP, trackerPort))
        print(f"Connected to tracker for sending hashcodes {trackerIP}:{trackerPort}")
        torrent_folder = './Torrent'
        
        # Lấy danh sách các tệp trong thư mục Torrent
        files = os.listdir(torrent_folder)
        
        # Lọc các tệp JSON
        hashcodes = []
        for file_name in files:
            if file_name.endswith('.json'):
                try:
                    with open(os.path.join(torrent_folder, file_name), 'r') as file:
                        data = json.load(file)
                        hashcode = data.get("hashcode", None)
                        if hashcode:
                            hashcodes.append(hashcode)
                except json.JSONDecodeError:
                    print(f"Lỗi định dạng JSON trong tệp {file_name}. Bỏ qua tệp này.")    
                except Exception as e:
                    print(f"Lỗi không xác định khi đọc tệp {file_name}: {e}")
        
        # Gửi danh sách hashcode cho tracker
        torrents = ""
        torrents = " ".join(hashcodes)
        print(torrents)   
        self.tracker_socket.send(f"{torrents}".encode())
        
        print("Sent all hashcodes to tracker")

    def connectToTrackerGetAllFile(self, trackerId, trackerPort):
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.connect((trackerId, trackerPort))
        print(f"Connected to get all file {trackerId}:{trackerPort}")
        # connect to get a respond magnet text (all file from tracker)
        # return []files