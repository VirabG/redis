import subprocess
import time
from ..Client import Client

<<<<<<< HEAD

def test_server_with_single_client():
    p = subprocess.Popen(['python', 'redis/Server.py'])
    time.sleep(0.5)
    try:
        client = Client()
        response = client.set(4, "aaa")
        assert response == '+Set successfully\r\n'
    finally:
        p.terminate()


def test_server_set_get():
    p = subprocess.Popen(['python', 'redis/Server.py'])
    time.sleep(0.5)
    try:
        client = Client()
        response = client.set(4, "aaa")
        response = client.get(4)
        assert response == '+aaa\r\n'
    finally:
        p.terminate()
=======
def test_echo_server_with_single_client():
    p = subprocess.Popen(['python3', 'Server.py'])
    time.sleep(1.1)
    client = Client()
    response = client.set(4, "aaa")
    assert response == "('SET', 4, 'aaa')"
    p.terminate()

"""
def test_Server_State_Save():
    p = subprocess.Popen(['python', 'Server.py'])
    time.sleep(0.1)
    client = Client()
"""
>>>>>>> communication
