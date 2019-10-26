import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5800)
sock.bind(server_address)

sock.listen(1)

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from')

        while True:
            data = connection.recv(64)
            if data:
                print('received: ', data)
            else:
                print('no more data from: ', client_address)
                break
    finally:
        connection.close()
