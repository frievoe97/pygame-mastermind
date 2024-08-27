# The `ComputerVsComputer` command sets up the game configuration for a computer vs computer mode and
# starts a new game.
from constants import GAME
from .command import Command
from config import game_config

import sys
sys.path.insert(0, '..')


"""
The `ComputerVsComputer` command sets up the game configuration for a computer vs computer mode and
starts a new game.
"""
class ComputerVsComputer(Command):
    def execute(self):
        """
        The method sets up the game configuration for a computer vs computer mode and starts a new game.
        """
        print("Executing the Computer vs Computer command...")
        
        game_config.PLAYER_IS_GUESSER = False
        game_config.GUESSER_IS_COMPUTER = True
        game_config.GUESSER_IS_PLAYER = False
        game_config.CODER_IS_PLAYER = False

        if self.main_app.online_settings_model.online_mode:
            
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.CODER_IS_COMPUTER_SERVER = True

            game_config.IP_ADDRESS = self.main_app.online_settings_model.ip_address
            game_config.PORT = self.main_app.online_settings_model.port

        else:        
            game_config.CODER_IS_COMPUTER_LOCAL = True
            game_config.CODER_IS_COMPUTER_SERVER = False
        
        self.main_app.start_new_game()

    def __str__(self):
        """
        The method returns a string that says "Computer vs Computer".
        :return: The string "Computer vs Computer" is being returned.
        """
        return "Computer vs Computer"
