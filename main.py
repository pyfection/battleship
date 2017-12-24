

from kivy.app import App

from controller.game import Game
from controller.actor import Local, AI


class GameApp(App):
    def build(self):
        game = Game()
        game.actors = [
            Local(game=game, name='player1'),
            AI(game=game, name='player2'),
        ]
        view = game.actors[0].view
        game.setup()
        return view


if __name__ == '__main__':
    GameApp().run()
