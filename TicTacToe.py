import numpy as np
import random


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

    def set_board(self, x: int, y: int, player: int) -> None:
        self.board[x + (self.size*y)] = player

    def place(self, location: tuple, player: int) -> int:
        if not self.is_empty(location):
            return -1
        x, y = location
        self.set_board(x, y, player)
        return self.game_over(location, player)

    def is_empty(self, location: tuple):
        """
        returns:
         0: already there
         1: there is space
        """
        x, y = location
        if self.get_board(x, y) in self.types:
            return 0
        return 1

    def game_over(self, location: tuple, player: int):
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


class Player:
    def __init__(self, game: TicTacToe, player: int):
        self.game = game
        self.player = player
        self.weights = np.random.random((len(game.board) * 2, len(game.board)))
        self.weights_old = np.subtract(self.weights, np.multiply(self.weights, 0.1))

    def calculate_next_move(self):
        b = np.array(self.game.board)
        if self.player < 0:
            b = np.concatenate((np.negative(b), b), axis=0)
        else:
            b = np.concatenate((b, np.negative(b)), axis=0)
        o = b.dot(self.weights)

        while True:
            move = o.argmax()
            if self.game.board[move] is 0:
                break
            o[move] = o.min() - 1

        return move % self.game.size, int(move / self.game.size)


random.seed()
game_over = 0
t = TicTacToe(3)
t.place((random.randint(0, 2), random.randint(0, 2)), t.x)
players = Player(t, t.o), Player(t, t.x)
xwins = 0
owins = 0

for i in range(1000):
    while game_over is 0:
        for p in players:
            next_move = p.calculate_next_move()
            game_over = t.place(next_move, p.player)
            if game_over is not 0:
                break

    #p = players[0]
    for p in players:
        if game_over is p.player:
            p.weights += np.subtract(p.weights, p.weights_old)
        if game_over is -p.player:
            p.weights -= np.subtract(p.weights, p.weights_old)
        p.weights += np.multiply(np.subtract(np.random.random((len(p.game.board) * 2, len(p.game.board))), 0.5), 0.001)
        p.weights_old = p.weights
        #print(p.player, p.weights)

    #if game_over is not None:
    #    print(t, i, game_over)
    if game_over is t.x:
        xwins += 1
    if game_over is t.o:
        owins += 1
    game_over = 0
    t.board = [0 for i in range(t.size*t.size)]

print(xwins, owins)



