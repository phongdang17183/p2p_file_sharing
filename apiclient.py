from peer import Peer
import socket


class ClientSite:
    """Interface to interact with client with api (like response entity or DTO)"""

    def __init__(self, peer: Peer):
        self.peer = peer

    def start(self, trackerIP, trackerPort):
        """Start first connect to tracker"""
        # tracker return a peerId
        # self.peer.connectToTrackerForPeerID(trackerID, trackerPort)
        # begin to be a seeder if have torrent => update peerList on tracker

        self.peer.start()

    def get_all_file(self, trackerIP, trackerPort):
        """get all file from tracker"""
        files = self.peer.connectToTrackerGetAllFile(trackerIP, trackerPort)
        # print all hashcode in a table
        print(f"{'Name':<20} {'HashInfo'}")
        print("-" * 40)

        for file in files:
            name = file.get("name", "N/A")
            hash_info = file.get("hashInfo", "N/A")
            print(f"{name:<20} {hash_info}")

    def download(hashcode):
        """download with hashcode"""
        print("download")

    def upload():
        """upload torrent"""

        print("upload")

    def exit():
        """exit app"""
        # announce tracker to update peerlist
