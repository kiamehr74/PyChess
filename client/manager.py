#python imports
import copy

#project imports
from worldmodel import WorldModel
from connection import Connection
from parser import Parser
import ai


class Manager:
    def __init__(self):
        self.wm = WorldModel()
        self.conn = Connection()


    def init(self):
        self.conn.connect()
        name = input('Enter your name: ')
        self.conn.send(name.encode('UTF-8'))

        my_color = self.conn.recv(1).decode()
        other_team_name = self.conn.recv(32).decode()

        if my_color == '1':
            white_team_name = name
            black_team_name = other_team_name
        elif my_color == '0':
            white_team_name = other_team_name
            black_team_name = name

        self.wm.init(white_team_name, black_team_name, int(my_color))


    def run(self):
        turn = 1
        while True:
            turn_color = turn % 2
            is_white = bool(turn_color)

            try:
                if self.wm.my_color == turn_color:
                    move = ai.decide(copy.deepcopy(self.wm))
                    self.conn.send(Parser.encode(turn, move))
            except:
                pass

            t, m = Parser.decode(self.conn.recv(4))
            if t == turn:
                self.wm.do_move(m, is_white)

            turn += 1
            print (self.wm)
