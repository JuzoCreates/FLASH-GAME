# ⚡ FLASH GAME ⚡

Welcome to **FLASH GAME** — a fast-paced arcade built with **Python** and **Pygame**.  
Originally based on [JuzoCreates/FLASH-GAME](https://github.com/JuzoCreates/FLASH-GAME), this version includes multiple fixes, optimizations, and structural improvements for better stability across all systems.

---

## 🚀 What's New

- 🔧 Fixed path and case-sensitivity issues (especially on Linux)
- 🧩 Reorganized project structure for cleaner modularity
- ⚙️ Improved startup sequence and error handling
- 🕹️ Enhanced controls and UI responsiveness
- 🖼️ Fixed several visual bugs (textures, buttons, scaling)
- 💾 Optimized resource loading and memory cleanup on exit
- 🌍 Cross-platform support — Windows, macOS, and Linux

---

## 🧠 Game Overview

**FLASH GAME** is a reflex-based arcade where precision and timing decide your score.  
Control your character, dodge obstacles, and aim for the highest possible points.  
Built entirely in **Pygame**, it’s designed to be simple yet addictive.

---

## 🎮 Controls

| Action | Key |
|--------|-----|
| Move   | Arrow Keys / WASD |
| Pause  | `Esc` |
| Confirm / Select | `Enter` / `Space` |
| Exit Game | `Q` or close window |

---

## 🧰 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/JuzoCreates/FLASH-GAME.git
   cd FLASH-GAME
   ````

2. **(Optional) Create a virtual environment**

   ```bash
   python3 -m venv env
   source env/bin/activate     # macOS / Linux
   env\Scripts\activate        # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   If you don’t have a `requirements.txt`, install manually:

   ```bash
   pip install pygame
   ```

4. **Run the game**

   ```bash
   python FLASH_main.py
   ```

---

## 🗂️ Project Structure

```
FLASH-GAME/
├── FLASH_main.py           # Main entry point
├── modules/                # Game logic and helper modules
│   ├── player.py
│   ├── level.py
│   └── utils.py
├── assets/                 # Game assets
│   ├── images/
│   └── sounds/
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 🪲 Known Issues

* Minor lag may occur on certain systems during the first level load
* Fullscreen toggle not yet implemented
* Some sound effects might clip at high volume

---

## 🔮 Future Plans

* Add settings menu (sound, controls, resolution)
* Implement multiple difficulty levels
* Add player progress saving
* Improve visuals and animations
* Multi-language support (EN, RU, AZ)

---

## 📝 License

This project is distributed under the **MIT License**.
See the `LICENSE` file for details.

---

## 🙌 Credits

* Original project by [@JuzoCreates](https://github.com/JuzoCreates)
* Updated and maintained by myself
* Built using [Pygame](https://www.pygame.org/)
* Thanks to everyone who tested and contributed feedback ❤️

---

**FLASH GAME — Fast. Simple. Addictive.**
