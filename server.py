import os
import socket
import json
import math
import sys


class BaseServer:
    def __init__(self):
        self.__socket = None
        self.close()
    
    def __del__(self):
        self.close()
    
    def close(self) -> None:
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except:
            pass
    
    def create_socket(self, address, family:int, typ:int, proto:int):
        self.__socket = socket.socket(family, typ, proto)
        self.__socket.settimeout(60)
        self.__socket.bind(address)
        self.__socket.listen(1)
        print("Server started :", address)
        return self.__socket.accept()


class UnixServer(BaseServer):
    def __init__(self, path:str, buffer:int=4096):
        self.server = path
        self.__buffer = buffer
        self.delete()
        
    def __del__(self):
        self.delete()

    def delete(self):
        if os.path.exists(self.server):
            os.remove(self.server)
    
    def accept(self, connection):
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
       """
       10進数xを最も近い整数に切り捨て, その結果を整数で返す.
       """
        return math.floor(x)
    
    def nroot(self, intArr:list) -> float:
       """
       方程式r^n = x における, rの値を計算する.
       """
        x = intArr[0]
        n = intArr[1]
        return math.pow(x, 1/n)
    
    def reverse(self, s:str) -> str:
       """
       文字列sを入力として受取, 入力文字列の逆である新しい文字列を返す
       """
        return s[::-1]
    
    def validAnagram(self, strList:list) -> bool:
       """
      　2つの入力文字列がアナグラムであるか判定
       """
        str1 = strList[0]
        str2 = strList[1]
        if str1 is None or str2 is None or len(str1) != len(str2):
            return False
        return True if sorted(str1) == sorted(str2) else False
    
    def sort(self, strArr:list) -> list:
        return sorted(strArr)


def main():
    path = '/tmp/myapp.sock'
    server = UnixServer(path)
    connection, _ = server.create_socket(path, socket.AF_UNIX, socket.SOCK_STREAM, 0)
    server.accept(connection)


if __name__ == '__main__':
    main()
