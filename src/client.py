import socket
import json
import sys
import math
from aima.search import Problem, Node, breadth_first_graph_search

if len(sys.argv) != 3:
    print("Usage: client server_host server_port")
    exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (sys.argv[1], int(sys.argv[2]))
sock.connect(server_address)

try:
    # sending name
    sock.sendall(b'Ragnarok')

    #data = sock.recv(64)
    #print(data)

    while True:
        time.sleep(0.2)

    message = {
        "x": "A",
        "y": 5,
        "direction": 1,
        "amount": 4
    }
    sock.sendall(json.dumps(message).encode('utf-8'))

finally:
    print('closing socket')
    sock.close()
