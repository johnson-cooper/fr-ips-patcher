# Pokémon FireRed IPS Patcher (Windows)

A simple, user-friendly **IPS patcher for Pokémon FireRed** built with **Python + DearPyGui**.

This tool applies **multiple IPS patches in order** to a clean Pokémon FireRed ROM, with built-in **ROM verification**, **dry-run conflict detection**, and an easy-to-use GUI.

It can for example, create a **complete graphics & gameplay overhaul of Pokémon FireRed**, bundling patches from **LibertyTwins** and **Pokémon FireRed Essence** into a single, safe workflow.

![Preview](https://github.com/johnson-cooper/fr-ips-patcher/blob/main/images/1.png?raw=true)

---

## ✨ Features

- Multi-patch IPS application (applied in order)
- ROM verification
  - CRC32
  - SHA-1
- Dry-run conflict detection
  - Detects overlapping patch writes before applying
- Enable / disable individual patches
- Reorder patches (Up / Down)
- Detailed logging output
- Outputs a newly patched ROM (original remains untouched)

---

## 🎮 Included Patch Content

This patcher includes curated IPS patches from:

- **LibertyTwins**
- **Pokémon FireRed Essence**

Together, these provide a **full visual and gameplay overhaul**, including:

- Updated graphics and sprites
- Modernized mechanics
- Quality-of-life improvements
- Expanded gameplay systems

> This tool **does not distribute ROMs**. You must provide your own clean Pokémon FireRed ROM.

---

## 🖥️ Platform Support

### Windows (Recommended)

- Works out of the box using the included launcher

### macOS / Linux (Advanced)

- Requires manual setup
- Dependencies must be installed manually

---

## ▶️ How to Run (Windows)

### Easy Start (Recommended)

Clone or download this repository

Double-click:

```
!start.bat
```

No Python knowledge required.

---

## 🐍 Manual Setup (All Platforms)

### 1. Install Python

- Python **3.10+** recommended

### 2. Install dependencies

```
pip install dearpygui
```

### 3. Run the patcher

```
python main.py
```

---

## 📦 Expected ROM

This tool expects a **clean Pokémon FireRed ROM**, typically:

- Pokémon FireRed Version (USA)

The application displays **CRC32 and SHA-1 hashes** to verify ROM correctness before patching.

If the ROM does not match expected values, the tool will warn you before proceeding.

---

## 🧠 How It Works

1. Load a clean FireRed ROM
2. Select patches (enabled by default)
3. Reorder patches if desired
4. Run a dry-run to detect conflicts
5. Apply patches
6. Save the newly patched ROM

If conflicts are detected, the tool warns you **before writing anything**.

---

## ⚠️ Legal Notice

This project:

- Does **not** include Pokémon ROMs
- Does **not** distribute copyrighted game files
- Only distributes IPS patches and tooling

You must legally own a copy of Pokémon FireRed to use this software.

---

## ❤️ Credits

- **LibertyTwins** — patch authorship
- **Pokémon FireRed Essence** — gameplay overhaul
- **DearPyGui** — GUI framework
- Community ROM hacking tools & research

---

Happy hacking! 🔥

