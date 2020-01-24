# Python3 CHIP-8 Emulator

CHIP-8 Emulator writen in Python3.

https://github.com/cassianoperin/Chip8_Python3/blob/master/images/pong.png


## Base Documentation
[Cowgod's Chip-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0)

[How to write an emulator (CHIP-8 interpreter) — Multigesture.net](http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/)

[Wikipedia - CHIP-8](https://en.wikipedia.org/wiki/CHIP-8)

## Features
* Pause and resume emulation
* Step Forward CPU Cycle for Debug



## Requirements
- Python3
- Pygame (on MAC, 2.0.0.dev5 or latest)

	`$ pip install pygame==2.0.0.dev5`


## Usage

1. From simple menu:

	`$ chmod +x menu.py chip8.py`

	`$ ./menu.py`



Select the number of the game.


2. Directly from emulator:

	`$ chmod +x chip8.py`

	`$ ./chip8.py ROM_NAME`


Where ROM_NAME is the name of one of the games inside "roms" folder.

3. Keys
- Original COSMAC Keyboard Layout:

	`1` `2` `3` `C`

	`4` `5` `6` `D`

	`7` `8` `9` `E`

	`A` `0` `B` `F`

- **Keys used in this emulator:**

	`1` `2` `3` `4`

	`Q` `W` `E` `R`

	`A` `S` `D` `F`

	`Z` `X` `C` `V`

	`P`: Pause and Resume emulation
	
	`[`: Step forward one CPU cycle with paused emulation (for debug and study purposes)
	
	`ESC`: Exit emulator

## Improvements

1. Equalize game speed (some games runs too fast, other slow)
2. Key pressing cause slowness
3. Improve draw method
