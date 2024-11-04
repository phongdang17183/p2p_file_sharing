import os

import json

def send_torrent_hashcodes():
    torrent_folder = './Torrent'
    
    # Lấy danh sách các tệp trong thư mục Torrent
    files = os.listdir(torrent_folder)
    
    # Lọc các tệp JSON
    hashcodes = []
    for file_name in files:
        if file_name.endswith('.json'):
            try:
                with open(os.path.join(torrent_folder, file_name), 'r') as file:
                    data = json.load(file)
                    hashcode = data.get("hashcode", None)
                    if hashcode:
                        hashcodes.append(hashcode)
            except json.JSONDecodeError:
                print(f"Lỗi định dạng JSON trong tệp {file_name}. Bỏ qua tệp này.")    
            except Exception as e:
                print(f"Lỗi không xác định khi đọc tệp {file_name}: {e}")
    # Gửi danh sách hashcode cho tracker
    for hashcode in hashcodes:
        print(hashcode)
    
    print("Sent all hashcodes to tracker")

send_torrent_hashcodes()
