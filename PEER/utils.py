import socket
import hashlib
import os
from dotenv import load_dotenv
import json
    
load_dotenv()
trackerIP = os.getenv('TRACKERIP')
trackerPort = int(os.getenv('TRACKERPORT'))

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

def make_attribute_torrent(filename , piece_size=4):
    path = os.path.dirname(__file__)
    fullpath = os.path.join(path, "MyFolder", filename)
    
    piece_hashes = []
    hashinfo = hashlib.sha1()
    
    size =  os.stat(fullpath).st_size
    
    with open(fullpath, 'rb') as f:
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
            "name": filename.split('.')[0],
            "filesize": size,
            "piece_size": piece_size,
            "pieces": pieces
        }
    }
    create_torrent_file(filename.split('.')[0], data)
    return json.dumps(data)

def get_magnetTexts_from_torrent():
    path = os.path.dirname(__file__)
    fullpath = os.path.join(path, "Torrent")
    
    # Lấy danh sách các tệp trong thư mục Torrent
    hashcodes = {}
    files = os.listdir(fullpath)
    json_files = [file for file in files if file.endswith('.json')]
    
    for file_name in json_files:
        hashcode = get_hashcode(fullpath, file_name)
        if hashcode is not None:
            hashcodes[hashcode] = file_name
            
    print(hashcodes)     
    return hashcodes
                    
def get_hashcode(fullpath, file_name):
    try:
        with open(os.path.join(fullpath, file_name), 'r') as file:
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
        
def create_torrent_file(file_name, data_torrent):
    """Tạo một tệp .json mới từ dữ liệu JSON."""
    path = os.path.dirname(__file__)
    file_name +=  ".json"
    fullpath = os.path.join(path, "Torrent", file_name)
    with open(fullpath, 'w') as json_file:
        json.dump(data_torrent, json_file, indent=4)
    print(f"Tệp {file_name} đã được tạo thành công.")

def create_temp_file(data, piece_count, torrent):
    """tao temp file cho piece"""
    #check sum + create file tmp
    if check_sum_piece(data, torrent['metaInfo']['pieces'], piece_count):
    
        path = os.path.dirname(__file__)
        file_name = torrent['metaInfo']['name'] + "_" +str(piece_count) + ".tmp"
        fullpath = os.path.join(path, "Temp", file_name)
        
        with open(fullpath, 'wb') as f:
            f.write(data)
        print(f"Tệp {file_name} đã được tạo thành công.")
    
    else: 
        print("data loi khi check sum.")

def check_sum_piece(data, listPiece,  piece_count):
    """check"""
    hashPiece = hashlib.sha1(data).digest().hex()
    if(hashPiece == listPiece[piece_count]):
        return True
    else:
        return False
    
def check_file(filename, torrent_file):
    status = []
    path = os.path.dirname(__file__)
    fullpath = os.path.join(path, "MyFolder", filename)
    with open(fullpath, "rb") as file:
        while True:
            index = 0
            piece = file.read(torrent_file["metaInfo"]["piece_size"])
            if not piece:
                break
            status.append(
                check_sum_piece(piece, torrent_file["metaInfo"]["pieces"], index)
            )
    return status


def merge_temp_files(output_file, filename):
    """Gộp tất cả các tệp .tmp trong thư mục temp thành một tệp duy nhất."""
    path = os.path.dirname(__file__)
    fullpath = os.path.join(path,"Download", output_file)
    
    with open(fullpath, 'wb') as outfile:
        # Lấy danh sách tất cả các tệp .tmp trong thư mục temp và sắp xếp chúng
        temp_files = sorted([f for f in os.listdir(os.path.join(path,"Temp")) if f.endswith('.tmp') and f.startswith(filename)],
                            key=lambda x: int(x.split('_')[1].split('.')[0]))  # Giả sử tên tệp có dạng 'piece_1.tmp'
        
        # Duyệt qua từng tệp .tmp và ghi nội dung vào tệp đích
        for temp_file in temp_files:
            temp_file_path = os.path.join(os.path.join(path,"Temp"), temp_file)
            with open(temp_file_path, 'rb') as infile:
                outfile.write(infile.read())  # Đọc và ghi toàn bộ nội dung vào tệp đích
    
    print(f"Đã gộp tất cả các tệp .tmp thành tệp duy nhất: {output_file}")
    
    
