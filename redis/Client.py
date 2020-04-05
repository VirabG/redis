import asyncio
from ProtocolHandler import ProtocolHandler
import time


class Client(object):

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.prot_handler = ProtocolHandler()

    def command_to_message(self, args):
    #    ###TODO: parse a command which is given in args, send it to server and receive response
    #        command = ''
    #        assert args[0] in ('GET', 'SET', 'DELETE', 'FLUSH'), 'Wrong Command!'
    #        n_args = len(args)
    #        command += args[0]
    #        if command == 'GET' or command == 'DELETE' or command == 'SET':
    #            assert n_args >= 2, 'Wrong Command: no key given for SET/GET/DELETE'
    #            assert (type(args[1] is int) or type(args[1]) is str), 'Wrong Command: key type in SET/GET/DELETE must be either "int" or "str"'
    #            command += self.prot_handler.serialize(args[1])
    #
    #            if command[0:3] == 'SET':
    #                assert n_args == 3, 'Wrong Command: SET must have exactly two arguments, the key and the value'
    #                command += self.prot_handler.serialize(args[2])
    #            else:
    #                assert n_args == 2, 'Wrong Command: GET/DELETE must have exactly one argument, the key'
    #        else: # the command is FLUSH
    #            assert n_args == 1, 'Wrong Command: FLUSH must not have any arguments'
    #        # self.socket.sendall(b'Hello, world')
    #        command_bytes = bytes(command, 'ascii')
    #
    #        # at the beginning we add the number of bytes to be transferred
    #        # n_bytes = len(command_bytes)
    #        # command_bytes = bytes(str(n_bytes), 'ascii') + command_bytes
    #
    #        self.socket.send(command_bytes)
    #
    #        # all hell breaks loose
    #        #while True:
    #        #    data = self.socket.recv(128)
    #        #    if not data:
    #        #        break
    #        #data = self.socket.recv(128)
    #        #print(data)
    #
        msg = str(args)
        return msg

    async def send_request_and_get_response(self, message, loop):
        reader, writer = await asyncio.open_connection(self.host, self.port,
                                                       loop=loop)

        print('Send: %r' % message)
        writer.write(message.encode())

        data = await reader.read(100)
        print('Received: %r' % data.decode())

        print('Close the socket')
        writer.close()

        return data.decode('ascii')

    def execute(self, *args):
        msg = self.command_to_message(args)
        
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.send_request_and_get_response(msg, loop))
        loop.close()

        return response

    def get(self, key):
        return self.execute('GET', key)

    def set(self, key, value):
        return self.execute('SET', key, value)

    def delete(self, key):
        return self.execute('DELETE', key)

    def flush(self):
        return self.execute('FLUSH')

if __name__ == "__main__":
    c = Client()
    c.set(4, "aaa")
