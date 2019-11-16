import socket

class Client(object):
    def __init__(self, host='127.0.0.1', port=31337):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def execute(self, *args):
        ###TODO: parse a command which is given in args, send it to server and receive response 
        self.socket.sendall(b'Hello, world')
        data = self.socket.recv(1024)
        print(data)

