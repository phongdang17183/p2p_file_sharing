import socket
import hashlib
import os
from dotenv import load_dotenv
import json

load_dotenv()
trackerIP = os.getenv("TRACKERIP")
trackerPort = int(os.getenv("TRACKERPORT"))


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


def make_attribute_torrent(filename, piece_size=4):
    path = os.path.dirname(__file__)
    fullpath = os.path.join(path, "MyFolder", filename)

    piece_hashes = []
    hashinfo = hashlib.sha1()

    size = os.stat(fullpath).st_size

    with open(fullpath, "rb") as f:
        while True:
            piece = f.read(piece_size)
            if not piece:
                break

            piece_hash = hashlib.sha1(piece).digest()
            piece_hashes.append(piece_hash.hex())
            hashinfo.update(piece_hash)

    return hashinfo.hexdigest(), piece_hashes, size, piece_size


def generate_Torrent(filename):

    magnet_text, pieces, size, piece_size = make_attribute_torrent(filename)
    data = {
        "trackerIp": trackerIP,
        "magnetText": magnet_text,
        "metaInfo": {
            "name": filename,
            "filesize": size,
            "piece_size": piece_size,
            "pieces": pieces,
        },
    }
    return json.dump(data)


def get_magnetTexts_from_torrent():
    path = os.path.dirname(__file__)
    fullpath = os.path.join(path, "Torrent")

    # Lấy danh sách các tệp trong thư mục Torrent
    hashcodes = []
    files = os.listdir(fullpath)
    json_files = [file for file in files if file.endswith(".json")]

    for file_name in json_files:
        hashcode = get_hashcode(fullpath, file_name)
        if hashcode is not None:
            hashcodes.append(hashcode)

    print(hashcodes)
    return hashcodes


def get_hashcode(fullpath, file_name):
    try:
        with open(os.path.join(fullpath, file_name), "r") as file:
            data = json.load(file)
            hashcode = data.get("magnetText", None)
            if hashcode is not None:
                return hashcode
            else:
                raise Exception("khong co hashcode")
    except json.JSONDecodeError:
        print(f"Lỗi định dạng JSON trong tệp {file_name}. Bỏ qua tệp này.")
    except Exception as e:
        print(f"Lỗi khi đọc tệp {file_name}: {e}")
