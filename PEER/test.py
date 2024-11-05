import os
import socket
import json

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

hostIp= get_host_default()
hostPort = 1000
trackerIP = "192.168.1.68"
trackerPort = 1000
print( hostIp, trackerIP )

connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect.settimeout(2)
connect.connect((trackerIP, trackerPort))
# def send_torrent_hashcodes():
#     torrent_folder = './Torrent'
    
#     # Lấy danh sách các tệp trong thư mục Torrent
#     files = os.listdir(torrent_folder)
    
#     # Lọc các tệp JSON
#     hashcodes = []
#     for file_name in files:
#         if file_name.endswith('.json'):
#             try:
#                 with open(os.path.join(torrent_folder, file_name), 'r') as file:
#                     data = json.load(file)
#                     hashcode = data.get("hashcode", None)
#                     if hashcode:
#                         hashcodes.append(hashcode)
#             except json.JSONDecodeError:
#                 print(f"Lỗi định dạng JSON trong tệp {file_name}. Bỏ qua tệp này.")    
#             except Exception as e:
#                 print(f"Lỗi không xác định khi đọc tệp {file_name}: {e}")
#     # Gửi danh sách hashcode cho tracker
#     for hashcode in hashcodes:
#         print(hashcode)
    
#     print("Sent all hashcodes to tracker")

# send_torrent_hashcodes()
