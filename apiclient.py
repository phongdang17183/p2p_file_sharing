from peer import Peer


class ClientSite:
    """Interface to interact with client with api (like response entity or DTO)"""

    def __init__(self, peer: Peer):
        self.peer = peer
        self.success = False

    def register(self, username, password):
        """Register username and password to the tracker"""
        response = self.peer.register(username, password)
        print("register success: ", response)
        return response

    def login(self, username, password):
        """Login to the tracker"""
        response = self.peer.login(username, password)
        print("login success")
        return response

    def exit(self):
        """Exit the client"""
        self.peer.exit()
        print("Exiting the client.")
