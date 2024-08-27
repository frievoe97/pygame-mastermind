# The PlayAsCodeBreakerCommand class defines a command to play as a code breaker

from config import game_config

from .command import Command
import sys
sys.path.insert(0, '..')
from constants import GAME

# The PlayAsCodeBreakerCommand class defines a command to play as a code breaker.
class PlayAsCodeBreakerCommand(Command):
    
    
    def execute(self):
        """
        The method sets up the game configuration based on the player's choices and starts a new game.
        """

        print("Command Playing as CodeBreaker is being executed...")

        game_config.PLAYER_IS_GUESSER = True
        game_config.GUESSER_IS_PLAYER = True
        game_config.GUESSER_IS_COMPUTER = False
        game_config.CODER_IS_PLAYER = False

        if self.main_app.online_settings_model.online_mode:
            game_config.IP_ADDRESS = self.main_app.online_settings_model.ip_address
            game_config.PORT = self.main_app.online_settings_model.port
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.CODER_IS_COMPUTER_SERVER = True
        else:
            game_config.CODER_IS_COMPUTER_LOCAL = True
            game_config.CODER_IS_COMPUTER_SERVER = False

        self.main_app.start_new_game()

    def __str__(self):
        """
        The function returns a string that says "CodeBreaker Spielen".
        :return: The string "CodeBreaker Spielen" is being returned.
        """
        return "CodeBreaker Spielen"
    