import socket

class Server(object):
    def __init__(self, host='127.0.0.1', port=31337):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()

        self.database = dict()
    
    def run(self):
        conn, addr = self.socket.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
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
                conn.sendall(data)

if __name__ == "__main__":
    s = Server()
    s.run()
