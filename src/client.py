import socket
import json
import sys
import numpy as np
from search.negamax import Search

def main():
    host, port, color = parse_arg()
    client = Client(host, port)
    search = Search(color)

    try:
        # present name
        client.send_name("Ragnarok")
        # wait init state
        state_np, state_obj, turn = client.recv_state()
        # game loop:
        while True:
            if color == turn:
                move = search.start(state_obj)
                if move != None:
                    client.send_move(move)
            state_np, state_obj, turn = client.recv_state()

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

    def send_move(self, move, t="obj"):
        if t=="obj":
            move_obj = {
                "from": chr(97 + move[0][1]) + str(move[0][0]+1),
                "to": chr(97 + move[1][1]) + str(move[1][0]+1)
            }
        if t=="numpy":
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
        board = state_obj["board"]
        turn = 1 if state_obj["turn"] == "WHITE" else -1

        state_obj = list(board)
        state_numpy = np.zeros((9,9), dtype = int)
        for i in range(9):
            for j in range(9):
                if state_obj[i][j] == "BLACK":
                    state_numpy[i,j] = -1
                    state_obj[i][j] = -1
                if state_obj[i][j] == "WHITE":
                    state_numpy[i,j] = 1
                    state_obj[i][j] = 1
                if state_obj[i][j] == "KING":
                    state_numpy[i,j] = 2
                    state_obj[i][j] = 2
                if state_obj[i][j] == "EMPTY" or  state_obj[i][j] == "THRONE":
                    state_obj[i][j] = 0

        return state_numpy, state_obj, turn

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