# The QuitGameCommand class defines a command to quit the game and exit the program.
from .command import Command
import sys


# The QuitGameCommand class defines a command to quit the game and exit the program.
class QuitGameCommand(Command):
    def execute(self):
        """
        The function terminates the program.
        """
        sys.exit()
    
    def __str__(self):
        """
        The function returns the string "Beenden".
        :return: The string "Beenden" is being returned.
        """
        return "Beenden"