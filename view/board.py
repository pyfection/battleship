

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

import util
from errors import ValidationError
from view.widgets.field import Field


BLUE = (.2, .2, 1, 1)
GRAY = (.5, .5, .5, 1)
RED = (.5, 0, 0, 1)
WHITE = (1, 1, 1, 1)


class Board(BoxLayout):
    def __init__(self, actor):
        self.actor = actor
        super(Board, self).__init__()

    def generate(self):
        for board in ('board_own', 'board_enemy'):
            self.cols, self.rows = self.actor.board.SIZE
            for i in range(self.rows):
                for j in range(self.cols):
                    coord = util.to_coord(j, i)
                    if i == 0 and j == 0:
                        label = Label(size_hint=(None, None), size=(50, 50))
                        self.ids[board].add_widget(label)
                    elif i == 0:
                        label = Label(size_hint=(None, None), size=(50, 50), text=coord[0])
                        self.ids[board].add_widget(label)
                    elif j == 0:
                        label = Label(size_hint=(None, None), size=(50, 50), text=coord[1])
                        self.ids[board].add_widget(label)
                    else:
                        field = Field(background_color=BLUE)
                        field.coord = coord
                        field.background_color = BLUE
                        if board == 'board_enemy':
                            field.is_ship = None
                            field.disabled = True
                            field.bind(on_press=self.try_hit)
                        elif board == 'board_own':
                            field.is_ship = False
                            field.bind(on_press=self.place_ship)
                        self.ids[board].add_widget(field)

    def toggle_enemy_board(self, disable=True):
        for cell in self.ids.board_enemy.children:
            if hasattr(cell, 'coord'):
                if cell.is_ship is None:
                    cell.disabled = disable

    def finish_setup(self):
        try:
            self.actor.board.validate()
        except ValidationError as e:
            print(e)
            return
        board = {}  # ToDo: Investigate why it works without this being used
        for cell in self.ids.board_own.children:
            if hasattr(cell, 'coord'):
                board[cell.coord] = cell.is_ship
                cell.disabled = True
        # self.ids.board_own.disabled = True
        self.ids.setup_controls.disabled = True
        self.ids.setup_controls.width = 0
        self.actor.finish_setup()

    def do_turn(self):
        # self.ids.board_enemy.disabled = False
        self.toggle_enemy_board(disable=False)

    def place_ship(self, instance):
        self.actor.board.place(instance.coord)
        instance.is_ship = True
        instance.background_color = GRAY

    def try_hit(self, instance):
        assert self.actor
        coord = instance.coord
        has_hit = self.actor.try_hit(coord)
        if has_hit:
            instance.background_color = RED
            instance.is_ship = True
            instance.disabled = True
        else:
            instance.background_color = WHITE
            instance.is_ship = False
            instance.disabled = True
            # self.ids.board_enemy.disabled = True
            self.toggle_enemy_board()

    def enemy_hit(self, coord):
        for cell in self.ids.board_own.children:
            if hasattr(cell, 'coord') and cell.coord == coord:
                break
        else:
            return
        cell.background_color = RED

    def enemy_missed(self, coord):
        for cell in self.ids.board_own.children:
            if hasattr(cell, 'coord') and cell.coord == coord:
                break
        else:
            return
        cell.background_color = WHITE

    def inform_win(self, actor):
        self.ids.message.text = f"Player {actor.name} has won!"
