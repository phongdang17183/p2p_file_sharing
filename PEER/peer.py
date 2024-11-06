import socket
from threading import Thread
import json
import ast
import os
import queue
from dotenv import load_dotenv
from utils import *

class Peer:

    def __init__(self, peer_host, peer_port):
        self.peer_host = peer_host
        self.peer_port = peer_port
        
        # self.messageTracker = queue.Queue()
        self.messagePeer = queue.Queue()
        
        self.__thread: dict[str, Thread] = {}
        self.__thread["listen"] = Thread(target=self.listen, args=())
        self.__thread["connectToPeer"] = Thread(target=self.PeerProcess, args=(magnetText))
    
    #---------PEER CONNECTION INTERACTION-------------#
    
    def DownloadProcess(self):
        """Hanlde download process"""
        

    def download(self, magnet_text):
        """Handle download"""
        tracker_socket = self.make_connection_to_tracker()
        print(f"Connected to tracker for download torrent {trackerIP}:{trackerPort}")
        
        message = "DOWNLOAD " + magnet_text 
        print(message)
        tracker_socket.send(message.encode())
        
        res = tracker_socket.recv(1024).decode("utf-8")
        PeerListForDownloadFile = ast.literal_eval(res)
        tracker_socket.close()
        
        downloadThread = Thread(target=self.DownloadProcess, args=(PeerListForDownloadFile, magnet_text))
        downloadThread.start()
        downloadThread.join()
    #-------------------------------------------------#      
    
    
    
    #-------------PEER LISTENING INTERACTION------------#
    
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

    #-------------------------------------------#
    
    #---------------------------------------------------# 
    
    
    
    #-----------TRACKER INTERACTION-------------#

    def start(self): 
        """start server listen thread"""
        self.send_torrent_hashcodes(trackerIP, trackerPort)
        self.__thread["listen"].start()
        
    def send_torrent_hashcodes(self, trackerIP, trackerPort):
       
        # Lấy danh sách các tệp trong thư mục Torrent
        hashcodes = get_magnetTexts_from_torrent()  
       
        tracker_socket = self.make_connection_to_tracker()
        print(f"Connected to tracker for sending hashcodes {trackerIP}:{trackerPort}")
        
        # Gửi danh sách hashcode cho tracker
        message = "START" + " " + self.peer_host + " " + str(self.peer_port) + " " + " ".join(hashcodes)
        print(message)   
        tracker_socket.send(f"{message}".encode())
        tracker_socket.close()
        print("Sent success")
        
    def get_all_file(self):
        """Fetch all file from Tracker"""
        
        tracker_socket = self.make_connection_to_tracker()
        print(f"Connected to get all file {trackerIP}:{trackerPort}")
       
        message = "FETCH ALL TORRENT"
        tracker_socket.send(message.encode())
        res = tracker_socket.recv(1024).decode("utf-8")
        Files = ast.literal_eval(res)
        tracker_socket.close()
        return Files
            
    def upload_Torrent(self, filename):
        """upload torrent for tracker"""
        tracker_socket = self.make_connection_to_tracker()
        print("connected to upload file")
        
        message = "UPLOAD " + generate_Torrent(filename)
        
        tracker_socket.send(message.encode())
        print(tracker_socket.recv(1024).decode("utf-8"))
        tracker_socket.close()

    def make_connection_to_tracker(self):
        """connect to tracker"""
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.settimeout(2)
        tracker_socket.connect((trackerIP, trackerPort))
        return tracker_socket
    
    def exit(self, host, port):
        tracker_socket = self.make_connection_to_tracker()
        message = "EXIT" + " " + host + " " + str(port)
        tracker_socket.send(message.encode())
        tracker_socket.close()
        print("Exit success")
        
    #-------------------------------------------#
        
        