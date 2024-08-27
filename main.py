import time

import numpy as np
import pygame

from background_manager import BackGroundManager
from config import config, game_config
from constants import GAME, MENU, MENU_NEW, ONLINE_SETTINGS
from gui.board_view import BoardView
from gui.menu_controller import MenuController
from gui.menu_model import MenuModel
from gui.menu_view import MenuView
from gui.menu_view_update import MenuViewUpdate
from gui.mvc_online_settings.controller import \
    Controller as OnlineSettingsController
from gui.mvc_online_settings.model import Model as OnlineSettingsModel
from gui.mvc_online_settings.view import View as OnlineSettingsView
from logic.color_mapping import convert_input_to_color
from logic.computer_guesser import ComputerGuesser
from logic.computer_local_coder import ComputerLocalCoder
from logic.computer_network_coder import ComputerNetworkCoder
from logic.player_coder import PlayerCoder
from logic.player_guesser import PlayerGuesser

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Fenstergröße
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

# Button-Größe
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

# Texteingabe-Größe
TEXT_INPUT_WIDTH = 200
TEXT_INPUT_HEIGHT = 60


class MainApp:
    def __init__(self):
        # Initialisierung von Pygame
        pygame.init()   # pylint: disable=E1101

        # Erstellen des Bildschirms mit den angegebenen Dimensionen
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

        # Festlegen des Fenstertitels
        pygame.display.set_caption("Mastermind")

        # Erstellen eines Clock-Objekts zur Framerate-Steuerung
        self.clock = pygame.time.Clock()
        self.backgroundManager = BackGroundManager()

        self.time = time.time() - 1000

        self.last_player_is_coder = game_config.CODER_IS_PLAYING

        # Property und Setter für den Zustand der Anwendung (Menü oder Spiel)
        @property
        def state(self):
            return self._state

        @state.setter
        def state(self, value):
            if value in [MENU, GAME, ONLINE_SETTINGS, MENU_NEW]:
                print("setting..." + value)
            else:
                raise ValueError("Invalid view state")

        self._state = MENU

        self.online_settings_model = OnlineSettingsModel()
        self.online_settings_view = OnlineSettingsView(
            self.screen, self, self.online_settings_model)
        self.online_settings_controller = OnlineSettingsController(
            self.screen, self, self.online_settings_model)

        # These lines of code are creating instances of the `MenuModel`, `MenuView`, and `MenuController`
        # classes, which are part of the Model-View-Controller (MVC) design pattern.
        # By creating these objects, the code is setting up the MVC architecture for the menu screen.
        self.menu_model = MenuModel(self)
        self.menu_view = MenuView(self.screen, self.menu_model)
        self.menu_controller = MenuController(self.menu_model, self.menu_view)

        self.menu_view_new = MenuViewUpdate(
            self.screen, self.handle_button_start_game_click)

        # Initialisierung der Boardansicht
        self.board_view = BoardView(self.screen, self.color_cell, self.handle_button_click,
                                    self.handle_button_exit_click, self.start_new_game)

        # Initialisierung von Coder und Guesser
        self.coder = None
        self.guesser = None

    def update_roles(self):
        """
        Aktualisiert die Rollen des Coder und Guesser basierend auf den Spielkonfigurationen.
        """
        if game_config.CODER_IS_COMPUTER_LOCAL:
            self.coder = ComputerLocalCoder()
        elif game_config.CODER_IS_COMPUTER_SERVER:
            self.coder = ComputerNetworkCoder(self)
        else:
            self.coder = PlayerCoder()

        if game_config.GUESSER_IS_COMPUTER:
            self.guesser = ComputerGuesser(code_length=config.COLUMNS)
        else:
            self.guesser = PlayerGuesser()

        print("Die Spieler wurden initialisiert.")

    def handle_button_start_game_click(self):
        """
        Diese Methode wird aufgerufen, wenn der "Start Game" Button im Menü geklickt wird.
        Sie überprüft die ausgewählten Optionen und startet das Spiel mit den entsprechenden Konfigurationen.
        """
        selected_buttons = []
        if pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Superhirn")
        if pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Supersuperhirn")

        if pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Spieler Rater")
        if pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Computer Rater")

        if pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Spieler Kodierer")
        if pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Computer Kodierer")
        if pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
            selected_buttons.append("Server")

        if len(selected_buttons) != 3:
            return
        elif 'Server' in selected_buttons and (len(self.menu_view_new.text_input1) < 1 or len(self.menu_view_new.text_input2) < 1):
            return

        if "Superhirn" in selected_buttons:
            config.IS_SUPERSUPERHIRN = False
        else:
            config.IS_SUPERSUPERHIRN = True

        if "Spieler Rater" in selected_buttons:
            game_config.GUESSER_IS_PLAYER = True
            game_config.GUESSER_IS_COMPUTER = False
        else:
            game_config.GUESSER_IS_COMPUTER = True
            game_config.GUESSER_IS_PLAYER = False

        if "Spieler Kodierer" in selected_buttons:
            game_config.CODER_IS_PLAYER = True
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.CODER_IS_COMPUTER_SERVER = False
        elif "Computer Kodierer" in selected_buttons:
            game_config.CODER_IS_PLAYER = False
            game_config.CODER_IS_COMPUTER_LOCAL = True
            game_config.CODER_IS_COMPUTER_SERVER = False
        else:
            game_config.IP_ADDRESS = self.menu_view_new.text_input1
            game_config.PORT = self.menu_view_new.text_input2
            game_config.CODER_IS_PLAYER = False
            game_config.CODER_IS_COMPUTER_LOCAL = False
            game_config.CODER_IS_COMPUTER_SERVER = True

        self.start_new_game()

    def handle_button_exit_click(self, board_view):
        """
        Diese Methode wird aufgerufen, wenn der "Exit" Button im Spiel geklickt wird.
        Sie setzt den Zustand der Anwendung auf das Menü zurück.
        """
        self._state = MENU_NEW
        self.menu_view = MenuView(self.screen)
        self.menu_controller = MenuController(self.screen, self)
        self.menu_view.clearSetting()
        self.board_view = BoardView(self.screen, self.color_cell, self.handle_button_click,
                                    self.handle_button_exit_click, self.start_new_game)
        self.coder = None
        self.guesser = None

    def start_new_game(self):
        game_config.GAME_IS_OVER = False
        game_config.BOARD_GUESS = np.empty(
            (config.ROWS, config.COLUMNS), dtype=object)
        game_config.BOARD_FINAL = np.empty(
            (config.ROWS, config.COLUMNS), dtype=object)
        game_config.FEEDBACK_BOARD_FINAL = np.empty(
            ((config.ROWS - 1), config.COLUMNS), dtype=object)
        game_config.SOLUTION = np.empty(config.COLUMNS, dtype=object)
        game_config.CODE_IS_CODED = False
        game_config.CURRENT_ROW = config.ROWS - 1
        game_config.ERROR_MESSAGE = ""
        game_config.NO_NETWORK_CONNECTION = False

        # Farben für die Zellen im Spielbrett
        config.COLORS = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 128, 0), (153, 76, 0), (255, 255, 255), (0, 0, 0)] if config.IS_SUPERSUPERHIRN else [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 128, 0), (153, 76, 0)]

        # Farbennummern für die Zellen im Spielbrett
        config.COLORS_NUMBERS = [
            1, 2, 3, 4, 5, 6, 7, 8] if config.IS_SUPERSUPERHIRN else [1, 2, 3, 4, 5, 6]

        config.FEEDBACK_COLUMNS = 5 if config.IS_SUPERSUPERHIRN else 4
        config.COLUMNS = 5 if config.IS_SUPERSUPERHIRN else 4

        # Erstellen des Rate-Boards, auf dem der Spieler seinen Rateversuch macht
        game_config.BOARD_GUESS = np.empty(
            (config.ROWS, config.COLUMNS), dtype=object)

        # Erstellen des Boards, das alle logisch sinnvollen Eingaben enthält
        game_config.BOARD_FINAL = np.empty(
            (config.ROWS, config.COLUMNS), dtype=object)

        # Erstellen des Boards, das die Bewertungen des Raters enthält
        game_config.FEEDBACK_BOARD_FINAL = np.empty(
            ((config.ROWS - 1), config.COLUMNS), dtype=object)

        self.board_view = BoardView(self.screen, self.color_cell, self.handle_button_click,
                                    self.handle_button_exit_click, self.start_new_game)
        self.update_roles()

        self._state = GAME

        game_config.CODER_IS_PLAYING = True

        print()
        print("############################################")
        print("#                                          #")
        print("#    Es wurde ein neues Spiel gestartet.   #")
        print("#                                          #")
        print("############################################")
        print()

    def handle_button_exit_click(self, board_view):
        self._state = MENU
        # self.menu_view = MenuView(self.screen)
        # self.menu_controller = MenuController(self.screen, self)
        # """
        #         """
        #         Diese Methode wird aufgerufen, wenn der "Exit" Button im Spiel geklickt wird.
        #         Sie setzt den Zustand der Anwendung auf das Menü zurück.
        #         """
        #         self._state = MENU_NEW
        #         self.menu_view = MenuView(self.screen)
        #         self.menu_controller = MenuController(self.screen, self)
        # """

        self.board_view = BoardView(self.screen, self.color_cell, self.handle_button_click,
                                    self.handle_button_exit_click, self.start_new_game)
        self.coder = None
        self.guesser = None

    def set_state(self, value):
        """
        This function sets the value of the "_state" attribute to the input "value".

        :param value: The value parameter is the new value that we want to set for the state attribute of an
        object. The method set_state() takes this value as an argument and assigns it to the private
        attribute _state of the object
        """
        self._state = value

    def handle_button_click(self, board_view):
        """
        Diese Methode wird aufgerufen, wenn der Button im Spiel geklickt wird.
        Sie überprüft, ob alle Farben in der aktuellen Reihe ausgewählt wurden.
        Wenn ja, wird die entsprechende Aktion ausgeführt.
        """
        if game_config.GUESSER_IS_PLAYER or game_config.CODER_IS_PLAYER:
            if game_config.CODER_IS_PLAYING:
                if not game_config.CODE_IS_CODED:
                    if self.coder.generate_code(self.board_view):
                        game_config.CODER_IS_PLAYING = False
                else:
                    black_pins, white_pins, rate_was_correct = self.coder.rate_move(
                        self.board_view, self.guesser)
                    game_config.RATE_WAS_CORRECT = rate_was_correct
                    if game_config.RATE_WAS_CORRECT:
                        game_config.CODER_IS_PLAYING = False
            else:
                if self.guesser.guess(self.board_view):
                    game_config.CODER_IS_PLAYING = True

    def color_cell(self, board_view, row, column, color, isLeftBoard):
        """
        Diese Methode färbt eine Zelle in Abhängigkeit von ihrer Zeilennummer ein.
        Wenn die Zeilennummer mit der aktuellen Reihe übereinstimmt und der Spieler der Rater ist,
        wird die Zelle eingefärbt und die entsprechende Farbe im Rate-Board gespeichert.
        :param board_view: Das BoardView-Objekt, auf dem die Zelle eingefärbt werden soll
        :param row: Die Zeilennummer der Zelle
        :param column: Die Spaltennummer der Zelle
        :param color: Die Farbe, mit der die Zelle eingefärbt werden soll
        """
        if game_config.CODER_IS_PLAYER or game_config.GUESSER_IS_PLAYER:
            if game_config.CODER_IS_PLAYING:

                if not game_config.CODE_IS_CODED and isLeftBoard and row == 0:
                    game_config.BOARD_GUESS[row,
                                            column] = convert_input_to_color(color)
                    board_view.board[row][column] = color
                elif not isLeftBoard and row == (game_config.CURRENT_ROW - 1):
                    game_config.FEEDBACK_BOARD_FINAL[row, column] = convert_input_to_color(
                        color, True)
                    board_view.board_feedback[row + 1][column] = color

            else:
                if row == game_config.CURRENT_ROW and isLeftBoard:
                    game_config.BOARD_GUESS[row,
                                            column] = convert_input_to_color(color)
                    board_view.board[row][column] = color

    def run(self):
        # Den Bildschirm mit einer Hintergrundfarbe füllen
        self.screen.fill((32, 33, 36))

        """
        Startet die Hauptschleife der Anwendung.
        """
        while True:

            if self._state == MENU:
                # Menüzustand
                for event in pygame.event.get():
                    self.menu_controller.handle_event(event)

                if (len(pygame.event.get()) < 1):
                    self.menu_view.draw(self.menu_controller.selected_index)

            elif self._state == ONLINE_SETTINGS:
                for event in pygame.event.get():
                    self.online_settings_controller.handle_event(event)
                    self.online_settings_view.draw()

                if (len(pygame.event.get()) < 1):
                    self.online_settings_view.draw()

            elif self._state == MENU_NEW:

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(250, 50, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(50, 50, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(250, 150, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(50, 150, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            if pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                self.menu_view_new.marked_buttons.remove(
                                    pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                            else:
                                self.menu_view_new.marked_buttons.append(
                                    pygame.Rect(450, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(50, 250, BUTTON_WIDTH, BUTTON_HEIGHT))
                                if pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT) in self.menu_view_new.marked_buttons:
                                    self.menu_view_new.marked_buttons.remove(
                                        pygame.Rect(250, 250, BUTTON_WIDTH, BUTTON_HEIGHT))

                        elif self.menu_view_new.check_button_collision(mouse_pos, pygame.Rect(config.MARGIN, 450, BUTTON_WIDTH, BUTTON_HEIGHT)):
                            self.handle_button_start_game_click()

                    elif event.type == pygame.KEYDOWN:
                        if self.menu_view_new.server_button_selected:
                            if pygame.Rect(config.MARGIN, 350, TEXT_INPUT_WIDTH, TEXT_INPUT_HEIGHT).collidepoint(
                                    pygame.mouse.get_pos()):
                                if event.key == pygame.K_BACKSPACE:
                                    if len(self.menu_view_new.text_input1) > 0:
                                        self.menu_view_new.text_input1 = self.menu_view_new.text_input1[
                                            :-1]
                                elif event.key == pygame.K_RETURN:
                                    pass
                                else:
                                    self.menu_view_new.text_input1 += event.unicode
                            elif pygame.Rect(2 * config.MARGIN + TEXT_INPUT_WIDTH, 350, TEXT_INPUT_WIDTH, TEXT_INPUT_HEIGHT).collidepoint(
                                    pygame.mouse.get_pos()):
                                if event.key == pygame.K_BACKSPACE:
                                    if len(self.menu_view_new.text_input2) > 0:
                                        self.menu_view_new.text_input2 = self.menu_view_new.text_input2[
                                            :-1]
                                elif event.key == pygame.K_RETURN:
                                    pass
                                else:
                                    self.menu_view_new.text_input2 += event.unicode

                self.menu_view_new.draw()
            elif self._state == GAME:
                # Spielzustand
                # print( game_config.coder_is_playing, self.last_player_is_coder)

                # print(config.IS_SUPERSUPERHIRN)
                # if game_config.coder_is_playing != self.last_player_is_coder:
                #     if game_config.coder_is_playing: print("Der Kodierer ist an der Reihe.")
                #     else: print("Der Rater ist an der Reihe.")
                #     self.last_player_is_coder = game_config.coder_is_player

                while self.coder is None:
                    self.update_roles()

                if game_config.NO_NETWORK_CONNECTION:
                    self.board_view.textfield_text = game_config.ERROR_MESSAGE

                elif game_config.CURRENT_ROW == 0 or game_config.GAME_IS_OVER:
                    game_config.CODER_IS_PLAYING = True
                    if game_config.GUESSER_WON:
                        self.board_view.textfield_text = "Der Rater hat in " + \
                                                         str(config.ROWS - game_config.CURRENT_ROW) + \
                            " Spielzügengewonnen!"
                    else:
                        self.board_view.textfield_text = "Der Kodierer hat gewonnen!"

                else:
                    if not game_config.CODE_IS_CODED:
                        # falls der code vom spieler generiert wird, wird self.coder.generate_code in handle_button_click aufgerufen
                        if not game_config.CODER_IS_PLAYER:
                            if game_config.CODER_IS_COMPUTER_LOCAL:
                                self.board_view.textfield_text = "Der Computer denkt sich einen Code aus."
                            if game_config.CODER_IS_COMPUTER_SERVER:
                                self.board_view.textfield_text = "Der Server denkt sich einen Code aus."
                            self.coder.generate_code(self.board_view)

                            if game_config.CODER_IS_COMPUTER_LOCAL:
                                for index in range(len(game_config.SOLUTION)):
                                    game_config.BOARD_FINAL[0][index] = game_config.SOLUTION[index]
                                    game_config.BOARD_GUESS[0][index] = game_config.SOLUTION[index]
                                    self.board_view.board[0][index] = convert_input_to_color(
                                        game_config.SOLUTION[index])

                            game_config.CODER_IS_PLAYING = False
                        else:
                            self.board_view.textfield_text = "Lege den geheimen Code in der ersten\nReihe fest."

                    # Jetzt muss geraten werden
                    elif not game_config.CODER_IS_PLAYING:
                        if not game_config.GUESSER_IS_PLAYER:
                            if game_config.CODER_IS_COMPUTER_LOCAL:
                                self.board_view.textfield_text = "Der Computer versucht den Code\nzu knacken."
                            if game_config.CODER_IS_COMPUTER_SERVER:
                                self.board_view.textfield_text = "Der Server versucht den Code\nzu knacken."
                            self.guesser.guess(self.board_view)
                            game_config.CODER_IS_PLAYING = True
                        else:
                            self.board_view.textfield_text = "Versuche den Code zu knacken!"

                    else:
                        # Coder ist dran. muss also den Zug bewerten
                        if not game_config.CODER_IS_PLAYER:
                            if game_config.CODER_IS_COMPUTER_LOCAL:
                                self.board_view.textfield_text = "Der Computer bewerten deinen Zug."
                            if game_config.CODER_IS_COMPUTER_SERVER:
                                self.board_view.textfield_text = "Der Server bewerten deinen Zug."

                            black_pins, white_pins = self.coder.rate_move(
                                self.board_view, self.guesser)
                            self.guesser.evaluate_feedback(
                                black_pins, white_pins)

                            if black_pins == config.COLUMNS:
                                game_config.GAME_IS_OVER = True
                                game_config.GUESSER_WON = True

                                for index, color in enumerate(game_config.SOLUTION):
                                    self.board_view.board[0][index] = convert_input_to_color(
                                        color)

                            else:
                                game_config.CURRENT_ROW -= 1

                            if game_config.CURRENT_ROW == 0 and black_pins != config.COLUMNS:
                                game_config.GAME_IS_OVER = True
                                game_config.GUESSER_WON = False

                            if game_config.GAME_IS_OVER and not game_config.GUESSER_WON:
                                print(
                                    "Das Spiel ist vorbei. Der Kodierer hat gewonnen.")
                            elif game_config.GAME_IS_OVER and game_config.GUESSER_WON:
                                print(
                                    "Das Spiel ist vorbei. Der Rater hat gewonnen.")

                            game_config.CODER_IS_PLAYING = False

                        else:
                            if not game_config.RATE_WAS_CORRECT:
                                self.board_view.textfield_text = "Falsche Bewertung."
                            else:
                                self.board_view.textfield_text = "Bitte bewerte den Zug."

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # pylint: disable=E1101
                        pygame.quit()  # pylint: disable=E1101
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=E1101
                        mouse_pos = pygame.mouse.get_pos()
                        # Linksklick
                        if event.button == 1:
                            # Wenn eine Maustaste gedrückt wird, starte das Drag-Event mit der aktuellen Mausposition
                            self.board_view.start_drag(mouse_pos)
                        elif event.button == 3:
                            # Wenn der Spieler bewertet, kann er Eingaben durch Rechtsklick wieder entfernen
                            if not game_config.PLAYER_IS_GUESSER and not game_config.GAME_IS_OVER and not game_config.COMPUTER_IS_PLAYING:
                                row, column, is_left = self.board_view.get_clicked_cell(
                                    mouse_pos)
                                if not is_left:
                                    game_config.FEEDBACK_BOARD_FINAL[row][column] = None
                                    self.board_view.board_feedback[row +
                                                                   1] = game_config.FEEDBACK_BOARD_FINAL[row]

                    elif event.type == pygame.MOUSEBUTTONUP:
                        # Wenn eine Maustaste losgelassen wird, führe das Drop-Event mit der aktuellen Mausposition aus
                        mouse_pos = pygame.mouse.get_pos()
                        self.board_view.drop(mouse_pos)

                # Bildschirm mit einer Hintergrundfarbe füllen
                self.screen.fill((80, 80, 80))

                # Aktualisieren und Zeichnen des Spielbretts
                self.board_view.update()
                self.board_view.draw()

            # self.film_grain.update()
            # self.film_grain.draw()
            # Bildschirm aktualisieren
            pygame.display.flip()

            # Begrenzung der Framerate
            self.clock.tick(config.FPS)


if __name__ == '__main__':
    # Erstellen einer Instanz der MainApp-Klasse und Starten der Anwendung
    app = MainApp()
    app.run()
