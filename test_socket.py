import socket
from utils import get_host_default
import json

data = {
    "trackerIp": "192.168.244.43",
    "magnetText": "de9606a4a16a251304dd0095a00f86419cf01f0a",
    "metaInfo": {
        "name": "text.txt",
        "filesize": 24,
        "piece_size": 4,
        "pieces": [
            "776351ef196dbed5844a1140802b855498d7d81e",
            "c4269587151954eb6574fde71423650831ffb111",
            "19c96b9957f3491ac5881c52c163dfe4b481c3ff",
            "2ed618ae9167374fef1859a846a389ccf4a08427",
            "61dce8dc32a68b6793698881bfd9d244cf5dfc41",
            "a78fc6756af3b204c8dfe1635b2cb47ac71ae988",
        ],
    },
}


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = get_host_default()
print(ip)
s.connect((ip, 65432))
message1 = "START 17.0.1 10 sadkasd asmdasmd"
message2 = "EXIT 17.0.1 10"

# Chuyển đổi dữ liệu thành chuỗi JSON
json_data = json.dumps(data)
message3 = "UPLOAD " + json_data
message4 = "FETCH ALL TORRENT"

s.send(message4.encode("utf-8"))
