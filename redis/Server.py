import socket
from ProtocolHandler import ProtocolHandler
from ProtocolHandler import LINE_SEPARATOR, SEPARATOR_LENGTH
import time

class Server(object):
    def __init__(self, host='127.0.0.1', port=31337):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()

        self.database = dict()
        self.prot_handler = ProtocolHandler()
    
    def run(self):
        conn, addr = self.socket.accept()
        with conn:
            print('Connected by', addr)
            fulldata = b''
            while True:
                data = conn.recv(32)
                if not data:
                    break
                ###TODO: process data here and send response back to client
                ##TODO: process SET and GET
                ## SET or GET is the first word of data
                ## SET key value
                ## key is identifier alphanumeric
                ## value is int string array or dict
                ## if data[:3] == 'SET'
                ##      process(SET)
                ## self.database[key] = value
                ## if data[:3] == 'GET'
                ##      process(GET)
 
                #https://docs.python.org/3/howto/sockets.html
                #first put length of message
                #for short messages we can use socket.recv(length of message)
                # for longer 
                # while num_of_read_bytes < length_of_message:
                #   message.append(socket.recv(1024))
                #   num_of_read_bytes += 1024

                print(data)
                fulldata += data
                #conn.sendall(data)
            command = fulldata.decode('ascii')
            print(command)
            if command[0:3] == 'GET':
                key = self.prot_handler.deserialize(command[3:])
                try:
                    response = self.prot_handler.serialize(self.database[key])
                except:
                    response = self.prot_handler.serialize('No such key')

            elif command[0:3] == 'SET':
                key_end = command.find(LINE_SEPARATOR)
                key = self.prot_handler.deserialize(command[3:key_end + SEPARATOR_LENGTH])
                value = self.prot_handler.deserialize(command[key_end + SEPARATOR_LENGTH:])
                self.database[key] = value
                response = self.prot_handler.serialize('Set successfully')

            elif command[0:6] == 'DELETE':
                key = self.prot_handler.deserialize(command[6:])
                try:
                    del self.database[key]
                    response = self.prot_handler.serialize('Deleted successfully')
                except:
                    response = self.prot_handler.serialize('No such key')

            elif command[0:5] == 'FLUSH':
                self.database.clear()
                response = self.prot_handler.serialize('Flushed successfully')
            print(response)
            print(self.database)
            data = bytes(response, 'ascii')
            conn.sendall(data)

if __name__ == "__main__":
    s = Server()
    s.run()
