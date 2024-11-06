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
        self.running = True
        self.peer_host = peer_host
        self.peer_port = peer_port

        self.magnet_text_list = {}
        # self.messageTracker = queue.Queue()
        # self.messagePeer = queue.Queue()

        # self.__thread: dict[str, Thread] = {}
        # self.__thread["listen"] = Thread(target=self.listen, args=())
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
        res = peer_socket.recv(1024000).decode("utf-8")
        res = res + " " + str(peer)

        with lock:
            status.append(res)
        peer_socket.close()

    def download_pieces_from_peer(self, peer, piece_count, data_torrent):
        """Download the piece"""
        peer_socket = self.make_connection_to_peer(peer)
        print("Make connect to peer to get piece {} : {}".format(peer[0], peer[1]))
        message = "PIECE " + str(piece_count) + " " + data_torrent["magnet_text"]
        peer_socket.send(message.encode())
        res = peer_socket.recv(1024000).decode("utf-8")

        create_temp_file(res, piece_count, data_torrent)

    def DownloadProcess(self, peerList, data_torrent):
        """Handle download process for each peer in the peerList"""

        # get status

        threadsStatus = []
        threadsPiece = []
        list_status = []
        lock = Lock()
        # Tạo thread cho mỗi peer
        for peer in peerList:
            thread = Thread(
                target=self.download_status_from_peer,
                args=(peer, data_torrent, list_status, lock),
            )
            threadsStatus.append(thread)
            thread.start()

        # Chờ tất cả các thread hoàn thành
        for thread in threadsStatus:
            thread.join()

        piece_to_peer = contruct_piece_to_peers(list_status)
        print(piece_to_peer)

        # get piece
        try:
            for piece in piece_to_peer:
                thread = Thread(
                    target=self.download_pieces_from_peer,
                    args=(piece_to_peer[piece], piece, data_torrent),
                )
                threadsPiece.append(thread)
                thread.start()

            for thread in threadsPiece:
                thread.join()

        except Exception as e:
            print(e)

        merge_temp_files("./Download", data_torrent["metaInfo"]["name"])
        print("Download complete")

    def download(self, magnet_text):
        """Handle download"""

        data_torrent, peer_list = self.download_torrent_from_tracker(magnet_text)

        filename = data_torrent["metaInfo"]["name"]
        if data_torrent["magnetText"] not in self.magnet_text_list:
            create_torrent_file(filename.split(".")[0], data_torrent)
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
        filename = filename.split(".")[0] + ".json"
        path = os.path.dirname(__file__)
        fullpath = os.path.join(path, "Torrent", filename)
        with open(fullpath, "r") as file:
            torrent_file = file.read()
            status = check_file(filename, json.loads(torrent_file))
            print(status)
            send_socket = recv_socket.sendall(str(status).encode("utf-8"))
            print(send_socket)

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
        while self.running:
            try:
                recv_socket, src_addr = self.listen_socket.accept()

                print("connected from {}".format(src_addr))
                message = recv_socket.recv(1024000).decode("utf-8")

                handle_listen = Thread(
                    target=self.handle_listen, args=(recv_socket, src_addr, message)
                )
                handle_listen.start()

            except Exception:
                continue

    def handle_listen(self, recv_socket: socket.socket, src_addr, message):
        if message.startswith("STATUS"):
            self.handle_status(recv_socket, src_addr, message[7:])
        else:
            self.handle_piece(recv_socket, src_addr, message[6:])

    def handle_piece(self, recv_socket: socket.socket, src_addr, message):
        """send piece"""

        piece_index, magnet_text = message.split(" ")
        filename = self.magnet_text_list[magnet_text].split(".")[0] + ".json"
        piece_index = int(piece_index)

        path = os.path.dirname(__file__)

        torrent_file = open(os.path.join(path, "Torrent", filename), "r").read()
        piece_size = torrent_file["metaInfo"]["piece_size"]

        fullpath = os.path.join(path, "MyFolder", filename)
        with open(fullpath, "r") as file:

            file.seek(piece_index * piece_size)
            piece = file.read(piece_size)
            if not check_sum_piece(
                piece, torrent_file["metaInfo"]["pieces"], piece_index
            ):
                raise Exception
            recv_socket.sendall(piece.encode("utf-8"))

    # -------------------------------------------#

    # ---------------------------------------------------#

    # -----------TRACKER INTERACTION-------------#

    def start(self):
        """start server listen thread"""
        self.send_torrent_hashcodes(trackerIP, trackerPort)
        listen_thread = Thread(target=self.listen, args=())
        listen_thread.start()
        # self.__thread["listen"].start()

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
        res = tracker_socket.recv(1024).decode("utf-8")
        if res != "File already exists":
            create_torrent_file(
                filename.split(".")[0], json.loads(generate_Torrent(filename))
            )

        magnet_text = json.loads(generate_Torrent(filename))["magnetText"]
        self.magnet_text_list[magnet_text] = filename
        print(self.magnet_text_list)

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
        self.running = False
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
