import socket
from threading import Thread
import json
import ast
import os
from dotenv import load_dotenv
from utils import *


class Peer:

    def __init__(self, peer_host, peer_port):
        self.peer_host = peer_host
        self.peer_port = peer_port

        self.__thread: dict[str, Thread] = {}
        self.__thread["listen"] = Thread(target=self.listen, args=())
        # self.__thread["connectToPeer"] = Thread(target=self.download, agrs=())
        # self.__thread["connectToTracker"] = Thread(target=self.tracker, agrs=())

    def thread_hanldeling(type):
        """Hanlde comming commnad from user"""

    def download(self, magnet_text):
        """Handle download"""
        # self.tracker_socket

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

        # Lấy danh sách các tệp trong thư mục Torrent
        hashcodes = get_magnetTexts_from_torrent()

        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.settimeout(2)
        self.tracker_socket.connect((trackerIP, trackerPort))
        print(f"Connected to tracker for sending hashcodes {trackerIP}:{trackerPort}")

        # Gửi danh sách hashcode cho tracker
        message = (
            "START"
            + " "
            + self.peer_host
            + " "
            + str(self.peer_port)
            + " "
            + " ".join(hashcodes)
        )
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
        message = "UPLOAD " + generate_Torrent(filename)

        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.settimeout(2)
        self.tracker_socket.connect((trackerIP, trackerPort))
        print("connected to upload file")

        self.tracker_socket.send(message.encode())
        print(self.tracker_socket.recv(1024).decode("utf-8"))

    def exit(self, host, port):
        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.settimeout(2)
        self.tracker_socket.connect((trackerIP, trackerPort))
        message = "EXIT" + " " + host + " " + str(port)
        self.tracker_socket.send(message.encode())
        print("Exit success")
