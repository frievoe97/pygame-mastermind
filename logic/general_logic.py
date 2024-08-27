import numpy as np


def calculate_pins(solution, guess):
    """
    Berechnet die Anzahl der schwarzen und weißen Pins für einen gegebenen Rateversuch im Vergleich zur Lösung.

    Args:
        solution (list): Die Lösung, repräsentiert als Liste von Farben.
        guess (list): Der Rateversuch, repräsentiert als Liste von Farben.

    Returns:
        tuple: Ein Tupel, bestehend aus der Anzahl der schwarzen und weißen Pins.

    """
    # print(solution, guess)
    # Variable zur Zählung der schwarzen Pins initialisieren
    black_pins = 0

    # Variable zur Zählung der weißen Pins initialisieren
    white_pins = 0

    # Erstellen von Kopien der Lösung und des Rateversuchs, um sie zu modifizieren
    solution_copy = np.asarray(solution).tolist()
    guess_copy = np.asarray(guess).tolist()

    # Berechnung der schwarzen Pins
    for i in range(len(guess)):
        # print(i)
        # Wenn die Farbe in der gleichen Position in Lösung und Rateversuch übereinstimmt
        if guess[i] == solution[i]:
            # Inkrementiere die Anzahl der schwarzen Pins
            black_pins += 1

            # Markiere die Übereinstimmungen, um sie bei der Berechnung der weißen Pins zu ignorieren
            solution_copy[i] = -1
            guess_copy[i] = -1

    # Berechnung der weißen Pins
    for i in range(len(guess)):
        # Wenn die Farbe im Rateversuch an einer anderen Position in der Lösung vorkommt
        if guess_copy[i] != -1 and guess_copy[i] in solution_copy:
            # Inkrementiere die Anzahl der weißen Pins
            white_pins += 1

            # Markiere die Übereinstimmungen, um Doppelzählungen zu vermeiden
            solution_copy[solution_copy.index(guess_copy[i])] = -1
            guess_copy[i] = -1

    # Rückgabe der Anzahl der schwarzen und weißen Pins
    return black_pins, white_pins
