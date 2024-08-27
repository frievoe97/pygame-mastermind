import config
from config import game_config
from config import config


class PlayerGuesser:
    """
    Klasse, die den Spielerrater repräsentiert.
    """

    def make_move(self):
        """
        Führt einen Rateversuch des Spielers aus.
        """
        # Überprüfen, ob in der aktuellen Reihe alle Farben ausgewählt wurden
        allColorsAreSelected = True

        for element in game_config.BOARD_GUESS[game_config.CURRENT_ROW]:
            if element is None:
                allColorsAreSelected = False

        # Übertragen der abgegebenen Reihe auf das finale Board
        if allColorsAreSelected:
            game_config.BOARD_FINAL[game_config.CURRENT_ROW] = game_config.BOARD_GUESS[game_config.CURRENT_ROW]
            game_config.COMPUTER_IS_PLAYING = True

        return

    def evaluate_feedback(self, black_pins, white_pins):
        """
        Bewertet das Feedback des Spielers.

        Args:
            black_pins (int): Die Anzahl der schwarzen Pins.
            white_pins (int): Die Anzahl der weißen Pins.
        """
        pass

    def guess(self, board_view):
        """
        Führt einen Rateversuch des Spielers aus.

        Args:
            board_view (BoardView): Die Ansicht des Spielbretts.

        Returns:
            bool: Gibt zurück, ob der Rateversuch korrekt ausgeführt wurde.
        """
        row_is_correct = True

        for column in range(config.COLUMNS):
            if game_config.BOARD_GUESS[game_config.CURRENT_ROW][column] is None:
                row_is_correct = False

        if row_is_correct:
            game_config.BOARD_FINAL[game_config.CURRENT_ROW] = game_config.BOARD_GUESS[game_config.CURRENT_ROW]
            game_config.COMPUTER_IS_PLAYING = True

        print("Der Rater hat versucht den Code zu knacken.")
        return row_is_correct
