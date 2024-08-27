# The EditOnlineSettings class is a subclass of the Command class that sets the main app state to
# ONLINE_SETTINGS

import sys
from .command import Command
sys.path.insert(0, '..')
from constants import ONLINE_SETTINGS


# The `EditOnlineSettings` class is a command that sets the state of the
# main app to "ONLINE_SETTINGS".
class EditOnlineSettings(Command):
    
    def execute(self):
        """
        The function "execute" sets the state of the main app to
        "ONLINE_SETTINGS".
        """
        print("The Online Settings command is being executed...")
        self.main_app.set_state(ONLINE_SETTINGS)

    def __str__(self):
        """
        The function returns the string "Einstellungen".
        :return: The string "Einstellungen" is being returned.
        """
        return "Einstellungen"