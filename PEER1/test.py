import os
import json
import hashlib

def create_temp_file(data, piece_count, torrent):
    """tao temp file cho piece"""
    #check sum + create file tmp
    if check_sum(data, torrent['metaInfo']['pieces'], piece_count):
    
        path = os.path.dirname(__file__)
        file_name = torrent['metaInfo']['name'] + "_" +str(piece_count) + ".tmp"
        fullpath = os.path.join(path, "Temp", file_name)
        
        with open(fullpath, 'wb') as f:
            f.write(data)
        print(f"Tệp {file_name} đã được tạo thành công.")
    
    else: 
        print("data loi khi check sum.")

def check_sum(data, listPiece, piece_count):
    """check"""
    hashPiece = hashlib.sha1(data).digest().hex()
    if(hashPiece == listPiece[piece_count]):
        return True
    else:
        return False
    
    
# def merge_temp_files(output_file, filename):
#     """Gộp tất cả các tệp .tmp trong thư mục temp thành một tệp duy nhất."""
#     path = os.path.dirname(__file__)
#     fullpath = os.path.join(path,"test", output_file)
    
#     # Mở tệp đích để ghi tất cả nội dung từ các tệp .tmp
#     with open(fullpath, 'wb') as outfile:
#         # Lấy danh sách tất cả các tệp .tmp trong thư mục temp và sắp xếp chúng
#         temp_files = sorted([f for f in os.listdir(os.path.join(path,"test")) if f.endswith('.tmp') and f.startswith(filename)],
#                             key=lambda x: int(x.split('_')[1].split('.')[0]))  # Giả sử tên tệp có dạng 'piece_1.tmp'
        
#         # Duyệt qua từng tệp .tmp và ghi nội dung vào tệp đích
#         for temp_file in temp_files:
#             temp_file_path = os.path.join(os.path.join(path,"test"), temp_file)
#             with open(temp_file_path, 'rb') as infile:
#                 outfile.write(infile.read())  # Đọc và ghi toàn bộ nội dung vào tệp đích
    
#     print(f"Đã gộp tất cả các tệp .tmp thành tệp duy nhất: {output_file}")

def create_torrent_file(file_name, data_torrent):
    """Tạo một tệp .json mới từ dữ liệu JSON."""
    path = os.path.dirname(__file__)
    file_name +=  ".json"
    fullpath = os.path.join(path, "test", file_name)
    with open(fullpath, 'wb') as json_file:
        json.dump(bytes(data_torrent), json_file, indent=4)
    print(f"Tệp {file_name} đã được tạo thành công.")
    
# Ví dụ sử dụng
data = "45611"
piece_count = 2
torrent = {
    "trackerIp": "10.10.2.182",
    "magnetText": "5f7124f698afa29f5780043bc62144767ba5af7c",
    "metaInfo": {
        "name": "text",
        "filesize": 80,
        "piece_size": 4,
        "pieces": [
            "776351ef196dbed5844a1140802b855498d7d81e",
            "c4269587151954eb6574fde71423650831ffb111",
            "19c96b9957f3491ac5881c52c163dfe4b481c3ff",
            "2ed618ae9167374fef1859a846a389ccf4a08427",
            "61dce8dc32a68b6793698881bfd9d244cf5dfc41",
            "a78fc6756af3b204c8dfe1635b2cb47ac71ae988",
            "910091cc05b9bd57820c2d1d921f6a7a3fa9bca5",
            "eef18771dac22e9d6bcb29f8620208e8ea1667b0",
            "596daf0c25a72e2ae114e58b66b3235d9fc96386",
            "69c298569e8d5bd04d1bbc406cdb5c1699cee7a0",
            "072c2548bb86a8838bbe10ec453731f4b1455832",
            "1caa5d9074f0e44d4d732a47b14f122e2b478031",
            "db9997ca8f6baa3fedda7d5a2ae270832c017b04",
            "80834a9cf51a8c3faed6af74e3943fc9f9fad018",
            "5a42fc4be595215857c41c5eee869087f5a30c19",
            "072c2548bb86a8838bbe10ec453731f4b1455832",
            "bc32e211aaec9d99e3ebecf377d0944ec5ec3637",
            "5e37028beac0f0d8c6640021fc13643313ef3e3f",
            "cf217d30e8b6734c61d5367049dec6207e80018e",
            "cde5911439b1bf1db82642e6e4ae76bdc44c048a"
        ]
    }
}

# create_torrent_file("bach1",torrent)
# create_temp_file(data, piece_count, torrent)
# merge_temp_files("merged_output_file.txt", "text3")