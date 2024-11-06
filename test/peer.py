import socket
from threading import Thread, Lock
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

        self.magnet_text_list = {}
        # self.messageTracker = queue.Queue()
        self.messagePeer = queue.Queue()

        self.__thread: dict[str, Thread] = {}
        self.__thread["listen"] = Thread(target=self.listen, args=())
        # self.__thread["connectToPeer"] = Thread(target=self.ThreadDownload, args=(magnetText))

    # ---------PEER CONNECTION INTERACTION-------------#

    def make_connection_to_peer(self, peer):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.settimeout(2)
        peer_socket.connect((peer[0], int(peer[1])))
        return peer_socket

    def download_status_from_peer(self, peer, data_torrent, status, lock):
        """Download the status"""
        peer_socket = self.make_connection_to_peer(peer)
        print("Make connect to peer to get status {} : {}".format(peer[0], peer[1]))
        message = "STATUS " + data_torrent["magnetText"]
        peer_socket.send(message.encode())
        res = peer_socket.recv(1024000).decode("uft-8")
        # print(res)
        with lock:
            status.append(res)
        peer_socket.close()

    def download_pieces_from_peer(self, peer, piece_count, data_torrent):
        """Download the piece"""
        peer_socket = self.make_connection_to_peer(peer)
        print("Make connect to peer to get piece {} : {}".format(peer[0], peer[1]))
        message = "PIECE " + str(piece_count) + " " + data_torrent["magnet_text"]
        peer_socket.send(message.encode())
        res = peer_socket.recv(1024000).decode("uft-8")
        create_temp_file(res, piece_count, data_torrent)

    def DownloadProcess(self, peerList, data_torrent):
        """Handle download process for each peer in the peerList"""
        threadsStatus = []
        threadsPiece = []
        status = []
        lock = Lock()
        # Tạo thread cho mỗi peer
        for peer in peerList:
            thread = Thread(
                target=self.download_status_from_peer,
                args=(peer, data_torrent, status, lock),
            )
            threadsStatus.append(thread)
            thread.start()

        # Chờ tất cả các thread hoàn thành
        for thread in threadsStatus:
            thread.join()

        print(status)
        # piece_count = 0
        # # Tao thread de download cac piece cua file
        # for peer in peerList:
        #     thread = Thread(target=self.download_pieces_from_peer, args=(peer, piece_count, data_torrent))
        #     threadsPiece.append(thread)
        #     thread.start()
        #     piece_count += 1

        # for thread in threadsPiece:
        #     thread.join()

        # merge_temp_files("ouput.txt", data_torrent['metaInfo']['name'])

    def download(self, magnet_text):
        """Handle download"""

        data_torrent, peer_list = self.download_torrent_from_tracker(magnet_text)

        filename = data_torrent["metaInfo"]["name"]
        if data_torrent["magnetText"] not in self.magnet_text_list:
            create_torrent_file(filename, data_torrent)
        else:
            print("You already have torrent")

        print(
            "Your download is being process, enter 6 to see detail {}".format(peer_list)
        )

        downloadThread = Thread(
            target=self.DownloadProcess, args=(peer_list, data_torrent)
        )
        downloadThread.start()

    # -------------------------------------------------#

    # -------------PEER LISTENING INTERACTION------------#

    def handle_status(self, recv_socket: socket.socket, src_addr, magnetText):
        """Handle status"""
        filename = self.magnet_text_list[magnetText]
        with open("./Torrent/" + filename, "r") as file:
            torrent_file = file.read()
        status = check_file(filename, torrent_file)

        recv_socket.sendall(str(status).encode("utf-8"))

    def listen(self):
        """
        Listen on the opening socket and create a new thread whenever it accepts a connection (listen peer connect ?!).
        """
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.peer_host, self.peer_port))
        print("Succes listening")
        print(self.listen_socket.getsockname())
        self.listen_socket.listen(5)
        while True:
            try:
                recv_socket, src_addr = self.listen_socket.accept()
                print("connected")
                message = recv_socket.recv(1024000).decode("utf-8")
                if message.startswith("STATUS"):
                    self.handle_status(recv_socket, src_addr, message[7:])

            except OSError:
                break

    # -------------------------------------------#

    # ---------------------------------------------------#

    # -----------TRACKER INTERACTION-------------#

    def start(self):
        """start server listen thread"""
        self.send_torrent_hashcodes(trackerIP, trackerPort)
        self.__thread["listen"].start()

    def send_torrent_hashcodes(self, trackerIP, trackerPort):

        # Lấy danh sách các tệp trong thư mục Torrent
        self.magnet_text_list = get_magnetTexts_from_torrent()
        keys = list(self.magnet_text_list.keys())
        if len(keys) == 0:
            return

        tracker_socket = self.make_connection_to_tracker()
        print(f"Connected to tracker for sending hashcodes {trackerIP}:{trackerPort}")

        # Gửi danh sách hashcode cho tracker
        message = (
            "START"
            + " "
            + self.peer_host
            + " "
            + str(self.peer_port)
            + " "
            + " ".join(keys)
        )
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

        message = (
            "UPLOAD "
            + self.peer_host
            + " "
            + str(self.peer_port)
            + " "
            + generate_Torrent(filename)
        )
        print(message)
        tracker_socket.send(message.encode())
        print(tracker_socket.recv(1024).decode("utf-8"))

        create_torrent_file(
            filename.split(".")[0], json.loads(generate_Torrent(filename))
        )
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
        self.__thread["listen"].join()
        print("Exit success")

    def download_torrent_from_tracker(self, magnet_text):
        tracker_socket = self.make_connection_to_tracker()
        print(f"Connected to tracker for download torrent {trackerIP}:{trackerPort}")

        message = (
            "DOWNLOAD " + self.peer_host + " " + str(self.peer_port) + " " + magnet_text
        )
        print(message)
        tracker_socket.send(message.encode())

        #  hanlde respond from tracker
        res = tracker_socket.recv(1024000).decode("utf-8")
        data_torrent = json.loads(res)["torrent_file"]
        data_list = json.loads(res)["peer_list"]
        tracker_socket.close()
        return data_torrent, data_list

    # -------------------------------------------#
