from peer import Peer
import socket
from threading import Thread

class ClientSite:
    """Interface to interact with client with api (like response entity or DTO)"""

    def __init__(self, peer: Peer):
        self.peer = peer

    def start(self):
        """Start first connect to tracker"""
        # tracker return a peerId
        # self.peer.connectToTrackerForPeerID(trackerID, trackerPort)
        # begin to be a seeder if have torrent => update peerList on tracker
        # self.peer.listen()
        self.peer.start()

    def get_all_file(self):
        """get all file from tracker"""
        Files = self.peer.get_all_file()
        # print all hashcode in a table
        print(f"{'Name':<20} {'HashInfo'}")
        print("-" * 40)

        for file_name, hashcode in Files:
            print(f"{file_name:<20} {hashcode}")

    def download(hashcode):
        """download with hashcode"""
        print("download")
    
    def upload(self, filename):
        """upload torrent"""
        self.peer.upload_Torrent(filename)
    
    def exit(self, host, port):
        """exit app """
        self.peer.exit(host, port)
        
        # announce tracker to update peerlist
