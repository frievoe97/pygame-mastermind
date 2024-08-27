# Mastermind

**Mastermind** ist ein klassisches Brettspiel, das mit der Pygame-Bibliothek entwickelt wurde. Das Spiel bietet vier verschiedene Modi und mehrere Konfigurationsoptionen, um das Spielerlebnis zu variieren.

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Installation](#installation)
- [Spielmodi](#spielmodi)
- [Supersuper Mode](#supersuper-mode)
- [Netzwerkmodus](#netzwerkmodus)
- [Build-Skript](#build-skript)
- [Bekannte Probleme](#bekannte-probleme)
- [Kontakt](#kontakt)

## Über das Projekt

Mastermind ist ein strategisches Brettspiel, bei dem ein Spieler (CodeMaker) einen geheimen Code erstellt und der andere Spieler (CodeBreaker) versucht, diesen Code zu erraten. Das Spiel bietet zusätzlich die Möglichkeit, gegen den Computer zu spielen oder Computer gegen Computer antreten zu lassen.

## Installation

1. **Voraussetzungen:**
   - Python 3.11

2. **Klonen Sie das Repository:**

```
git clone https://github.com/frievoe97/pygame-mastermind
cd pygame-mastermind
```

3. **Installieren Sie die benötigten Python-Pakete:**

```
pip install -r requirements.txt
```

## Spielmodi

Das Spiel bietet vier Hauptmodi:

1. **CodeBreaker gegen Computer**
2. **CodeMaker gegen Computer**
3. **Computer gegen Computer**
4. **Mensch gegen Mensch**

## Supersuper Mode

Im Supersuper Mode gibt es 8 anstatt der Standard-6 Farben. Dieser Modus kann in den Spieleinstellungen ausgewählt werden, um eine zusätzliche Herausforderung zu bieten.

## Netzwerkmodus

Das Spiel unterstützt den Netzwerkmodus, bei dem der Computer entweder lokal oder über einen Server gespielt werden kann. Der Netzwerkmodus kann in den Einstellungen (Online Mode) konfiguriert werden. Der HTTP-Server für den Netzwerkmodus kann lokal mit dem folgenden Skript gestartet werden:

```
python network/server.py
```

## Build-Skript

Für MacOS-Nutzer steht ein Build-Skript zur Verfügung, um eine ausführbare Anwendung zu erstellen. Führen Sie das folgende Skript aus, um die Anwendung zu kompilieren:

```
python build_script.py
```

**Hinweis:** Derzeit ist die Anwendung nur für MacOS verfügbar.

## Bekannte Probleme

- Momentan ist die Anwendung nur für MacOS verfügbar.

## Kontakt

Für Fragen oder Anmerkungen wenden Sie sich bitte an den Projektleiter:

- **GitHub:** [frievoe97](https://github.com/frievoe97)
