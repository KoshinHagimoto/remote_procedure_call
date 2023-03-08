import os
import socket
import json
import math
import sys


class UnixServer:
    def __init__(self, path:str='/tmp/myapp.sock', timeout:int=60, buffer:int=4096):
        self.server = path
        self.__socket = None
        self.__timeout = timeout
        self.__buffer = buffer
        self.close()
        self.delete()
        self.create_socket(self.server, socket.AF_UNIX, socket.SOCK_STREAM, 0)
        self.accept()

    def __del__(self):
        self.delete()
    
    def close(self) -> None:
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except:
            pass

    def delete(self):
        if os.path.exists(self.server):
            os.remove(self.server)
    
    def create_socket(self, address, family:int, typ:int, proto:int) -> dict:
        self.__socket = socket.socket(family, typ, proto)
        self.__socket.settimeout(self.__timeout)
        self.__socket.bind(address)
        self.__socket.listen(1)
        print("Server started :", address)
    
    def accept(self):
        connection, _ = self.__socket.accept()

        while True:
            try:
                received_packet= connection.recv(self.__buffer)
                if len(received_packet) == 0:
                    break
                request_dict = json.loads(received_packet.decode('utf-8'))
                print(request_dict)
                response_dict = self.process(request_dict)
                if request_dict['id'] == response_dict['id']:
                    packet = json.dumps(response_dict).encode()
                    connection.sendall(packet)
            except ConnectionResetError:
                break
            except BrokenPipeError:
                break
        self.close()
        print("Finish")
    
    def process(self, request:dict, response:dict={}) -> dict:
        method = request['method']
        while True:
            try:
                func = getattr(self, method)
                try:
                    response['results'] = func(request['params'])
                    response['result_type'] = str(type(response['results']))
                except Exception as e:
                    print(e)
                    sys.exit()
            except AttributeError:
                print('this method:{} is not exist.\n'.format(method))
                print('please input method \n')
                method = input('>>>')
            except Exception as othererr:
                print(type(othererr))
                print(othererr)
            else:
                print('Success')
                break
        response['id'] = request['id']
        print(response)
        return response

    def floor(self, x:float) -> int:
        return math.floor(x)
    
    def nroot(self, intArr:list) -> float:
        x = intArr[0]
        n = intArr[1]
        return math.pow(x, 1/n)
    
    def reverse(self, s:str) -> str:
        return s[::-1]
    
    def validAnagram(self, strList:list) -> bool:
        str1 = strList[0]
        str2 = strList[1]
        if str1 is None or str2 is None or len(str1) != len(str2):
            return False
        return True if sorted(str1) == sorted(str2) else False
    
    def sort(self, strArr:list) -> list:
        return sorted(strArr)

if __name__ == '__main__':
    UnixServer()