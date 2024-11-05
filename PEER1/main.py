import socket
from apiclient import ClientSite
from peer import Peer

def get_host_default():  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        print('err when get host default')
        return None
    finally:
        s.close()
    return ip

def main():
    """Main function to run the client interface."""
    print("Welcome to the P2P File Sharing Client!")
    # host = input("Enter Host: ")
    # port = int(input("Enter Port (for listening): "))
    host = get_host_default()
    port = 1001
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
            hashcode = input("Enter torrent hashcode")
            client.download(hashcode)

        elif command == "4":
            print("Make sure your file is in folder Myfolder")
            filename = input("Enter filename: ") 
            client.upload( filename )
        
        elif command == "5":
            client.exit(host, port)
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
