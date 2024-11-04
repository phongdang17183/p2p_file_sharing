from peer import Peer
from apiclient import ClientSite


def main():
    """Main function to run the client interface."""
    print("Welcome to the P2P File Sharing Client!")
    # host = input("Enter Host: ")
    # port = int(input("Enter Port (for listening): "))
    host = "127.0.0.1"
    port = 65431

    client = ClientSite(Peer(host, port))

    while True:
        print("\nAvailable Commands:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        command = input("Enter command number: ")

        if command == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            client.register(username, password)

        if command == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            client.login(username, password)

        elif command == "3":
            client.exit()
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
