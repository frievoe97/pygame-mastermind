import numpy as np

from config import config

# Variable, die angibt, ob der Spieler der Rater ist
PLAYER_IS_GUESSER = None

# Aktuelle Reihe, auf der der Rater seinen Rateversuch macht (unterste Reihe bei 10 Reihen)
CURRENT_ROW = config.ROWS - 1

# Variable, die angibt, ob der Computer am Zug ist
COMPUTER_IS_PLAYING = False

# Variable, die angibt, ob der Computer über ein Netzwerk kommuniziert
COMPUTER_IS_NETWORK = False

# Variablen, um die verschiedenen Rollen festzulegen
GUESSER_IS_PLAYER = True
GUESSER_IS_COMPUTER = False
CODER_IS_PLAYER = False
CODER_IS_COMPUTER_LOCAL = True
CODER_IS_COMPUTER_SERVER = False
CODER_IS_PLAYING = True
RATE_WAS_CORRECT = True
NO_NETWORK_CONNECTION = False
ERROR_MESSAGE = ""

# IP-Adresse und Port für den Server
IP_ADDRESS = "127.0.0.1"
PORT = 8005
GAMER_ID = "Gruppe22"
# IP_ADDRESS = "141.45.39.112"
# PORT = 5001

# Variable, die angibt, ob der Geheimcode bereits festgelegt wurde
CODE_IS_CODED = False

# Array, das den Geheimcode enthält
SOLUTION = np.empty(config.COLUMNS, dtype=object)

# Variable, die angibt, ob das Spiel vorbei ist
GAME_IS_OVER = False

# Variable, die angibt, ob der Spieler gewonnen hat
PLAYER_WON = False # muss raus

# Variable, die angibt, ob der Rater gewonnen hat
GUESSER_WON = False

# Erstellen des Rate-Boards, auf dem der Spieler seinen Rateversuch macht
BOARD_GUESS = np.empty((config.ROWS, config.COLUMNS), dtype=object)

# Erstellen des Boards, das alle logisch sinnvollen Eingaben enthält
BOARD_FINAL = np.empty((config.ROWS, config.COLUMNS), dtype=object)

# Erstellen des Boards, das die Bewertungen des Raters enthält
FEEDBACK_BOARD_FINAL = np.empty(((config.ROWS - 1), config.COLUMNS), dtype=object)
