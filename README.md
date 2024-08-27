# Mastermind

<img width="322" alt="mastermind_2" src="https://github.com/user-attachments/assets/58020ca3-d09e-48c0-95a2-8a5db7226d73">
<img width="322" alt="mastermind_1" src="https://github.com/user-attachments/assets/be01c40f-9db8-48ff-9e9a-a4d488a979ef">

**Mastermind** is a classic board game developed using the Pygame library. The game features four different modes and several configuration options to vary the gameplay experience.

## Table of Contents

- [About the Project](#about-the-project)
- [Installation](#installation)
- [Game Modes](#game-modes)
- [Supersuper Mode](#supersuper-mode)
- [Network Mode](#network-mode)
- [Build Script](#build-script)
- [Known Issues](#known-issues)
- [Contact](#contact)

## About the Project

Mastermind is a strategic board game where one player (CodeMaker) creates a secret code and the other player (CodeBreaker) tries to guess that code. The game also allows playing against the computer or having computer vs. computer matches.

## Installation

1. **Prerequisites:**
   - Python 3.11

2. **Clone the Repository:**

```
git clone https://github.com/frievoe97/pygame-mastermind
cd pygame-mastermind
```

3. **Install the Required Python Packages:**

```
pip install -r requirements.txt
```

4. **Start the Program:**

```
python ./main.py
```

## Game Modes

The game offers four main modes:

1. **CodeBreaker vs. Computer**
2. **CodeMaker vs. Computer**
3. **Computer vs. Computer**
4. **Human vs. Human**

## Supersuper Mode

In Supersuper Mode, there are 8 colors instead of the standard 6. This mode can be selected in the game settings for an additional challenge.

## Network Mode

The game supports network mode, where the computer can be played either locally or over a server. The network mode can be configured in the settings (Online Mode). The HTTP server for the network mode can be started locally using the following script:

```
python network/server.py
```

## Build Script

For MacOS users, a build script is available to create an executable application. Run the following script to compile the application:

```
python build_script.py
```

**Note:** Currently, the application is only available for MacOS.

## Known Issues

- The application is currently only available for MacOS.

## Contact

For questions or comments, please reach out to the project maintainer:

- **GitHub:** [frievoe97](https://github.com/frievoe97)
