import pygame
import pygame_gui

import config.config as config
import config.game_config as game_config


class BoardView:
    def __init__(self, screen, color_cell_handler, button_callback, button_exit_callback, button_restart_callback):
        """
        Initialisiert die BoardView-Klasse.

        Args:
            screen (pygame.Surface): Der Pygame-Bildschirm, auf dem das Spielbrett angezeigt werden soll
            color_cell_handler (function): Die Handler-Funktion zum Einfärben einer Zelle
            button_callback (function): Die Callback-Funktion, die aufgerufen wird, wenn der Button geklickt wird
        """
        self.screen = screen
        self.color_cell_handler = color_cell_handler
        self.button_callback = button_callback
        self.button_exit_callback = button_exit_callback
        # Neuer Restart Button
        self.button_restart_callback = button_restart_callback

        self.dragging = False
        self.dragged_color = None
        self.start_pos = (0, 0)
        self.current_pos = (0, 0)
        # self.used_colors = config.COLORS if game_config.player_is_guesser or not game_config.code_is_coded else config.FEEDBACK_COLORS
        self.used_colors = config.FEEDBACK_COLORS if game_config.CODER_IS_PLAYING and game_config.CODE_IS_CODED else config.COLORS

        # Initialisierung des Spielbretts
        self.board = [[None] * config.COLUMNS for _ in range(config.ROWS)]
        self.board_feedback = [[None] * config.COLUMNS for _ in range(config.ROWS)]

        # GUI-Manager erstellen
        self.gui_manager = pygame_gui.UIManager(screen.get_size())


        self.textfield_rect = pygame.Rect(config.MARGIN, (config.ROWS + 2) * (config.CELL_SIZE + config.GAP_SIZE) + 2 * config.MARGIN, config.WIDTH - 2 * config.MARGIN, config.TEXTFIELD_HEIGHT)

        # Button-Parameter
        self.button_rect = pygame.Rect(len(self.used_colors) * (config.CELL_SIZE + config.GAP_SIZE) + 2 * config.MARGIN,
                                       config.ROWS * (config.CELL_SIZE + config.GAP_SIZE) + 2 * config.MARGIN, config.BUTTON_WIDTH, config.BUTTON_HEIGHT)

        self.button_rect = pygame.Rect(config.COLUMNS * (config.CELL_SIZE + config.GAP_SIZE) +
                                       config.COLUMNS * (config.FEEDBACK_CELL_SIZE + config.GAP_SIZE) +
                                       3 * config.MARGIN,
                                       config.MARGIN,
                                       config.BUTTON_WIDTH, config.BUTTON_HEIGHT)

        self.button_restart_rect = pygame.Rect(config.COLUMNS * (config.CELL_SIZE + config.GAP_SIZE) +
                                               config.COLUMNS * (config.FEEDBACK_CELL_SIZE + config.GAP_SIZE) +
                                               3 * config.MARGIN,
                                               3 * config.MARGIN + 2 * config.BUTTON_HEIGHT,
                                               config.BUTTON_WIDTH, config.BUTTON_HEIGHT)

        self.button_color = (255, 0, 0)
        self.button_text = "Bestätigen"
        self.button_font = pygame.font.Font(None, 24)

        # Button-Parameter
        self.button_exit_rect = pygame.Rect(config.COLUMNS * (config.CELL_SIZE + config.GAP_SIZE) +
                                       config.COLUMNS * (config.FEEDBACK_CELL_SIZE + config.GAP_SIZE) +
                                       3 * config.MARGIN,
                                       2 * config.MARGIN + config.BUTTON_HEIGHT,
                                       config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
        self.button_exit_color = (20, 20, 20)
        self.button_exit_text = "Beenden"
        self.button_exit_font = pygame.font.Font(None, 24)

        self.button_restart_color = (0, 255, 0)
        self.button_restart_text = "Neustart"
        self.button_restart_font = pygame.font.Font(None, 24)

        self.textfield_text = ""

        # Feedback-Kugeln
        self.feedback_balls = [[None] * config.FEEDBACK_COLUMNS for _ in range(config.FEEDBACK_ROWS)]

    def draw(self):
        """
        Zeichnet das Spielbrett auf den Bildschirm.
        """
        # UI-Elemente zeichnen
        self.gui_manager.draw_ui(self.screen)

        self.used_colors = config.FEEDBACK_COLORS if game_config.CODER_IS_PLAYING and game_config.CODE_IS_CODED else config.COLORS

        # # # Rahmen um das Spielfeld zeichnen
        # board_rect = pygame.Rect(
        #     config.MARGIN - 1,
        #     config.MARGIN - 1,
        #     config.COLUMNS * (config.CELL_SIZE + config.GAP_SIZE),
        #     1 * (config.CELL_SIZE + config.GAP_SIZE)
        # )
        # #
        # pygame.draw.rect(self.screen, (255, 0, 0), board_rect)
        #
        # # Rahmen um die Feedback-Kugeln zeichnen
        # feedback_rect = pygame.Rect(
        #     config.COLUMNS * (config.CELL_SIZE + config.GAP_SIZE) + 2 * config.MARGIN,
        #     config.MARGIN + (config.CELL_SIZE + config.GAP_SIZE),
        #     config.COLUMNS * (config.FEEDBACK_CELL_SIZE + config.GAP_SIZE),
        #     (config.ROWS - 1) * (config.CELL_SIZE + config.GAP_SIZE)
        # )
        #
        # pygame.draw.rect(self.screen, (0, 0, 255), feedback_rect, 3)

        # Zeichnen der leeren Zellen des Spielbretts
        for row in range(config.ROWS):
            for column in range(config.COLUMNS):
                cell_x = column * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN
                cell_y = row * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN
                radius = config.CELL_SIZE // 2
                pygame.draw.circle(
                    self.screen,
                    (0,0,0) if row == 0 and game_config.PLAYER_IS_GUESSER else config.CELL_COLOR,
                    (cell_x, cell_y),
                    radius
                )

        # Zeichnen der schwarzen und weißen Pins
        x_start_feedback = config.COLUMNS * (
                config.CELL_SIZE + config.GAP_SIZE) + 2 * config.MARGIN + config.FEEDBACK_CELL_SIZE // 2
        y_start_feedback = config.MARGIN + config.CELL_SIZE // 2
        for row in range(config.ROWS):
            if (row != 0):
                for column in range(config.COLUMNS):
                    cell_x = x_start_feedback + column * (config.FEEDBACK_CELL_SIZE + config.GAP_SIZE)
                    cell_y = y_start_feedback + row * (config.CELL_SIZE + config.GAP_SIZE)
                    radius = config.FEEDBACK_CELL_SIZE // 2
                    pygame.draw.circle(
                        self.screen,
                        config.CELL_COLOR,
                        (cell_x, cell_y),
                        radius
                    )

        # Zeichnen der bereits eingefärbten Zellen
        for row in range(config.ROWS):
            for column in range(config.COLUMNS):
                if self.board_feedback[row][column] is not None:
                    cell_x = x_start_feedback + column * (config.FEEDBACK_CELL_SIZE + config.GAP_SIZE)
                    cell_y = y_start_feedback + row * (config.CELL_SIZE + config.GAP_SIZE)
                    radius = config.FEEDBACK_CELL_SIZE // 2
                    pygame.draw.circle(
                        self.screen,
                        (255, 225, 225) if row == 0 and not game_config.PLAYER_IS_GUESSER else self.board_feedback[row][
                            column],
                        (cell_x, cell_y),
                        radius
                    )

        # Zeichnen der Farbzellen
        for i, color in enumerate(self.used_colors):
            circle_x = i * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN
            circle_y = (config.ROWS) * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN * 2
            circle_radius = config.CELL_SIZE // 2
            if self.dragging and self.dragged_color == color:
                circle_x = self.current_pos[0]
                circle_y = self.current_pos[1]
            pygame.draw.circle(
                self.screen,
                color,
                (circle_x, circle_y),
                circle_radius
            )

        # Zeichnen der bereits eingefärbten Zellen
        for row in range(config.ROWS):
            for column in range(config.COLUMNS):
                if self.board[row][column] is not None:
                    cell_x = column * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN
                    cell_y = row * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN
                    radius = config.CELL_SIZE // 2
                    pygame.draw.circle(
                        self.screen,
                        (0,0,0) if self.check_if_first_row_is_not_visible(row) else self.board[row][column],
                        (cell_x, cell_y),
                        radius
                    )

        # Zeichnen des Bestätigen Buttons
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        button_text_surface = self.button_font.render(self.button_text, True, (255, 255, 255))
        button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text_surface, button_text_rect)

        # Zeichnen des Beenden Buttons
        pygame.draw.rect(self.screen, self.button_exit_color, self.button_exit_rect)
        button_exit_text_surface = self.button_font.render(self.button_exit_text, True, (255, 255, 255))
        button_exit_text_rect = button_exit_text_surface.get_rect(center=self.button_exit_rect.center)
        self.screen.blit(button_exit_text_surface, button_exit_text_rect)

        # Zeichnen des Neustart Buttons
        pygame.draw.rect(self.screen, self.button_restart_color, self.button_restart_rect)
        button_restart_text_surface = self.button_restart_font.render(self.button_restart_text, True, (255, 255, 255))
        button_restart_text_rect = button_restart_text_surface.get_rect(center=self.button_restart_rect.center)
        self.screen.blit(button_restart_text_surface, button_restart_text_rect)

        # Zeichnen des Textfelds
        textfield_color = (255, 255, 255)
        textfield_font = pygame.font.SysFont(None, 40)
        textfield_text_color = (255, 255, 255)
        textfield_border_width = 2
        textfield_padding = 5

        # Zeichnen des Textfelds
        pygame.draw.rect(self.screen, textfield_color, self.textfield_rect, textfield_border_width)
        text_surface = textfield_font.render(self.textfield_text, True, textfield_text_color)
        text_rect = text_surface.get_rect(topleft=(self.textfield_rect.x + textfield_padding,
                                                   self.textfield_rect.y + textfield_padding))
        self.screen.blit(text_surface, text_rect)

    def start_drag(self, start_pos):
        """
        Startet den Drag-Vorgang.

        Args:
            start_pos (tuple): Die Startposition des Drag-Vorgangs
        """
        if not self.dragging:
            self.dragging = True
            self.dragged_color = self.get_clicked_color(start_pos)
            self.start_pos = start_pos
            self.current_pos = start_pos

    def drop(self, drop_pos):
        """
        Behandelt das Ablegen der gezogenen Farbzelle.

        Args:
            drop_pos (tuple): Die Position, an der die Farbzelle abgelegt wurde
        """
        if self.button_rect.collidepoint(drop_pos):
            # Überprüfen, ob der Button geklickt wurde
            self.button_callback(self)
        elif self.button_exit_rect.collidepoint(drop_pos):
            self.button_exit_callback(self)
        elif self.button_restart_rect.collidepoint(drop_pos):  # Geändert: Hinzugefügt
            self.button_restart_callback()  # Geändert: Hinzugefügt
        else:
            # Einfärben der Zelle, wenn sie im Spielbrettbereich liegt
            drop_row, drop_column, isLeftBoard = self.get_clicked_cell(drop_pos)
            if drop_row is not None and drop_column is not None:
                self.color_cell_handler(self, drop_row, drop_column, self.dragged_color, isLeftBoard)
        self.dragging = False

    def update(self):
        """
        Aktualisiert den aktuellen Zustand des Drag-Vorgangs.
        """
        if self.dragging:
            self.current_pos = pygame.mouse.get_pos()

        self.gui_manager.update(pygame.time.get_ticks() / 1000.0)

    def get_clicked_cell(self, mouse_pos):
        """
        Ermittelt die Zelle, die anhand der Mausposition angeklickt wurde.

        Args:
            mouse_pos (tuple): Die aktuelle Mausposition

        Returns:
            tuple: Die Zeilen- und Spaltennummer der angeklickten Zelle sowie ein Wert, ob es sich um das linke Spielbrett handelt oder nicht
        """
        x, y = mouse_pos
        margin = config.MARGIN
        cell_size = config.CELL_SIZE
        gap_size = config.GAP_SIZE
        feedback_cell_size = config.FEEDBACK_CELL_SIZE
        columns = config.COLUMNS
        rows = config.ROWS
        is_left = True

        column = 0  # Standardwert
        row = 0  # Standardwert

        if margin <= x <= margin + columns * (cell_size + gap_size) and margin <= y <= rows * (
                cell_size + gap_size) + margin:
            updated_x_position = x - margin
            updated_y_position = y - margin
            row = updated_y_position // (cell_size + gap_size)
            column = updated_x_position // (cell_size + gap_size)
        elif 2 * margin + columns * (cell_size + gap_size) <= x <= 2 * margin + columns * (
                cell_size + gap_size + feedback_cell_size + config.FEEDBACK_GAP_SIZE) and \
                margin + cell_size + gap_size <= y <= rows * (cell_size + gap_size) + margin:
            is_left = False
            updated_x_position = x - 2 * margin - columns * (cell_size + gap_size)
            updated_y_position = y - margin - cell_size - gap_size
            column = updated_x_position // (feedback_cell_size + gap_size)
            row = updated_y_position // (cell_size + gap_size)

        return row, column, is_left

    def get_clicked_color(self, mouse_pos):
        """
        Ermittelt die Farbe, die anhand der Mausposition angeklickt wurde.

        Args:
            mouse_pos (tuple): Die aktuelle Mausposition

        Returns:
            tuple: Die ausgewählte Farbe
        """
        for i, color in enumerate(self.used_colors):
            circle_x = i * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN
            circle_y = (config.ROWS) * (config.CELL_SIZE + config.GAP_SIZE) + config.CELL_SIZE // 2 + config.MARGIN * 2
            circle_radius = config.CELL_SIZE // 2
            if circle_x - circle_radius <= mouse_pos[0] <= circle_x + circle_radius and circle_y - circle_radius <= \
                    mouse_pos[1] <= circle_y + circle_radius:
                return color
        return None

    def check_if_first_row_is_not_visible(self, row):
        if row != 0: return False
        elif game_config.CODER_IS_PLAYER and game_config.CODER_IS_PLAYING: return False
        elif game_config.GAME_IS_OVER: return False
        else: return True