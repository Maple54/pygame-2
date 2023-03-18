import pygame,os
from states import State
from world import main_game
#from main_menu import Main_Menu



class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        #self.image =  os.path.join(os.getcwd(), "graphics", "ui", "introscreen.png")
        

    def update(self, delta_time, actions):
      if actions["start"]:
            new_state = main_game(self.game)
            new_state.enter_state()
      self.game.reset_keys()


    def render(self, display):
        display.fill('white')

        self.game.draw_text(display, "Adventure Lad", (0,0,0), self.game.GAME_W/2, self.game.GAME_H/2 )