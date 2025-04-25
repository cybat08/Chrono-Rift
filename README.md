# Chrono Rift

⚡ A fast-paced hybrid Python/C++ arena game where you battle endless waves of enemies across a shattered starfield — unlocking spells, weapons, and achievements as you survive the onslaught. ⚡

---

## 🚀 Features

- **Hybrid Python + C++** performance (PyOpenGL, Pygame, pybind11)
- **Smart Enemies** that chase and surround you
- **Dashing Ability** to evade and reposition (Shift Key)
- **Weapon Drops** (Laser Blaster, Heavy Cannon, Fireball, Lightning Strike)
- **Achievements System** with pop-up unlocks (First Blood, Spell Master, Boss Slayer)
- **XP, Leveling Up, and Upgrades** (Damage Up, Speed Up, Spell Power)
- **Boss Fights** every 3 levels (giant enemies + special boss music)
- **Scrolling Starfield Background** (dynamic parallax space effect)
- **Particle Effects** (explosions, dash trails, spell glows)
- **Full Sound Support** (background tracks, future sound FX ready)
- **Randomized Waves** — every play session is unique!

---

## 🎮 Controls

| Key             | Action                        |
|-----------------|-------------------------------|
| `WASD`           | Move Player                   |
| `Shift`          | Dash in movement direction    |
| `Space`          | Shoot spell                   |
| `1 2 3`          | Switch spell (Normal / Fireball / Lightning) |
| `Q / E`          | Switch random weapons you pick up |
| `I`              | Toggle inventory menu         |


---

## 🛠 How to Build and Run

**Option 1 (Easy Mode)**:
- Double-click `make_ex.bat`
- (It will build and immediately run the game.)

**Option 2 (Manual Mode)**:
```bash
mkdir build
cd build
cmake ..
cmake --build .
cd ..
python main.py
```
### 🧱 Requirements

- **Python 3.10 or higher**

- **Pygame (pip install pygame)**

- **pybind11 (pip install pybind11)**

- **C++ Compiler (Visual Studio, MinGW, or equivalent)**

- **CMake 3.0+**

---

## 🌌 Coming Soon

- **better assets/animations**

- **Power-ups (lifesteal, shield bubble)**

- **Player skins**
