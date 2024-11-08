import socket
from threading import Thread, Lock
import json
import ast
import os
from utils import *
import random
import time


class Peer:

    def __init__(self, peer_host, peer_port):
        self.running = True

        self.peer_host = peer_host
        self.peer_port = peer_port

        self.magnet_text_list = {}

    # ---------PEER CONNECTION INTERACTION-------------#

    def make_connection_to_peer(self, peer):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.settimeout(2)
        peer_socket.connect((peer[0], int(peer[1])))
        return peer_socket

    def download_status_from_peer(self, peer, data_torrent, status, lock):
        """Download the status from peer"""
        peer_socket = self.make_connection_to_peer(peer)

        print("Make connect to peer to get status {} : {}".format(peer[0], peer[1]))

        message = "STATUS " + data_torrent["magnetText"]
        peer_socket.sendall(message.encode())
        res = peer_socket.recv(8192).decode()
        peer_socket.close()

        res = res + " " + str(peer)
        with lock:
            status.append(res)

    def download_pieces_from_peer(
        self, ListPeer, piece_index, data_torrent, downloaded_status
    ):
        """Download the piece"""
        for peer in ListPeer:

            message = "PIECE " + str(piece_index) + " " + data_torrent["magnetText"]

            peer_socket = self.make_connection_to_peer(peer)
            print("Make connect to peer to get piece {} : {}".format(peer[0], peer[1]))
            peer_socket.sendall(message.encode())
            res = peer_socket.recv(8192)
            peer_socket.close()

            # If send False
            if res == b"False":
                return

            print(res.decode())

            if create_temp_file(res, piece_index, data_torrent):
                downloaded_status[piece_index] = True
                break

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

        # {0: true,
        #  1: fale }

        downloaded_status = [False] * len(piece_to_peer)
        timeout = time.time() + 10
        # get piece
        try:

            while time.time() < timeout:
                # while True:
                for piece_index in piece_to_peer:
                    if downloaded_status[piece_index] == False:
                        random.shuffle(piece_to_peer[piece_index])
                        print(piece_to_peer[piece_index])
                        thread = Thread(
                            target=self.download_pieces_from_peer,
                            args=(
                                piece_to_peer[piece_index],
                                piece_index,
                                data_torrent,
                                downloaded_status,
                            ),
                        )
                        threadsPiece.append(thread)
                        thread.start()

                for thread in threadsPiece:
                    thread.join()

                if False in downloaded_status:
                    continue
                else:
                    break

        except Exception as e:
            print("something when wrong in download process : {}".format(e))

        name = data_torrent["metaInfo"]["name"]
        merge_temp_files(name, data_torrent["metaInfo"]["name"])
        print("Download complete")

    def download(self, magnet_text):
        """Handle download"""
        try:
            data_torrent, peer_list = self.download_torrent_from_tracker(magnet_text)
        except Exception:
            return

        if data_torrent["magnetText"] not in self.magnet_text_list:
            filename = data_torrent["metaInfo"]["name"]
            filenameTorrent = filename.split(".")[0] + ".json"
            self.magnet_text_list[data_torrent["magnetText"]] = filenameTorrent
            create_torrent_file(filename, data_torrent)
        else:
            print("You already have torrent")

        print("Your download is being process, peerList: {}".format(peer_list))

        if len(peer_list) == 0:
            print("There's no seeder online now pls try nater")
            return

        downloadThread = Thread(
            target=self.DownloadProcess, args=(peer_list, data_torrent)
        )
        downloadThread.start()

    # ---------PEER CONNECTION INTERACTION-------------#

    # ---------------------------------------------------#

    # -------------PEER LISTENING INTERACTION------------#

    def handle_status(self, recv_socket: socket.socket, src_addr, magnetText):
        """Handle status"""
        filenameTorrent = self.magnet_text_list[magnetText]

        path = os.path.dirname(__file__)
        fullpath = os.path.join(path, "Torrent", filenameTorrent)
        try:
            with open(fullpath, "r") as file:
                torrent_file = file.read()
                status = check_file(json.loads(torrent_file))
                print(status)
                recv_socket.sendall(str(status).encode())

        except Exception as e:
            print("something when wrong when handle status listen: {}".format(e))

    def listen(self):
        """
        Listen on the opening socket and create a new thread whenever it accepts a connection (listen peer connect ?!).
        """
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.peer_host, self.peer_port))
        print("Succes listening")
        print(self.listen_socket.getsockname())
        self.listen_socket.listen(50)
        self.listen_socket.settimeout(10)
        while self.running:
            try:
                recv_socket, src_addr = self.listen_socket.accept()

                print("connected from {}".format(src_addr))
                message = recv_socket.recv(8192).decode("utf-8")

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
        """Seeder send piece"""
        print("--------piece dowload------")
        piece_index, magnet_text = message.split(" ")

        filenameTorrent = self.magnet_text_list[magnet_text]

        piece_index = int(piece_index)

        path = os.path.dirname(__file__)

        torrent_file = json.loads(
            open(os.path.join(path, "Torrent", filenameTorrent), "r").read()
        )

        filename = torrent_file["metaInfo"]["name"]
        piece_size = int(torrent_file["metaInfo"]["piece_size"])

        fullpath = os.path.join(path, "MyFolder", filename)
        piece = None
        with open(fullpath, "rb") as file:
            file.seek(piece_index * piece_size)
            piece = file.read(piece_size)

            if (
                check_sum_piece(piece, torrent_file["metaInfo"]["pieces"], piece_index)
                == False
            ):
                recv_socket.sendall(str("False").encode())
            else:
                recv_socket.sendall(piece)

    # -------------------------------------------#

    # ---------------------------------------------------#

    # -----------TRACKER INTERACTION-------------#

    def start(self):
        """start server listen thread"""
        print(trackerIP, trackerPort)
        self.send_torrent_hashcodes(trackerIP, trackerPort)
        listen_thread = Thread(target=self.listen, args=())
        listen_thread.start()

    def send_torrent_hashcodes(self, trackerIP, trackerPort):
        # Get hashcode_list from torrent
        self.magnet_text_list = get_magnetTexts_from_torrent()
        hashcode_list = list(self.magnet_text_list.keys())
        hashcode_list = " ".join(hashcode_list)

        if len(hashcode_list) == 0:
            return

        try:
            # Send hashcode to tracker
            message = " ".join(
                ["START", self.peer_host, str(self.peer_port), hashcode_list]
            )

            tracker_socket = self.make_connection_to_tracker()
            print(f"Connected to tracker {trackerIP}:{trackerPort}")
            tracker_socket.sendall(message.encode())
            tracker_socket.close()

            print("Sent success")

        except Exception as e:
            print("something when wrong when start : {}".format(e))

    def get_all_file(self):
        """Fetch all file from Tracker"""
        try:
            message = "FETCH ALL TORRENT"

            tracker_socket = self.make_connection_to_tracker()
            print(f"Connected tracker to get all file")
            tracker_socket.sendall(message.encode())
            res = tracker_socket.recv(8192).decode()
            tracker_socket.close()

            Files = ast.literal_eval(res)
            return Files

        except Exception as e:
            print("Something when wrong when get all file: {}".format(e))
            return []

    def upload_Torrent(self, filename):  # .txt
        """upload torrent for tracker"""
        try:
            data = generate_Torrent(filename)
            if data is None:
                return

            message = " ".join(["UPLOAD", self.peer_host, str(self.peer_port), data])

            tracker_socket = self.make_connection_to_tracker()
            print("Connected tracker to upload file")
            tracker_socket.sendall(message.encode())
            res = tracker_socket.recv(8192).decode()
            tracker_socket.close()

            if res != "File already exists":
                create_torrent_file(filename, json.loads(data))

            magnet_text = json.loads(data)["magnetText"]
            filenameTorrent = filename.split(".")[0] + ".json"
            self.magnet_text_list[magnet_text] = filenameTorrent
            print(self.magnet_text_list)

        except Exception as e:
            print("Something when wrong when Upload file: {}".format(e))

    def make_connection_to_tracker(self):
        """connect to tracker"""
        tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tracker_socket.settimeout(2)
        tracker_socket.connect((trackerIP, trackerPort))
        return tracker_socket

    def download_torrent_from_tracker(self, magnet_text):
        message = " ".join(
            ["DOWNLOAD", self.peer_host, str(self.peer_port), magnet_text]
        )
        try:
            # Send request download fo tracker
            tracker_socket = self.make_connection_to_tracker()
            print(f"Connected tracker for download torrent")
            tracker_socket.sendall(message.encode())

            res = tracker_socket.recv(8192)
            res = bencodepy.decode(res)
            print(res)
            res = res.decode("utf-8")

            # debug
            print(res)
            tracker_socket.close()

            data_torrent = json.loads(res)["torrent_file"]
            data_list = json.loads(res)["peer_list"]

            return data_torrent, data_list
        except Exception as e:
            print("Something when wrong when download torrent : {}".format(e))

    def exit(self, host, port):
        self.running = False
        message = " ".join(["EXIT", host, str(port)])

        try:
            tracker_socket = self.make_connection_to_tracker()
            tracker_socket.sendall(message.encode())
            tracker_socket.close()

            print("Exit success")

        except Exception as e:
            print("Something when wrong when exit")

    # -------------------------------------------#
