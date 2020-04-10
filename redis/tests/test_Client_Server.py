import subprocess
import time
from ..Client import Client


def test_server_with_single_client():
    p = subprocess.Popen(['python', 'redis/Server.py'])
    time.sleep(0.1)
    client = Client()
    response = client.set(4, "aaa")
    assert response == '+Set successfully\r\n'
    p.terminate()
