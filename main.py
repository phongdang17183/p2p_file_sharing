import socket
from apiclient import ClientSite
from peer import Peer
from utils import get_host_default


def main():
    """Main function to run the client interface."""
    print("Welcome to the P2P File Sharing Client!")
    host = get_host_default()
    port = 1000
    print("hi {} {}".format(host, port))

    client = ClientSite(Peer(host, port))

    while True:
        print("\nAvailable Commands:")
        print("1. Start")
        print("2. Get all file")
        print("3. Download")
        print("4. Upload")
        print("5. Exit")

        command = input("Enter command number: ")

        if command == "1":
            client.start()

        elif command == "2":
            client.get_all_file()

        elif command == "3":
            hashcode = input("Enter torrent hashcode: ")
            client.download(hashcode)

        elif command == "4":
            print("Make sure your file is in folder Myfolder")
            filename = input("Enter filename: ")
            client.upload(filename)

        elif command == "5":
            client.exit(host, port)
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
