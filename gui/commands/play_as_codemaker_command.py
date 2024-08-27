# The PlayAsCodeMakerCommand class defines a command to play as a CodeMaker
from constants import GAME
from .command import Command
from config import game_config

import sys
sys.path.insert(0, '..')


# The PlayAsCodeMakerCommand class defines a command to play as a CodeMaker
class PlayAsCodeMakerCommand(Command):
    def execute(self):

        print("Executing Play As CodeMaker command...")

        game_config.PLAYER_IS_GUESSER = False
        game_config.GUESSER_IS_COMPUTER = True
        game_config.GUESSER_IS_PLAYER = False
        game_config.CODER_IS_PLAYER = True

        if self.main_app.online_settings_model.online_mode:
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.CODER_IS_COMPUTER_SERVER = False
            game_config.IP_ADDRESS = self.main_app.online_settings_model.ip_address
            game_config.PORT = self.main_app.online_settings_model.port

        else:
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.CODER_IS_COMPUTER_SERVER = False

        self.main_app.start_new_game()

    def __str__(self):
        return "CodeMaker Spielen"
