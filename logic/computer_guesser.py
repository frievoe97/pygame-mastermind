import random

from config import config
from config import game_config
from logic.color_mapping import convert_input_to_color
from logic.general_logic import calculate_pins


class ComputerGuesser:
    def __init__(self, code_length):
        self.code_length = code_length
        self.code = self.generate_code()  # Generiere den zu erratenden Code
        self.solutions = []  # Liste der geratenen Lösungen
        self.possibilities = self.get_all_possible_codes()  # Liste aller möglichen Codes
        self.last_guess = None  # Der zuletzt geratene Code

    def generate_code(self):
        """
        Generiert einen zufälligen Code mit der angegebenen Länge
        """
        code = random.choices(config.COLORS_NUMBERS, k=self.code_length)
        return code

    def evaluate_guess(self, code):
        """
        Bewertet den geratenen Code und gibt die Anzahl der schwarzen und weißen Pins zurück
        """
        code_copy = list(code)
        guess_copy = list(self.last_guess)

        black_pins, white_pins = calculate_pins(code_copy, guess_copy)

        return black_pins, white_pins

    def guess(self, board_view):
        """
        Rät einen zufälligen Code aus der Liste der möglichen Codes und speichert ihn als letzten geratenen Code
        """
        print("Anzahl der verbelibenden Möglichkeiten:", len(self.possibilities))
        guess = random.choice(self.possibilities)
        self.solutions.append(guess)
        self.last_guess = guess

        for index, color in enumerate(guess):
            # Board View hinzufügen
            board_view.board[game_config.CURRENT_ROW][index] = convert_input_to_color(color)
            game_config.BOARD_GUESS[game_config.CURRENT_ROW][index] = color
            game_config.BOARD_FINAL[game_config.CURRENT_ROW][index] = color

        return True

    def evaluate_feedback(self, black_pins, white_pins):
        """
        Aktualisiert die Liste der möglichen Codes basierend auf dem erhaltenen Feedback
        """
        self.possibilities = [code for code in self.possibilities if
                              self.evaluate_guess(code) == (black_pins, white_pins)]

    def get_all_possible_codes(self):
        """
        Generiert alle möglichen Codes mit der angegebenen Länge
        """
        possibilities = []

        def generate_codes(colors, code_length, current_code):
            if len(current_code) == code_length:
                possibilities.append(current_code)
            else:
                for color in colors:
                    generate_codes(colors, code_length, current_code + [color])

        generate_codes(config.COLORS_NUMBERS, self.code_length, [])

        return possibilities


# game = ComputerGuesser(code_length=config.COLUMNS)
# attempts_list = []
#
# for i in range(10000):
#     if i % 100 == 0:
#         print(i)
#     guess = None
#     attempts = 0
#
#     solution = game.generate_code()
#     game.possibilities = game.get_all_possible_codes()
#
#     while guess != solution:
#         attempts += 1
#         guess = game.guess_code()
#         black_pins, white_pins = game.evaluate_guess(solution)
#         game.evaluate_feedback(black_pins, white_pins)
#
#     attempts_list.append(attempts)
#
# # Berechnung der schnellsten, langsamsten und durchschnittlichen Anzahl der Versuche
# fastest_attempt = min(attempts_list)
# slowest_attempt = max(attempts_list)
# average_attempt = sum(attempts_list) / len(attempts_list)
#
# # Plotten des Histogramms
# plt.figure(figsize=(10, 10))
# plt.hist(attempts_list, bins=range(min(attempts_list), max(attempts_list) + 2), edgecolor='black')
# plt.xlabel('Anzahl der Versuche')
# plt.ylabel('Häufigkeit')
# plt.title('Verteilung der Versuche')
# plt.grid(True)
#
# # Markierung des Mittelwerts
# mean_value = average_attempt
# plt.axvline(mean_value, color='red', linestyle='dashed', linewidth=2)
# plt.text(mean_value + 0.1, plt.ylim()[1] * 0.97, f'Mittelwert: {mean_value:.2f}', color='black',font = {'size': 15})
#
# plt.tight_layout()
# plt.show()
#
# print("Schnellster Versuch:", fastest_attempt, "Versuche")
# print("Langsamster Versuch:", slowest_attempt, "Versuche")
# print("Durchschnittliche Anzahl der Versuche:", average_attempt, "Versuche")
