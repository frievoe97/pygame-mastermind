# The MenuCommand class is a command that sets the state of the main app to MENU when executed.
import sys
from .command import Command
sys.path.insert(0, '..')
from constants import MENU


# The MenuCommand class is a command that sets the state of the main app to MENU when executed.
class MenuCommand(Command):
    
    def execute(self):
        """
        The `execute` function sets the state of the main app to MENU.
        """
        print("Executing the Menu command...")
        self.main_app.set_state(MENU)

    def __str__(self):
        """
        The function returns the string "Open Menu".
        :return: The string "Open Menu" is being returned.
        """
        return "Open Menu"