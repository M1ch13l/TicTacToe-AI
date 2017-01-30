class TicTacToe:
    """The game"""
    x = 1
    o = -1
    types = {x, o}

    def __init__(self, size):
        self.board = [0 for i in range(size*size)]
        self.size = size

    def __str__(self):
        return_string = ''
        size = "{:<2}"
        for x in range(self.size):
            for y in range(self.size):
                return_string += "|" + size.format(str(self.get_board(x, y)))
            return_string += "|" + "\n"
        return return_string

    def get_board(self, x, y):
        return self.board[x + (self.size*y)]

    def set_board(self, x: int, y: int, player: "String 'X' or '0'") -> None:
        self.board[x + (self.size*y)] = player

    def place(self, location: tuple, player: "String 'X' or '0'") -> "Winner 'X' or 'O'":
        if not self.is_empty(location):
            return -1
        x, y = location
        self.set_board(x, y, player)
        return self.game_over(location, player)

    def is_empty(self, location):
        """
        returns:
         0: already there
         1: there is space
        """
        x, y = location
        if self.get_board(x, y) in self.types:
            return 0
        return 1

    def game_over(self, location, player):
        x, y = location

        for i in range(self.size):
            if self.get_board(i, y) is not player:
                break
            if i == self.size - 1:
                return player

        for i in range(self.size):
            if self.get_board(x, i) is not player:
                break
            if i == self.size - 1:
                return player

        if x == y:
            for i in range(self.size):
                if self.get_board(i, i) is not player:
                    break
                if i == self.size - 1:
                    return player

        if x + y == self.size - 1:
            for i in range(self.size):
                if self.get_board(i, (self.size-1)-i) is not player:
                    break
                if i == self.size - 1:
                    return player

        if 0 not in self.board:
            return None

        return 0

import numpy as np
import random

class Player:
    def __init__(self, game: TicTacToe, player):
        self.g = game
        self.p = player
        self.r = random.seed()
        self.w = np.random.random((len(game.board),len(game.board)))

    def calculateNextMove(self):
        b = np.array(self.g.board)
        o = b.dot(self.w)

        while True:
            move = o.argmax()
            if self.g.board[move] is 0:
                break
            o[move] = o.min() - 1

        return move % self.g.size, int(move / self.g.size)

game_over = 0
t = TicTacToe(3)
t.place((0,1), t.x)
players = Player(t, t.o), Player(t, t.x)

while game_over is 0:
    for p in players:
        next_move = p.calculateNextMove()
        print(p, next_move)
        game_over = t.place(next_move, p.p)
        print(t)
        if game_over is not 0:
            break

print(game_over)



