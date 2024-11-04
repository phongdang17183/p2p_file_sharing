from enum import Enum
from json import loads


class Type(Enum):
    REQUEST = 0
    RESPONSE = 1


class Header(Enum):
    PING = 0  # for announce that this peer is still alive
    DISCOVER = 1
    PUBLISH = 2
    FETCH = 3
    REGISTER = 4  # register this peer to server ?!
    LOG_IN = 5
    LOG_OUT = 6
    RETRIEVE = 7
    DOWNLOAD_MULTI = 8  # download multifile
    DOWNLOAD = 9  # download by pieces request


class Message:
    def __init__(self, header: Header, type: Type, info, message=None):
        if message:
            temp = loads(message)
            header = Header(temp["header"])
            type = Type(temp["type"])
            info = temp["info"]
        self._header = header
        self._type = type
        self._info = info
        """
        info include: server host, infohash, file server port, pieces
        """

    def get_header(self):
        return self._header

    def get_type(self):
        return self._type

    def get_info(self):
        return self._info

    def get_message(self):
        return {
            "header": self._header.value,
            "type": self._type.value,
            "info": self._info,
        }
