import socket
import json
import sys
import math
import time
import game

def usage():
    print("Usage: client server_host <white | black>")

if len(sys.argv) != 3:
    usage()
    exit(1)

color=sys.argv[2]
if color == "white":
    port = 5800
elif color == "black":
    port = 5801
else:
    usage()
    exit(1)

def send_utf(sock, string):
    encoded = string.encode("UTF-8")
    length = len(encoded).to_bytes(4, 'big')
    sock.sendall(length+encoded)

def recv_json(sock):
    char = sock.recv(1)
    while(char == b'\x00'):
        char = sock.recv(1)
    length_str = char + sock.recv(1)
    total = int.from_bytes(length_str, "big")
    msg = sock.recv(total)
    deserialized = json.loads(msg.decode("UTF-8"))
    return deserialized

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (sys.argv[1], port)
sock.connect(server_address)

try:
    # present name
    send_utf(sock, "Ragnarok")

    # wait init state
    state = recv_json(sock)    

    # game loop:
    while True:
        print(state)
        if color.upper() == state["turn"]:
            move = game.next_move(state)
            send_utf(sock, json.dumps(move))
        state = recv_json(sock)

finally:
    print('closing socket')
    sock.close()