from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection

import certifi
import socket
from threading import Thread


def get_host_default():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 1))
        ip = s.getsockname()[0]
    except Exception:
        print("err when get host default")
        return None
    finally:
        s.close()
    return ip


# Create a new client and connect to the server
DATABASE_URL = "mongodb+srv://tranchinhbach:tranchinhbach@co3001.qkb5z.mongodb.net/?retryWrites=true&w=majority&appName=CO3001/tracker"
# try:
#     database = MongoClient(DATABASE_URL, tlsCAFile=certifi.where())
#     print("Connected to MongoDB successfully.")
# except Exception as e:
#     print(f"Failed to connect to MongoDB: {e}")

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(("localhost", 8080))  # Địa chỉ và cổng của server socket
# server_socket.listen(5)

# Send a ping to confirm a successful connection
# tracker_db = database["tracker"]
# torrentfile = tracker_db["torrentfile"]
# documents = torrentfile.find()
# for document in documents:
#     print(str(document))


class Tracker:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.tracker_socket: socket.socket = None

        self.database: MongoClient = None
        self.torrent_file: Collection = None
        self.files: Collection = None

        self.__thread: dict[str, Thread] = {}
        self.start()

    def start(self):

        # Connnect to database
        try:
            self.database = MongoClient(DATABASE_URL, tlsCAFile=certifi.where())
            self.torrent_file = self.database["torrentfile"]
            self.files = self.database["files"]

            print("Connected to MongoDB successfully.")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.shutdown()

        self.tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tracker_socket.bind((self.host, self.port))
        self.tracker_socket.listen(10)

        while True:
            peer_socket, peer_addr = self.tracker_socket.accept()
            peer = Thread(target=self.recieve_torrent, args=(peer_socket, peer_addr))
            print(f"connect from {peer_addr}")
            peer.start()

    def recieve_torrent(self, peer_socket, peer_addr):
        torrent = peer_socket.recv(1024)
        print(str(torrent))

    def shutdown(self):
        for thread in self.__thread.values():
            thread.join()

        self.database.close()


ip = get_host_default()
print(ip)
tracker = Tracker(ip, 8081)