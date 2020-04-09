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

#                ##TODO: process SET and GET, FLUSH and DELETE

        if request[:3] == 'GET':
            key = self.prot_handler.deserialize(request[3:])
            try:
                response = self.prot_handler.serialize(self.database[key])
            except:
                response = self.prot_handler.serialize('No such key') # What if the value of the key is 'No such key'

        elif request[:3] == 'SET':
            key_end = request.find(LINE_SEPARATOR)
            key = self.prot_handler.deserialize(request[3:key_end + SEPARATOR_LENGTH])
            value = self.prot_handler.deserialize(request[key_end + SEPARATOR_LENGTH:])
            self.database[key] = value
            response = self.prot_handler.serialize('Set successfully')

        elif request[:6] == 'DELETE':
            key = self.prot_handler.deserialize(request[6:])
            try:
                del self.database[key]
                response = self.prot_handler.serialize('Deleted successfully')
            except:
                response = self.prot_handler.serialize('No such key')

        elif request[:5] == 'FLUSH':
            self.database.clear()
            response = self.prot_handler.serialize('Flushed successfully')

        else:
            response = self.prot_handler.serialize('Wrong Command! The command must be in (GET, SET, DELETE, FLUSH)')

        return response


    async def handle_request(self, reader, writer):
        ###TODO: process data here and send response back to client
        data = await reader.read(100)
        message = data.decode()    # should we change this 'message' to request?
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        message = self.get_response(message)

        print("Send: %r" % message)
        writer.write(message.encode())
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
