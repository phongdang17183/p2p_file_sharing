import bencodepy
import socket


PIECE_SIZE = 512 * 1024  # 512 KB


def generate_torrent(filesize, filename, piece_size, list_pieces):
    """Generate info hash"""
    info = {
        "file_name": filename,
        "file_size": filesize,
        "piece_size": piece_size,
        "list_pieces": list_pieces,
    }
    print(info)
    # bencoded_info = Bencode().encode(info)
    bencoded_info = bencodepy.encode(info)
    return bencoded_info


def split_file(filepath, filename, piece_size=512 * 1024):
    """Slice a file into pieces of size piece_size. Return (list_piece, piece_size)"""
    list_pieces = []
    with open(filepath, "rb") as file:
        while chunk := file.read(piece_size):
            list_pieces.append(chunk)

    return (list_pieces, piece_size)


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
