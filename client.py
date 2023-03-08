import socket
import sys
import json


class BaseClient:
    def __init__(self, timeout:int=10, buffer:int=4096):
        self.__socket = None
        self.__address = None
        self.__timeout = timeout
        self.__buffer = buffer

    def connect(self, address, family:int, typ:int, proto:int):
        self.__address = address
        self.__socket = socket.socket(family, typ, proto)
        self.__socket.settimeout(self.__timeout)
        self.__socket.connect(self.__address)
    
    def send(self, request:json=None) -> None:
        try:
            with open(request) as f:
                request_dict = json.load(f)
                self.__socket.send(json.dumps(request_dict).encode())
        except TypeError as err:
            print(err)
            sys.exit()
        received_packet = self.__socket.recv(self.__buffer)
        dictionary = json.loads(received_packet.decode())
        self.received(dictionary)
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except:
            pass
    
    def received(self, dictionary:dict):
        print(dictionary)
        with open('response.json', 'w') as f:
            json.dump(dictionary, f)
    

class UnixClient(BaseClient):
    def __init__(self, path:str='/tmp/myapp.sock'):
        self.server = path
        super().__init__(timeout=60, buffer=4096)
        super().connect(self.server, socket.AF_UNIX, socket.SOCK_STREAM,  0)

if __name__ == '__main__':
    cli = UnixClient()
    try:
        request = sys.argv[1]
    except IndexError:
        print("please input json file")
        request = input('>>>')
    cli.send(request)