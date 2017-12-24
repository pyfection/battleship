

import random

from kivy.clock import Clock

from errors import NotYourTurnError
from controller.actor import Actor
from controller.board import Board
from errors import ValidationError


class Game:
    def __init__(self):
        self.actors = [
            Actor(self, 'player1'),
            Actor(self, 'player2'),
        ]

    def setup(self):
        for actor in self.actors:
            actor.setup(
                board=Board(),
                enemy_board=Board(ships={}),
            )

    def finish_setup(self, actor):
        if all([a.stage != 'setup' for a in self.actors]):
            actor = random.choice(list(self.actors))
            actor.do_turn()

    def try_hit_other(self, origin_actor, coord):
        if not origin_actor.has_turn:
            raise NotYourTurnError
        for enemy_actor in self.actors:
            if origin_actor == enemy_actor:
                continue  # Actor can't attack himself
            is_ship = enemy_actor.board.is_ship(coord)
            if is_ship:
                enemy_actor.enemy_hit(coord)
                enemy_ships = set(enemy_actor.board.get_ships())
                guessed_ships = set(origin_actor.enemy_board.get_ships())
                print('###########')
                print(enemy_ships)
                print(guessed_ships)
                if enemy_ships == guessed_ships:
                    enemy_actor.inform_win(origin_actor)
                    origin_actor.inform_win(origin_actor)
            else:
                origin_actor.has_turn = False
                enemy_actor.enemy_missed(coord)
                Clock.schedule_once(lambda dt: enemy_actor.do_turn())
            return is_ship
