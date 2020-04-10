import asyncio
from .ProtocolHandler import ProtocolHandler


class Client(object):

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.prot_handler = ProtocolHandler()

    def command_to_message(self, args):
        """
            The function transforms the command to execute into a transferable string form.
            :param args: The first argument is in ('GET', 'SET', 'DELETE', 'FLUSH')
            :return: a string containing the arguments - serialized and concatenated
        """
        msg = ''
        assert args[0] in ('GET', 'SET', 'DELETE', 'FLUSH'), 'Wrong Command! The command must be in (SET, GET, DELETE, FLUSH)'
        n_args = len(args)
        msg += args[0]
        if msg == 'SET':
            assert n_args == 3, 'Wrong Command: SET must have exactly two arguments, the key and the value'
            assert ((type(args[1]) is int) or (type(args[1]) is str)), \
                'Wrong Command: key type in SET must be either "int" or "str"'
            msg += self.prot_handler.serialize(args[1])
            msg += self.prot_handler.serialize(args[2])

        elif msg == 'GET':
            assert n_args == 2, 'Wrong Command: GET must have exactly one argument, the key'
            assert ((type(args[1]) is int) or (type(args[1]) is str)), \
                'Wrong Command: key type in GET must be either "int" or "str"'
            msg += self.prot_handler.serialize(args[1])

        elif msg == 'DELETE':
            assert n_args == 2, 'Wrong Command: DELETE must have exactly one argument, the key'
            assert ((type(args[1]) is int) or (type(args[1]) is str)), \
                'Wrong Command: key type in DELETE must be either "int" or "str"'
            msg += self.prot_handler.serialize(args[1])

        else:  # command == FLUSH
            assert n_args == 1, 'Wrong Command: FLUSH must not have any arguments'

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
    resp1 = c.get(5)
    print(resp1)
