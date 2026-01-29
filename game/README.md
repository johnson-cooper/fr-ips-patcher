# POKEMON FIRE RED — ETERNAL FLAME OVERHAUL

**A difficulty + enhancement hack of Pokémon FireRed**
*By attackishere*

---

## Overview

This is a difficulty and quality-of-life overhaul of Pokémon FireRed that brings in the first two generations (Gen I & II) to Kanto while keeping the core FireRed experience intact. The hack focuses on better trainer and wild encounters, polished visuals inspired by later DS/Emerald styles, and a set of balance changes that make the game more tactical and satisfying for experienced players.

This README is written to ship with the patch. It explains features, installation, credits, and known issues so you (and contributors) can get the cleanest experience possible.

---

## Key Features

* **Catch 'Em All (Gen 1 + Gen 2, 251 Pokémon)** — All 251 Pokémon from Gen I and Gen II are available in-game, placed in iconic and sensible locations across Kanto (based on the Catch Them All patch).
* **Enhanced Trainer Battles** — All trainer teams have been improved with better movesets and more thematic Pokémon.
* **Stronger Wild Encounters** — Wild Pokémon rosters and AI have been upgraded for more engaging encounters.
* **Boss & Trainer Additions** — Bosses have two extra Pokémon; important and regular trainers typically have one extra Pokémon added for challenge balance.
* **No Battle Potions (Optional / Set Battle Style)** — Potion-like healing items are removed from battle under the set battle style — plan ahead.
* **Deletable HMs** — HMs can be permanently removed after use for quality-of-life.
* **Updated Graphics** — Sprites, battle boxes, HP bars, and UI elements updated with DS/Generation II-inspired assets and Emerald-style menus.
* **Level Caps & Balance Tweaks** — Level cap system implemented for balance. EV caps and related changes added for competitive-style progression.
* **Extras & QoL Changes** (from Extras patch):

  * Faster save times
  * Tutorial elements removed
  * Infinite-use TMs and Move Tutors
  * Start with Running Shoes; run indoors
  * Persistent world changes (e.g., cut trees remain cut)
  * Repels stack properly
  * Poisons don't apply in overworld
  * Nature-highlighted stat colors in the Pokémon info screen
  * Abilities that affect egg-hatching (Magma Armor / Flame Body) now work
  * Lots of previously unobtainable items are now obtainable (Scope Lens, Choice Band, Light Ball, etc.)
  * Many glitches fixed (Pokedex species glitch, roaming IV glitch, Pomeg glitch, Nugget Bridge bug, etc.)
  * Various sound, UI and minor engine optimizations

> See `Newly-Added Items.txt` in the patch distribution for exact item locations.

---

## Gameplay Notes & Tips

* **Think Before You Use Items in Battle:** With potion-like items disabled (in set battle style), healing during battles is limited — stock up on full items and plan switch-ins.
* **Trainer Power Spike:** Expect more challenging trainer battles. Save before major trainers and use type advantages.
* **TMs & Move Tutors:** TMs and tutors are infinite — experiment freely.
* **Level Caps:** To keep progression balanced and avoid trivializing content, level caps are in place in some areas — this encourages team diversity.

---

## Installation (Quick)

1. Obtain a clean **Pokémon FireRed (U)** ROM. Make sure the ROM is unmodified.
2. Verify the ROM checksum (recommended):

   * Example on Linux/macOS: `crc32 FireRed.gba` or `md5sum FireRed.gba`
   * On Windows, use any checksum utility.
3. Apply the provided IPS patch with your preferred patcher (IPS/UPS). Example:

   * `patcher apply <FireRed.gba> <###.ips> output.gba`
4. Load `output.gba` in your emulator of choice. Recommended emulators: mGBA, VisualBoyAdvance-M.

**Note:** This patch was built against an unmodified FireRed base ROM. If you have errors during patching, ensure your ROM is the correct region/version and unmodified.

