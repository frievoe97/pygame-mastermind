"""
This module defines the Command abstract base class (ABC). Subclasses of Command
should implement the execute and __str__ methods. The Command ABC can be used as
a template for creating commands that interact with a MainApp instance.
"""

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    import sys
    sys.path.insert(0, '..')
    from main import MainApp


class Command(ABC):
    """
    This is an abstract base class for commands. The constructor accepts a main_app parameter.

    :param main_app: The main application object that the method will interact with or modify.
    """

    def __init__(self, main_app: 'MainApp'):
        """
        The constructor initializes an instance of a command with a reference to the
        main application.

        :param main_app: The main_app parameter is an instance of the 'MainApp' class. It is passed to the
        __init__ method as an argument and assigned to the self.main_app attribute. This allows the current
        command object to access and interact with the main_app instance
        :type main_app: 'MainApp'
        """
        self.main_app = main_app

    @abstractmethod
    def execute(self):
        """
        Execute method to be implemented by each concrete Command.
        Uses the MainApp instance stored in self.main_app.
        """

    @abstractmethod
    def __str__(self):
        """
        Abstract method to return a string representation of the Command.
        """
