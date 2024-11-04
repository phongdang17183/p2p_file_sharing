import socket
from threading import Thread
from message import *
import requests
import json
import os
from utils import *
from apitracker import TrackerSite


class Peer:
    def __init__(self, peer_host, peer_port):
        self.__start = False
        self.__login_success = False
        self.peer_id = None

        self.peer_host = peer_host
        self.peer_port = peer_port

        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.peer_host, peer_port))
        print(self.listen_socket.getsockname()[1])

        self.__thread: dict[str, Thread] = {}
        self.__thread["listen"] = Thread(target=self.listen, daemon=True)

        self.run()

    def start_file_server(self, port):
        """Listen from other peer to recieve file."""
        try:
            file_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            file_server.bind((self.client_host, port))
            file_server.listen()
            print(f"[FILE SERVER] Listening for file transfers on port {port}")

            while True:
                conn, addr = file_server.accept()
                print(f"[FILE SERVER] Connection from {addr}")
                thread = Thread(target=self.receive_file, args=(conn,))
                thread.start()
        except Exception as e:
            print(f"Error in file server: {e}")
        finally:
            file_server.close()

    def handle_incoming_connection(self, recv_socket, src_addr):
        """
        Handle a new connection and pass the message to the appropriate function (for peer connect peer ?!).
        include PING
        """
        try:
            recv_socket.settimeout(5)
            message = recv_socket.recv(2048).decode()
            message = Message(None, None, None, message)
            message_header = message.get_header()

            if message_header == Header.PING:
                self.reply_ping_message(recv_socket)

        except Exception as e:
            print(f"An error occurred in listen: {e}")
        finally:
            recv_socket.close()

    def send_message(self, message: Message, sock: socket.socket):
        """
        Send an encoded message to an existing socket
        - message: Message to be sent
        - sock: Socket to which the message is sent

        Return: True if the message sent successfully, False otherwise
        """
        encode_message = json.dumps(message.get_packet()).encode("utf-8")
        # dest = 'server' if sock.getpeername()[0] == self.server_host else sock.getpeername()[0]

        dest = sock.getpeername()[0]

        try:
            sock.sendall(encode_message)
            print(
                f"Send a {message.get_header().name} - {message.get_type().name} message to {dest}"
            )
            return True
        except:
            print(
                f"An error occurred while sending a {message.get_header().name} message to {dest}"
            )
            return False

    def reply_ping_message(self, sock):
        """
        Receive ping message from the server and reply with PONG to tracker
        """
        response = Message(Header.PING, Type.RESPONSE, "PONG")
        self.send_message(response, sock)

    def run(self):
        """
        Initiate listening socket on port 5001 and FTP server on port 21.
        Socket port 5001 is used to listen incoming messages from server (ping, discover command)
        and other peers (request before transfering file). FTP server port 21
        is used to transfer file. This function also initialize other resources if necessary.
        """

        if self.__start:
            return

        for thread in self.__thread.values():
            thread.start()

        self.__start = True

    def exit(self):
        """
        Stop listening in port 5001 and port 21. Clean up other resources if necessary.
        """
        if not self.__start:
            return
        print("exiting...")
        # Close the listening socket
        self.listen_socket.close()

        for thread in self.__thread.values():
            thread.join()

        self.__start = False

    def listen(self):
        """
        Listen on the opening socket and create a new thread whenever it accepts a connection (listen peer connect ?!).
        """
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

    def publish(self, filename, filepath, description):
        """
        A local file (which is stored in the client's file system at filepath) is added to the client's repository
        as a file named fname and this information is conveyed to the tracker.

        Parameters:
        - filepath: The path to the file in local file system
        - filename: The file to be uploaded and published in the repository
        Tuc la can gui torrent file len, neu file da co trong db, cap nhat nhung peer da chua file nay -> se phai gui 2 req den tracker
        Return: Response message from the server
        """

        filesize = os.path.getsize(filepath)
        list_pieces, piece_size = split_file(filepath, filename)
        torrent_data = generate_torrent(filesize, filename, piece_size, list_pieces)

        response = requests.post(os.getenv(), json=torrent_data)

        result = response.json()

        return result

    ###########################
    ### Function for client ###
    ###########################
    def register(self, username, password):
        """
        Client registers its hostname and password to the server:

        {
            "Failure reason": "" (may be null),
            "Warning": "" (may be null),
            "Success":
                {
                    "Peer ID": tracker_id,
                    "Peer IP": peer_ip,
                    "Peer Port": peer_port,
                }
        }
        """

        request_data = {
            "username": username,
            "password": password,
            "peer_id": self.peer_host,
            "peer_port": self.peer_host,
        }
        response = TrackerSite.post(request_data)
        return response.json()

    def login(self, username, password):
        """
        Client registers its hostname and password to the server\n
        Return: Response message from the server
        """
        request_data = {
            "username": username,
            "password": password,
        }
        response = TrackerSite.post(request_data)
        if response.status_code == 200:
            self.__login_success = True
        return response.json()
