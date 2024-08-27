import numpy as np

from config import config


def convert_input_to_color(input_value, is_feedback=False):
    """
    Konvertiert eine Eingabe in eine Farbe.

    Args:
        input_value (int or tuple): Die Eingabe, die in eine Farbe konvertiert werden soll.
        is_feedback (bool, optional): Gibt an, ob es sich um ein Feedback handelt. Standardmäßig False.

    Returns:
        tuple or None: Die konvertierte Farbe als Tuple (R, G, B) oder None, wenn die Eingabe ungültig ist.

    """
    if np.issubdtype(type(input_value), int):
        # Farbzuordnung für Integer-Eingaben erstellen
        color_mapping = dict(zip(config.COLORS_NUMBERS, config.COLORS)) if not is_feedback else dict(
            zip(config.FEEDBACK_COLORS_NUMBERS, config.FEEDBACK_COLORS))
        return color_mapping.get(input_value)
    elif isinstance(input_value, tuple):
        # Farbzuordnung für Tuple-Eingaben erstellen
        color_mapping = dict(zip(config.COLORS, config.COLORS_NUMBERS)) if not is_feedback else dict(
            zip(config.FEEDBACK_COLORS, config.FEEDBACK_COLORS_NUMBERS))
        return color_mapping.get(input_value)
    else:
        # Eingabe ist ungültig, daher wird None zurückgegeben
        return None
