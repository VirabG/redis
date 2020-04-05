import asyncio

from ProtocolHandler import ProtocolHandler
from ProtocolHandler import LINE_SEPARATOR, SEPARATOR_LENGTH
import time

class Server(object):
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

        self.database = dict()
        self.prot_handler = ProtocolHandler()

    def get_response(self, request):
        return request
#                ##TODO: process SET and GET
#                ## SET or GET is the first word of data
#                ## SET key value
#                ## key is identifier alphanumeric
#                ## value is int string array or dict
#                ## if data[:3] == 'SET'
#                ##      process(SET)
#                ## self.database[key] = value
#                ## if data[:3] == 'GET'
#                ##      process(GET)
# 
#                #https://docs.python.org/3/howto/sockets.html
#                #first put length of message
#                #for short messages we can use socket.recv(length of message)
#                # for longer 
#                # while num_of_read_bytes < length_of_message:
#                #   message.append(socket.recv(1024))
#                #   num_of_read_bytes += 1024
#
#                print(data)
#                fulldata += data
#                #conn.sendall(data)
#            command = fulldata.decode('ascii')
#            print(command)
#            if command[0:3] == 'GET':
#                key = self.prot_handler.deserialize(command[3:])
#                try:
#                    response = self.prot_handler.serialize(self.database[key])
#                except:
#                    response = self.prot_handler.serialize('No such key')
#
#            elif command[0:3] == 'SET':
#                key_end = command.find(LINE_SEPARATOR)
#                key = self.prot_handler.deserialize(command[3:key_end + SEPARATOR_LENGTH])
#                value = self.prot_handler.deserialize(command[key_end + SEPARATOR_LENGTH:])
#                self.database[key] = value
#                response = self.prot_handler.serialize('Set successfully')
#
#            elif command[0:6] == 'DELETE':
#                key = self.prot_handler.deserialize(command[6:])
#                try:
#                    del self.database[key]
#                    response = self.prot_handler.serialize('Deleted successfully')
#                except:
#                    response = self.prot_handler.serialize('No such key')
#
#            elif command[0:5] == 'FLUSH':
#                self.database.clear()
#                response = self.prot_handler.serialize('Flushed successfully')
#            print(response)
#            print(self.database)
 

    async def handle_request(self, reader, writer):
        ###TODO: process data here and send response back to client
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        message = self.get_response(message)

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        print("Close the client socket")
        writer.close()
    
    def run(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_request, self.host, self.port, loop=loop)
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    s = Server()
    s.run()
