import socket
from threading import Thread
# from message import *
import requests
import json
import ast
import os
from dotenv import load_dotenv
import hashlib
# from utils import *
# from apitracker import TrackerSite

load_dotenv()
trackerIP = os.getenv('TRACKERIP')
trackerPort = int(os.getenv('TRACKERPORT'))


class Peer:

    def __init__(self, peer_host, peer_port):
        # self.peer_id = None
        self.peer_host = peer_host
        self.peer_port = peer_port

        self.__thread: dict[str, Thread] = {}
        self.__thread["listen"] = Thread(target=self.listen, args=())
        # self.__thread["connectToAnotherPeer"] = Thread(target=self.download, agrs=())

    def download(self, magnet_text):
        """Handle download"""
        self.tracker_socket
        
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
        print("Succes listening")
        print(self.listen_socket.getsockname())
        self.listen_socket.listen(5)
        self.listen_socket.settimeout(2)
        while True:
            try:
                recv_socket, src_addr = self.listen_socket.accept()
                new_thread = Thread(
                    target=self.handle_incoming_connection, args=(recv_socket, src_addr)
                )
                new_thread.start()
            except OSError:
                break

    def send_torrent_hashcodes(self, trackerIP, trackerPort):
        path = os.path.dirname(__file__)
        fullpath = os.path.join(path, "Torrent")
       
        # Lấy danh sách các tệp trong thư mục Torrent
        hashcodes = []
        files = os.listdir(fullpath)
        if (len(files) == 0):
            print("You dont have any torrent yet")
        else:   
            # Lọc các tệp JSON
            for file_name in files:
                if file_name.endswith('.json'):
                    try:
                        with open(os.path.join(fullpath, file_name), 'r') as file:
                            data = json.load(file)
                            hashcode = data.get("hashcode", None)
                            if hashcode:
                                hashcodes.append(hashcode)
                    except json.JSONDecodeError:
                        print(f"Lỗi định dạng JSON trong tệp {file_name}. Bỏ qua tệp này.")    
                    except Exception as e:
                        print(f"Lỗi không xác định khi đọc tệp {file_name}: {e}")
        
       
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(trackerIP, trackerPort)
        self.tracker_socket.settimeout(2)
        self.tracker_socket.connect((trackerIP, trackerPort))
        print(f"Connected to tracker for sending hashcodes {trackerIP}:{trackerPort}")
        
        # Gửi danh sách hashcode cho tracker
        message = "START" + " " + self.peer_host + " " + str(self.peer_port) + " " + " ".join(hashcodes)
        print(message)   
        self.tracker_socket.send(f"{message}".encode())
        
        print("Sent success")
        
    def get_all_file(self):
        """Fetch all file from Tracker"""
        
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.settimeout(2)
        self.tracker_socket.connect((trackerIP, trackerPort))
        print(f"Connected to get all file {trackerIP}:{trackerPort}")
        # connect to get a respond magnet text (all file from tracker)
        # return []files
        message = "FETCH ALL TORRENT"
        self.tracker_socket.send(message.encode())
        res = self.tracker_socket.recv(1024).decode("utf-8")
        Files = ast.literal_eval(res)
        return Files
        
    def start(self):
        
        """start server listen thread"""
        self.send_torrent_hashcodes(trackerIP, trackerPort)
        self.__thread["listen"].start()

    def upload_Torrent(self, filename):
        """upload torrent for tracker"""
        path = os.path.dirname(__file__)
        fullpath = os.path.join(path, "MyFolder", filename)
        
        try:
            magnet_text, pieces, size, piece_size = self.hash_function(fullpath)
            data = {
                "trackerIp": trackerIP,
                "magnetText": magnet_text,
                "metaInfo": {
                    "name": filename,
                    "filesize": size,
                    "piece_size": piece_size,
                    "pieces": pieces
                }
            }
            json_data = json.dumps(data)
            message = "UPLOAD " + json_data
            self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tracker_socket.settimeout(2)
            self.tracker_socket.connect((trackerIP, trackerPort))
            print("connected to upload file")
            
            self.tracker_socket.send(message.encode())
            print(self.tracker_socket.recv(1024).decode("utf-8"))
            
            
        except FileNotFoundError:
                print("Không tìm thấy tệp!")
        
    def hash_function(self, filepath , piece_size=4):
        piece_hashes = []
        hashinfo = hashlib.sha1()
        size =  os.stat(filepath).st_size
        with open(filepath, 'rb') as f:
            while True:
                piece = f.read(piece_size)
                if not piece:
                    break 
                
                piece_hash = hashlib.sha1(piece).digest()  
                piece_hashes.append(piece_hash.hex())
                hashinfo.update(piece_hash)
                
        return hashinfo.hexdigest(), piece_hashes, size, piece_size
        
    def exit(self, host, port):
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.settimeout(2)
        self.tracker_socket.connect((trackerIP, trackerPort))
        message = "EXIT" + " " + host + " " + str(port)
        self.tracker_socket.send(message.encode())
        print("Exit success")
        
        