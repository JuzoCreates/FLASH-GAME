# ⚡ FLASH

FLASH is a Python horror game built with the **Pygame** library.

---

## 🎮 Features

### 🧭 First-Person Perspective
- Unique **first-person view**
- Powered by a **custom raycasting engine** that transforms a 2D map into a pseudo-3D perspective
- Creates an immersive atmosphere for the player

### 🗺️ Random Map Generation
- Algorithm dynamically changes **map exits** and **available pickups**
- Ensures that every playthrough feels unique

### 📊 Recorded Stats
- Each run is saved into **FLASH_Scores.txt**
- Tracks:
  - Completion time
  - Date of playthrough
  - Selected difficulty
- Perfect for competing with friends or yourself

### 👾 Enemy AI & Custom Difficulty
- The main enemy follows **multiple strategies** to stop the player
- Player actions include:
  - Hiding from noises
  - Using the flashlight to repel shadow hallucinations
  - Identifying specific sounds (e.g., battery drain does **not** require hiding)
- Enemy has several win conditions, while the player has only one
- **Difficulty is adjustable**

### ⚙️ Custom Settings
- **Difficulty** (Easy / Normal / Hard)
- **Controls**: keyboard or mouse for camera movement
- **Graphics**: low, medium, high
- **Fullscreen** option (recommended)

---

## ⛔ Limitations
- The camera cannot be moved **up or down** (due to the raycasting engine)
- Transparent objects may appear with a **dark rectangle border**

---

## 🐞 Known Issues
1. Pressing **Ctrl+C** during gameplay may cause a crash
2. Choosing a **graphics level too high** for your hardware can result in a **memory error**

---

## 💻 Installation & Running

### 1. Install Python
- **Recommended version:** 3.8 or higher
- Download from [python.org](https://www.python.org/downloads/)

### 2. Install Pygame
Run in command line/terminal:
```bash
pip install pygame
```

### 3. Verify Installation
Test Pygame installation:
```bash
python -m pygame.examples.aliens
```
Or in Python shell:
```python
import pygame
print(pygame.version.ver)
```

### 4. Clone and Setup
```bash
git clone <your-repository-url>
cd Final-Project
```

### 5. Run the Game
```bash
python FLASH_main.py
```
Or click "Run" button in your IDE if you're using one.

### 6. Enjoy!
The game should start automatically. If you encounter any issues, make sure you're in the correct directory and all dependencies are installed.

---

## 📂 Project Structure

### 🔑 Core Files
- `FLASH_main.py` — main entry point
- `FLASH_characters.py`
- `FLASH_inanimates.py`
- `FLASH_menu.py`
- `FLASH_primarySettings.py`
- `FLASH_rendering.py`
- `FLASH_Scores.txt` — saved stats

### 🎨 Assets

#### 🌍 FLASH_Environment
- `FLASH_Escape.png`
- `FLASH_Pause.png`
- `FLASH_RenderedElements/`: `FLASH_Background.png`, `FLASH_Door.png`, `FLASH_Fog.png`, `FLASH_MaxWallDistance.jpg`, `FLASH_Wall.png`
- `FLASH_UI/`: `FLASH_Battery0.png`, `FLASH_BatteryFull.png`, `FLASH_BatteryLow.png`, `FLASH_BatteryMed.png`, `FLASH_Key.png`

#### 🔦 FLASH_InteractiveAssets
- `FLASH_Flashlight/`: `FLASH_FlashlightHalfway.png`, `FLASH_FlashlightOff.png`, `FLASH_FlashlightOn.png`
- `FLASH_Monster/`: `FLASH_Hallucination.png`, `FLASH_ShadowMonster.png`
- `FLASH_Pickups/`: `FLASH_Battery.png`, `FLASH_Key.png` (⚠️ different from UI version)

#### 😱 FLASH_JumpScare
- `FLASH_01.png` … `FLASH_26.png`

#### 🖥️ FLASH_MenuAssets
- `FLASH_Icon.png`, `FLASH_Over.png`, `FLASH_Win.png`
- `Backgrounds/`: `FLASH_CreditsScreen.png`, `FLASH_HowToPlayControls.png`, `FLASH_HowToPlayScreen.png`, `FLASH_MenuBackground.png`, `FLASH_SettingsMenu.png`
- `Buttons/`: (Easy, Medium, Hard, Exit, Options, Start, etc. — each with Highlighted versions)
- `Logos/`: `FLASH_Logo.png`, `FLASH_Title.png`

#### 🎵 FLASH_Music
- `FLASH_chase.ogg`

#### 🔊 FLASH_SoundEffects
- `FLASH_ding.wav`, `FLASH_discovery.wav`, `FLASH_flashlightOn.wav`, `FLASH_gameOver.ogg`
- `FLASH_jumpscare.ogg`, `FLASH_lowMonster.wav`, `FLASH_monsterStep.ogg`
- `FLASH_shock.wav`, `FLASH_steps.wav`, `FLASH_swoosh.ogg`

---

**Note:** If you have multiple Python versions, use `py` and `pip3` instead of `python` and `pip`.

---

⚠️ **IF YOU FIND ANY BUGS PLEASE REPORT THEM DIRECTLY TO ME** ⚠️
