import sys
sys.path.insert(0, '..')

from config import config, game_config

class Model:
    def __init__(self):

        self._super_mode = False
        self.online_mode = False
        self.port = "8005"
        self.ip_address = "127.0.0.1"
        self.update_super_mode()
        self.update_online_mode()

    @property
    def super_mode(self):
        return self._super_mode

    @super_mode.setter
    def super_mode(self, value):
        self._super_mode = value
        self.update_super_mode()

    def update_super_mode(self):
        config.IS_SUPERSUPERHIRN = self._super_mode
        print("update")

    @property
    def online_mode(self):
        return self._online_mode

    @online_mode.setter
    def online_mode(self, value):
        self._online_mode = value
        self.update_online_mode()

    def update_online_mode(self):
        if self._online_mode:
            game_config.CODER_IS_COMPUTER_SERVER = True
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.COMPUTER_IS_NETWORK = True
        else:
            game_config.CODER_IS_COMPUTER_SERVER = False
            game_config.CODER_IS_COMPUTER_LOCAL = True
            game_config.COMPUTER_IS_NETWORK = False