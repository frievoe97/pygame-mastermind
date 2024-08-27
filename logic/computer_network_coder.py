import json
import requests

from config import config
from config import game_config
from constants import MENU_NEW

class ComputerNetworkCoder:
    def __init__(self, game):
        # Initialisierung der Variablen
        self.gameid = 0
        self.gamerid = game_config.GAMER_ID
        self.positions = config.COLUMNS
        self.colors = len(config.COLORS)
        self.value = ""
        self.game = game
        game_config.NO_NETWORK_CONNECTION = False

    def generate_code(self, board_view):
        self.send_request(self.gameid, self.gamerid, self.positions, self.colors, self.value)
        game_config.CODER_IS_PLAYING = False
        game_config.CODE_IS_CODED = True
        print("Der Server hat den geheimen Code generiert.")
        return True

    def rate_move(self, board_view, guesser):
        """
        Bewertet den aktuellen Zug des Spielers.
        """
        current_guess = game_config.BOARD_FINAL[game_config.CURRENT_ROW]

        string_guess = ""

        # Umwandeln des Rateversuchs in einen String
        for num in current_guess:
            if num != None:
                string_guess += str(num)

        # Senden eines Requests an den Server, um den Rateversuch zu bewerten
        self.send_request(self.gameid, self.gamerid, self.positions, self.colors, string_guess)

        # Zählen der Anzahl von weißen und schwarzen Pins in der Antwort
        white_pins = self.value.count('7')
        black_pins = self.value.count('8')

        for index in range(black_pins):
            board_view.board_feedback[game_config.CURRENT_ROW][index] = config.FEEDBACK_COLORS[1]

        for index in range(white_pins):
            board_view.board_feedback[game_config.CURRENT_ROW][index + black_pins] = config.FEEDBACK_COLORS[0]

        if black_pins is config.COLUMNS:
            # Der Spieler hat gewonnen
            game_config.GUESSER_WON = True
            game_config.GAME_IS_OVER = True
            game_config.SOLUTION = game_config.BOARD_FINAL[game_config.CURRENT_ROW]

        return black_pins, white_pins

    def send_request(self, gameid, gamerid, positions, colors, value):
        """
        Sendet eine Anfrage an einen Server mit den bereitgestellten Daten.

        Args:
            gameid (int): Die Spiel-ID.
            gamerid (str): Der Name des Spielers.
            positions (int): Die Anzahl der Positionen.
            colors (int): Die Anzahl der Farben.
            value (str): Der Wert.

        Returns:
            int: Die aktualisierte Spiel-ID.

        Raises:
            requests.exceptions.RequestException: Bei einem Fehler während der Anfrage.
        """
        global response
        url = "http://{}:{}".format(game_config.IP_ADDRESS, game_config.PORT)

        data = {
            "gameid": gameid,
            "gamerid": gamerid,
            "positions": positions,
            "colors": colors,
            "value": value
        }

        headers = {"Content-Type": "application/json"}

        print("An den Server gesendet:", data)

        try:
            # Senden einer POST-Anfrage an den Server
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response_data = response.json()
            response.raise_for_status()

            if response.status_code == 200:
                # Extrahieren der Antwortdaten
                print("Antwort vom Server:", response_data)
                self.gameid = response_data.get("gameid", gameid)
                self.value = response_data["value"]

        except requests.exceptions.RequestException as e:
            game_config.NO_NETWORK_CONNECTION = True
            game_config.ERROR_MESSAGE = "Es konnte keine Verbindung zum\nServer aufgebaut werden."
            print("Es konnte keine Verbindung zum Server http://" + str(game_config.IP_ADDRESS) + ":" + str(game_config.PORT) + " aufgebaut werden.")
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 400:
                response_data = e.response.json()
                error_message = response_data.get("error")
                if error_message:
                    print("Fehlermeldung vom Server:", error_message)
