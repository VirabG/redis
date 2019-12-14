import socket

class Server(object):
    def __init__(self, host='127.0.0.1', port=31337):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()
    
    def run(self):
        conn, addr = self.socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                ###TODO: process data here and send response back to client
                conn.sendall(data)

