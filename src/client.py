import socket
import json
import sys
import numpy as np
from heuristic.eval_numpy import HeuristicNumpy
from game.game_numpy import GameNumpy
from search.alphabeta import start_search

def main():
    host, port, color = parse_arg()
    client = Client(host, port)
    game = GameNumpy()
    heuristic = HeuristicNumpy()

    try:
        # present name
        client.send_name("Ragnarok")
        # wait init state
        state, turn = client.recv_state()
        # game loop:
        while True:
            heuristic.update(state)
            if color == turn:
                move = start_search(game, state, turn, heuristic)
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
        turn = 1 if state_obj["turn"] == "WHITE" else -1
        state = np.zeros((9,9), dtype = int)
        board = np.array(json.loads(msg.decode("UTF-8"))["board"])
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
        return (sys.argv[1], 5800, 1)
    elif color == "black":
        return (sys.argv[1], 5801, -1)
    else:
        usage()
        exit(1)

if __name__ == '__main__': main()