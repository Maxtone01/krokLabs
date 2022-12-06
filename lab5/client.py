import socket
import os
import pathlib
import time
import threading


BASE_DIR = pathlib.Path(__file__).parent.resolve()
HOST = 'localhost'
PORT = 3702
SIZE = 1024
UTF8 = 'utf-8'
UPLOAD = 'upload'
DOWNLOAD = 'download'


def send_file(filename):
    sock = socket.socket()
    sock.connect((HOST, PORT))

    try:
        sock.sendall(f'{UPLOAD}: {filename}\r\n'.encode(UTF8))

        if sock.recv(SIZE) == b'filename received':
            path = os.path.join(BASE_DIR, 'files', filename)
            with open(path, 'rb') as f:
                data = f.read(SIZE)
                while data:
                    sock.sendall(data)
                    data = f.read(SIZE)
    finally:
        print('Finished.')
        sock.close()


def download_file(filename):
    sock = socket.socket()
    sock.connect((HOST, PORT))

    try:
        sock.sendall(f'{DOWNLOAD}: {filename}\r\n'.encode(UTF8))

        if sock.recv(SIZE) == b'filename received':
            path = os.path.join(BASE_DIR, 'downloaded', filename)
            with open(path, 'ab') as f:
                data = sock.recv(SIZE)
                while data:
                    f.write(data)
                    data = sock.recv(SIZE)
    finally:
        print('Finished.')
        sock.close()


def send_files():
    filename1 = 'image1.jpg'
    filename2 = 'image2.jpg'
    th1 = threading.Thread(target=send_file, args=(filename1,))
    th2 = threading.Thread(target=send_file, args=(filename2,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()


def download_files():
    filename1 = 'image1.jpg'
    filename2 = 'image2.jpg'
    th1 = threading.Thread(target=download_file, args=(filename1,))
    th2 = threading.Thread(target=download_file, args=(filename2,))

    th1.start()
    th2.start()

    th1.join()
    th2.join()


if __name__ == '__main__':
    send_files()
    download_files()
