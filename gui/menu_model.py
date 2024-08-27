# The MenuModel class initializes a list of menu items for a game,
# including options to play as a code breaker or maker,
# edit online settings, and quit the game.

from typing import TYPE_CHECKING
from .commands.play_as_codebreaker_command import PlayAsCodeBreakerCommand
from .commands.play_as_codemaker_command import PlayAsCodeMakerCommand
from .commands.edit_online_settings_command import EditOnlineSettings
from .commands.quit_game_command import QuitGameCommand
from .commands.computer_vs_computer_command import ComputerVsComputer
from .commands.human_vs_human_command import HumanVsHuman

if TYPE_CHECKING:
    import sys
    sys.path.insert(0, '..')
    from main import MainApp

# The MenuModel class initializes a list of menu items for the game.
class MenuModel:
    def __init__(self, main_app: 'MainApp'):
        """
        This function initializes a list of menu items for the game, including options to play as a code
        breaker or maker, edit online settings, and quit the game.
        """
        self.menu_items = [
            PlayAsCodeBreakerCommand(main_app),
            PlayAsCodeMakerCommand(main_app),
            ComputerVsComputer(main_app),
            HumanVsHuman(main_app),
            EditOnlineSettings(main_app),
            QuitGameCommand(main_app)
        ]
