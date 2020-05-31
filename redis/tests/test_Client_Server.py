import subprocess
import time
from ..Client import Client
import pickle


def test_server_with_single_client():
    p = subprocess.Popen(['python3', 'Server.py'])
    time.sleep(0.5)
    try:
        client = Client()
        response = client.set(4, "aaa")
        assert response == '+Set successfully\r\n'
    finally:
        p.terminate()


def test_server_set_get():
    p = subprocess.Popen(['python3', 'Server.py'])
    time.sleep(0.5)
    try:
        client = Client()
        response = client.set(4, "aaa")
        response = client.get(4)
        assert response == '+aaa\r\n'
    finally:
        p.terminate()

def test_echo_server_with_single_client():
    p = subprocess.Popen(['python3', 'Server.py'])
    time.sleep(0.5)
    client = Client()
    response = client.set(4, "aaa")
    assert response == "+Set successfully\r\n"
    p.terminate()


def test_Server_State_Save():
    p = subprocess.Popen(['python3', 'Server.py'])
    time.sleep(0.5)
    c = Client()

    # First we flush the database, st we are aware of the state of the database
    # test FLUSH - Save Server State
    c.flush()
    time.sleep(2.5)
    with open('database.dictionary', 'rb') as f:
        d = pickle.load(f)

    if d != {}:
        p.terminate()
        print(d)
        assert 0 == 1

    # test SET, GET, DELETE - Save State
    c.set('k2', 2)
    c.set(4, 16)
    c.set(5,'pix')
    resp = c.get('k2')

    if resp != ":2\r\n":
        p.terminate()
        print(resp)
        assert 0 == 1

    c.set(3, 'pix')
    c.set(3, 9)
    c.set('k8', 40320)
    resp = c.delete(8)
    if resp != "+No such key\r\n":
        p.terminate()
        print(resp)
        assert 0 == 1

    c.delete(5)

    time.sleep(2.5)
    with open('database.dictionary', 'rb') as f:
        d = pickle.load(f)
    if d != {'k2':2, 4:16, 3:9, 'k8':40320}:
        p.terminate()
        print(d)
        assert 0 == 1
        
    p.terminate()






