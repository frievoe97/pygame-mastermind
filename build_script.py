import subprocess
import os
import shutil

# Definiere den Pfad zum Icon
icon_path = "icon.icns"

# Schritt 1: PyInstaller ausführen, um eine `.spec`-Datei zu generieren
subprocess.run([
    "pyinstaller",
    "--name", "Mastermind",
    "--windowed",
    "--onedir",
    "--noconfirm",  # Automatische Bestätigung ohne Nachfragen
    "--add-data", "retro.png:.",
    "--add-data", "PressStart2P-Regular.ttf:.",
    "--add-data", "config:config",
    "--add-data", "gui:gui",
    "--add-data", "logic:logic",
    "--add-data", "network:network",
    "--hidden-import=pkg_resources",
    "--hidden-import=pkg_resources.py2_warn",
    "--hidden-import=background_manager",
    "--hidden-import=config.config",
    "--hidden-import=config.game_config",
    "--hidden-import=gui.board_view",
    "--hidden-import=gui.menu_controller",
    "--hidden-import=gui.menu_model",
    "--hidden-import=gui.menu_view",
    "--hidden-import=gui.menu_view_update",
    "--hidden-import=gui.mvc_online_settings.controller",
    "--hidden-import=gui.mvc_online_settings.model",
    "--hidden-import=gui.mvc_online_settings.view",
    "--hidden-import=logic.color_mapping",
    "--hidden-import=logic.computer_guesser",
    "--hidden-import=logic.computer_local_coder",
    "--hidden-import=logic.computer_network_coder",
    "--hidden-import=logic.player_coder",
    "--hidden-import=logic.player_guesser",
    "--hidden-import=pygame_gui",
    "--hidden-import=pygame",
    "--icon", icon_path,  # Pfad zum Icon hinzufügen
    "--specpath", ".",
    "main.py"
])

# Schritt 2: `.spec`-Datei anpassen
spec_file_name = "Mastermind.spec"
with open(spec_file_name, "r") as file:
    lines = file.readlines()

# Füge pathex=['.'] hinzu, falls noch nicht vorhanden oder passe es an
for i, line in enumerate(lines):
    if 'pathex=' in line:
        lines[i] = "    pathex=['.'],\n"

# Ersetze vorhandene Optionen für argv_emulation und runtime_tmpdir
for i, line in enumerate(lines):
    if 'argv_emulation=' in line:
        lines[i] = "    argv_emulation=True,\n"
    elif 'runtime_tmpdir=' in line:
        lines[i] = "    runtime_tmpdir=None,\n"

# Speichere die Änderungen in der spec-Datei
with open(spec_file_name, "w") as file:
    file.writelines(lines)

print("Spec-Datei angepasst.")

# Schritt 3: Angepasste `.spec`-Datei verwenden, um die Anwendung zu bauen
# Füge `--noconfirm` hinzu, um die Bestätigungsaufforderungen zu umgehen
subprocess.run(["pyinstaller", "--noconfirm", spec_file_name])

# Schritt 4: Lösche den zusätzlichen Ordner im `dist`-Verzeichnis
dist_folder = os.path.join("dist", "Mastermind")
if os.path.exists(dist_folder):
    shutil.rmtree(dist_folder)
    print(f"Ordner '{dist_folder}' wurde gelöscht.")
else:
    print(f"Ordner '{dist_folder}' nicht gefunden.")
