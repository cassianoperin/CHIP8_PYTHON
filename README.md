# Python3 CHIP-8 Emulator

CHIP-8 Emulator writen in Python3.

## Base Documentation
[Cowgod's Chip-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0)

[How to write an emulator (CHIP-8 interpreter) — Multigesture.net](http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/)

[Wikipedia - CHIP-8](https://en.wikipedia.org/wiki/CHIP-8)



## Requirements
* Python3
* pygame (on MAC, 2.0.0.dev5 or latest)
  pip install pygame==2.0.0.dev5

## Usage

1. From simple menu:

	$ chmod +x menu.py chip8.py

	$ ./menu.py


Select the number of the game.


2. Directly from emulator:

	$ chmod +x chip8.py
	
	$ ./chip8.py ROM_NAME
	

Where ROM_NAME is the name of one of the games inside "roms" folder.

