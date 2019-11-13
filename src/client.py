import socket
import json
import sys
from game.game_numpy import GameNumpy
import numpy as np

def main():
    host, port, color = parse_arg()
    client = Client(host, port)
    game = GameNumpy()

    try:
        # present name
        client.send_name("Ragnarok")
        # wait init state
        state, turn = client.recv_state()
        # game loop:
        while True:
            print(state)
            if color.upper() == turn:
                move = next_move(game, state, turn)
                client.send_move(move)
            state, turn  = client.recv_state()

    finally:
        print('closing socket')
        client.close()


############### TCP Client class
class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def send_name(self, name):
        encoded = name.encode("UTF-8")
        length = len(encoded).to_bytes(4, 'big')
        self.sock.sendall(length+encoded)

    def send_move(self, move):
        move_obj = {
            "from": chr(97 + move[0,1]) + str(move[0,0]+1),
            "to": chr(97 + move[1,1]) + str(move[1,0]+1)
        }
        encoded = json.dumps(move_obj).encode("UTF-8")
        length = len(encoded).to_bytes(4, 'big')
        self.sock.sendall(length+encoded)

    def recv_state(self):
        char = self.sock.recv(1)
        while(char == b'\x00'):
            char = self.sock.recv(1)
        length_str = char + self.sock.recv(1)
        total = int.from_bytes(length_str, "big")
        msg = self.sock.recv(total)
        state_obj = json.loads(msg.decode("UTF-8"))
        board = np.array(state_obj["board"])
        turn = state_obj["turn"]
        state = np.zeros((9,9), dtype = int)
        for i in range(9):
            for j in range(9):
                if board[i,j] == "BLACK":
                    state[i,j] = -1
                if board[i,j] == "WHITE":
                    state[i,j] = 1
                if board[i,j] == "KING":
                    state[i,j] = 2
        return state, turn

    def close(self):
        self.sock.close()


############### Argument parser
def parse_arg():

    def usage():
        print("Usage: client server_host <white | black>")

    if len(sys.argv) != 3:
        usage()
        exit(1)

    color=sys.argv[2]
    if color == "white":
        return (sys.argv[1], 5800, color)
    elif color == "black":
        return (sys.argv[1], 5801, color)
    else:
        usage()
        exit(1)

if __name__ == '__main__': main()