---

## Recommended Settings

* Emulator: mGBA (recommended for best compatibility) or VBA-M.
* Save type: Use in-emulator SRAM / battery saves.
* Cheats: Not recommended. Cheats may break scripted events and cause crashes.
* Emulator audio/video: Default settings are fine; turn on frame skip if needed for performance.

---

## Included Files

* `###.ips` — Main patch file.
* `Newly-Added Items.txt` — Exact locations for newly added/relocated items.
* `Credits.txt` — Full credits and contributors.
* `README.md` — This file.

---

## Credits (Selected)

**Author / Maintainer:** attackishere (title screen & many changes)

**Major Feature Patches & Tools:**

* Catch Them All, Extras — RichterSnipes
* IKARUS Patch — IKARUS, LibertyTwins, Alucus, ChaoticCherryCake, and many others

**Graphics & UI:**

* XY-styled battle boxes / HP bars / battle text: Verloren5
* GBC battle sprites revamp: captnotatroll, AlextheStarChild, EdensElite, peegeray, ElementalHeroShadow2, Uncle Dot, LibertyTwins, Matdemo159, reallyimjesus, PokeRevamp, nicholas
* Black & White text box: Green Jerry
* B2W2-styled bag / TM case / PokéMart / Berry pouch: Verloren5
* Emerald font: SidDays
* BW menus: LibertyTwins, Shiny Miner, Compumaxx, ansh860
* Battle backgrounds: LibertyTwins, princess-phoenix, carchagui, aveontrainer, WesleyFG, kWharever, worldslayer608, knizz
* Title screen: attackishere

**Gameplay / Fixes:**

* Pokedex glitch fixes, roaming IV fixes: HackMew
* Remove Potion-in-battle / Remove Shift from Options: attackishere
* Deletable HMs: JPAN
* Level Caps, hidden HP bars: BlackUser
* Various AI, wild scripts, EV caps: AkameTheBulbasaur, Touched, DoesntKnowHowToPlay, 1smash, and others

**Tools Used:**

* Universal Pokemon Randomizer ZX (Ajamar)
* HexManiAcAdvanced (haven1433)
* ModeXE (Li-Yun, Dreamaker, Vent)
* IPS Patcher FR (attackishere)

For a full, detailed list of contributors and who did what, see `Credits.txt` included with the patch.

---

## Known Issues & Compatibility

* This patch targets standard FireRed base ROMs. Patching non-standard or translated ROMs may fail or cause instability.
* Some minor graphical artifacts may remain in specific maps or battle backgrounds (work-in-progress).
* If you experience crashes: try a different emulator (mGBA recommended), verify ROM checksum, and confirm the patch applied successfully.

---

## Reporting Bugs & Contributing

If you find a bug or want to contribute:

1. Open an issue on the project's GitHub with:

   * The ROM checksum, emulator used, exact steps to reproduce, and a savestate if possible.
2. Fork the repo and open a PR for code or text improvements. Include clear notes and before/after images where helpful.

Please be respectful when reporting issues — include as much information as possible so maintainers can reproduce and fix the problem.

---

## Legal & Distribution

This project is a fan-made ROM hack. You must own a legal copy of Pokémon FireRed to apply this patch and play. Distribution of the original Pokémon FireRed ROM is illegal — this patch only modifies a legally obtained ROM. The project does not provide or host GBA ROMs.

---

## Change Log (High-level)

* v1.0 — Initial public release: Catch 'Em All integration, Extras QoL changes, trainer and wild encounter reworks, graphics updates, level caps, and bugfixes.

---

## Final Notes

Thanks for checking out this hack. It aims to balance nostalgia with modern improvements — catching all 251 Pokémon in a Kanto that feels familiar but refreshed. If you like the changes, star the GitHub repo and consider contributing to the credits or bug fixes.

Happy hacking — and good luck out there, trainer.

*— attackishere & contributors*
