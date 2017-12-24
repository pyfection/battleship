

import random
from time import sleep

from view.board import Board


class Actor:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.board = None
        self.enemy_board = None
        self.stage = 'setup'
        self.has_turn = False

    def setup(self, board, enemy_board):
        self.board = board
        self.enemy_board = enemy_board

    def do_turn(self):
        self.has_turn = True

    def finish_setup(self):
        self.board.validate()
        self.stage = 'play'
        self.game.finish_setup(self)

    def try_hit(self, coord):
        has_hit = self.game.try_hit_other(self, coord)
        if has_hit:
            self.enemy_board.place(coord)
        return has_hit

    def enemy_hit(self, coord):
        self.enemy_board.place(coord)

    def enemy_missed(self, coord):
        pass

    def inform_win(self, actor):
        self.stage = 'end'
        self.has_turn = False


class Connector:
    pass


class Visualizer:
    def __init__(self):
        self.view = Board(self)

    def setup(self):
        self.view.generate()

    def enemy_hit(self, coord):
        self.view.enemy_hit(coord)

    def enemy_missed(self, coord):
        self.view.enemy_missed(coord)

    def inform_win(self, actor):
        self.view.inform_win(actor)


class Local(Actor, Visualizer):
    def __init__(self, game, name):
        Actor.__init__(self, game, name)
        Visualizer.__init__(self)

    def do_turn(self):
        super(Local, self).do_turn()
        self.view.do_turn()

    def setup(self, board, enemy_board):
        Actor.setup(self, board, enemy_board)
        Visualizer.setup(self)

    def enemy_hit(self, coord):
        Actor.enemy_hit(self, coord)
        Visualizer.enemy_hit(self, coord)

    def enemy_missed(self, coord):
        Actor.enemy_missed(self, coord)
        Visualizer.enemy_missed(self, coord)

    def inform_win(self, actor):
        Actor.inform_win(actor)
        Visualizer.inform_win(actor)


class AI(Actor):
    def __init__(self, game, name):
        super(AI, self).__init__(game, name)
    
    def setup(self, board, enemy_board):
        board.fill_randomly()
        super(AI, self).setup(board, enemy_board)
        self.finish_setup()

    def do_turn(self):
        super(AI, self).do_turn()
        while self.has_turn:
            sleep(2)
            try:
                coord = random.choice(list(self.enemy_board.unknowns()))
            except StopIteration:
                raise StopIteration("No more fields to uncover, this should not be possible!")
            super(AI, self).try_hit(coord)


class Socket(Actor, Connector):
    pass


class Client(Visualizer):
    pass
