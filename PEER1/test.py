import os
import socket
import json
import hashlib


def hash_function( piece_size=4):
    filepath = "./MyFolder/text.txt"
    piece_hashes = []
    hashinfo = hashlib.sha1()
    # size =  os.stat(filepath).st_size
    size = 1
    with open(filepath, 'rb') as f:
        while True:
            piece = f.read(piece_size)
            if not piece:
                break 
            
            piece_hash = hashlib.sha1(piece).digest()  
            piece_hashes.append(piece_hash.hex())
            hashinfo.update(piece_hash)
            
    return hashinfo.hexdigest(), piece_hashes, size, piece_size

print(hash_function())