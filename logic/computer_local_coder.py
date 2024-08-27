import numpy as np

from config import config
from config import game_config
from logic.general_logic import calculate_pins


class ComputerLocalCoder:
    def __init__(self):
        self.current_guess = np.empty(config.COLUMNS, dtype=object)
        self.solution_temp = game_config.SOLUTION
        self.black_pins = 0
        self.white_pins = 0

    def rate_move(self, board_view, guesser):
        """
        Bewertet den aktuellen Zug des Spielers.
        """
        black_pins, white_pins = calculate_pins(game_config.SOLUTION.copy(), game_config.BOARD_FINAL[game_config.CURRENT_ROW].copy())

        for index in range(black_pins):
            board_view.board_feedback[game_config.CURRENT_ROW][index] = config.FEEDBACK_COLORS[1]

        for index in range(white_pins):
            board_view.board_feedback[game_config.CURRENT_ROW][index + black_pins] = config.FEEDBACK_COLORS[0]

        if black_pins == config.COLUMNS:
            game_config.GAME_IS_OVER = True
            game_config.GUESSER_WON = True

        return black_pins, white_pins

    def count_red_pins(self):
        """
        Zählt die Anzahl der roten Pins (richtige Farbe an richtiger Position).
        """
        red_pins = 0
        for i in range(len(self.current_guess)):
            if self.current_guess[i] == self.solution_temp[i]:
                red_pins += 1
                self.current_guess[i] = None

        return red_pins

    def count_white_pins(self):
        """
        Zählt die Anzahl der weißen Pins (richtige Farbe an falscher Position).
        """
        white_pins = 0
        for i in range(len(self.current_guess)):
            if self.current_guess[i] is not None and np.any(self.current_guess[i] == self.solution_temp):
                index = np.where(self.current_guess[i] == self.solution_temp)[0][0]
                white_pins += 1
                self.solution_temp[index] = -1  # Platzhalterwert, der nicht mit den tatsächlichen Elementen kollidiert

        return white_pins

    def generate_code(self, board_view):
        """
        Generiert einen zufälligen Code als Lösung für das Spiel.
        """
        solution = np.random.choice(config.COLORS_NUMBERS, size=config.COLUMNS)
        game_config.SOLUTION = solution
        game_config.CODE_IS_CODED = True
        print("Geheimcode wurde erstellt:", solution)
        return True
