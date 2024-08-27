
from constants import GAME
from .command import Command
from config import game_config

import sys
sys.path.insert(0, '..')


class HumanVsHuman(Command):
    def execute(self):

        print("Executing the Human vs Human command...")


        if self.main_app.online_settings_model.online_mode:
            
           return print("Gamemode does not exist")

        game_config.PLAYER_IS_GUESSER = True
        game_config.GUESSER_IS_COMPUTER = False
        game_config.GUESSER_IS_PLAYER = True
        game_config.CODER_IS_PLAYER = True
        game_config.CODER_IS_COMPUTER_LOCAL = False
        game_config.CODER_IS_COMPUTER_SERVER = False
        
        self.main_app.start_new_game()

    def __str__(self):
        return "Human vs Human"
