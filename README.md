
Samurai Quest – Modular Pygame Adventure Game Framework

Samurai Quest is a modular platform adventure game skeleton built with Python and Pygame.
It features a multi-phase enemy system, animated sprite management, dynamic health and stamina bars, a customizable main menu with save/load capability, and a phase-based gameplay loop – all split into maintainable modules and written using object-oriented principles.

---

🚀 Features

- Object-Oriented Modular Design:
  Each gameplay component (game logic, menu, health bar, stamina bar, sprite loading, etc.) is encapsulated in its own file/class.
- Animated Sprites:
  Sprite loader class enables easy loading and animation of character sprites.
- Dynamic Health & Stamina Bars:
  Visual bars update in real time to reflect player state.
- Multi-Phase Game Loop:
  The enemy and challenge system supports multiple progressive waves.
- Interactive Main Menu:
  Start, load, settings, and quit functions are easily accessible.
- Save & Load System:
  Progress can be saved and loaded for full gameplay experience.
- Modern Pygame UI:
  Styled fonts, color themes, and clear layouts.

---

📁 File & Module Structure

SamuraiQuest/
├── game.py              # Main game loop and phase/enemy management
├── menu.py              # Main menu, load, and settings screens
├── health_bar.py        # Player health bar visualization
├── stamina_bar.py       # Player stamina bar visualization
├── sprite_loader.py     # Sprite loading and animation utility
├── [assets/]            # Sprites, images, sounds (not included, use your own)
├── README.md            # Project documentation

Module summaries:
- game.py : Controls game states, phases, and enemy logic.
- menu.py : Draws and manages main menu, save/load, and options.
- health_bar.py : Updates and draws player's health bar.
- stamina_bar.py : Manages and draws the stamina bar.
- sprite_loader.py : Loads, organizes, and animates character/enemy sprites.

---

🛠️ How to Run

1. Requirements:
   - Python 3.8+
   - Pygame (pip install pygame)
   - (Optionally) your own image/sound assets

2. Run the Game:
   python game.py
   The main menu will appear with options for new game, load, settings, and quit.

---

📝 License

This project is open source and free for educational, demo, or personal use.
You may use, modify, and share with attribution.

---

👨‍💻 Author

Developed by Doğukan Avcı
- Email: hulavci121@gmail.com
- GitHub: https://github.com/AvciDogukan
- LinkedIn: https://www.linkedin.com/in/doğukanavcı-119541229/

For feedback or collaboration, feel free to contact!
