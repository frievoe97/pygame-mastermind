# Konfigurationen für das Spiel

# Variable, die angibt, ob der Spielmodi Superhirn aktiv ist
IS_SUPERSUPERHIRN = False

# Anzahl der Reihen (eine zusätzliche Reihe für die Farben)
ROWS = 11
# ROWS = 3  # Beispiel: Anzahl der Reihen auf 3 reduziert

# Anzahl der Spalten
COLUMNS = 5 if IS_SUPERSUPERHIRN else 4

# Größe einer Zelle im Spielbrett
CELL_SIZE = 40

# Abstand zwischen den Zellen
GAP_SIZE = 5

# Farbe einer Zelle
CELL_COLOR = (128, 128, 128)

# Farbe des Spielbrett-Rahmens
BORDER_COLOR = (0, 0, 0)

# Breite des Spielbrett-Rahmens
BORDER_WIDTH = 2

# Anzahl der Spalten im Feedback-Board
FEEDBACK_COLUMNS = 5 if IS_SUPERSUPERHIRN else 4

# Anzahl der Reihen im Feedback-Board
FEEDBACK_ROWS = ROWS - 1

# Größe einer Zelle im Feedback-Board
FEEDBACK_CELL_SIZE = 30

# Abstand zwischen den Zellen im Feedback-Board
FEEDBACK_GAP_SIZE = GAP_SIZE

# Farben für die Zellen im Spielbrett
COLORS = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 128, 0), (153, 76, 0), (255, 255, 255), (0, 0, 0)] if IS_SUPERSUPERHIRN else [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 128, 0), (153, 76, 0)]

# Farbennummern für die Zellen im Spielbrett
COLORS_NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8] if IS_SUPERSUPERHIRN else [1, 2, 3, 4, 5, 6]

# Farben für die Zellen im Feedback-Board
FEEDBACK_COLORS = [(255, 255, 255), (0, 0, 0)]

# Farbennummern für die Zellen im Feedback-Board
FEEDBACK_COLORS_NUMBERS = [7, 8]

# Framerate des Spiels
FPS = 60

# Randabstand des Spielbretts vom Bildschirmrand
MARGIN = 30

# Höhe des Textfelds
TEXTFIELD_HEIGHT = 100

# Breite des Buttons
BUTTON_WIDTH = 100

# Höhe des Buttons
BUTTON_HEIGHT = 30

# Berechnung der Breite des Fensters basierend auf der Anzahl der Spalten und der Zellengröße
WIDTH = (
        (COLUMNS + 1) * (CELL_SIZE + FEEDBACK_CELL_SIZE)
    + (COLUMNS) * (FEEDBACK_GAP_SIZE + GAP_SIZE)
    + 4 * MARGIN + BUTTON_WIDTH
) if (
    (COLUMNS + 1) * (CELL_SIZE + FEEDBACK_CELL_SIZE)
    + (COLUMNS) * (FEEDBACK_GAP_SIZE + GAP_SIZE)
    + 4 * MARGIN + BUTTON_WIDTH
) > (
    3 * MARGIN + len(COLORS) * (CELL_SIZE + GAP_SIZE) + 100
) else (
    3 * MARGIN + len(COLORS) * (CELL_SIZE + GAP_SIZE) + 100
)

# Berechnung der Höhe des Fensters basierend auf der Anzahl der Reihen und der Zellengröße
HEIGHT = (
    (ROWS + 1) * (CELL_SIZE + GAP_SIZE)
    + 5 * MARGIN
    + TEXTFIELD_HEIGHT
) if (
    (ROWS + 1) * (CELL_SIZE + GAP_SIZE)
    + 5 * MARGIN
    + TEXTFIELD_HEIGHT
) > 500 else 500
