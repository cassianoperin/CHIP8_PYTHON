# Python CHIP-8 Emulator

CHIP-8 Emulator writen in Python3 with simple code to be easy to be studied and understood.

<img width="430" alt="pong" src="https://github.com/cassianoperin/Chip8_Python3/blob/master/images/pong.png">

## Features
* Pause and resume emulation
* Step Forward CPU Cycle for Debug

## Requirements
- Python3
- Pygame

	`$ pip3 install pygame`


## Usage

1. From simple menu:

	`$ chmod +x menu.py chip8.py`

	`$ ./menu.py`


	Select the number of the game.


2. Directly from emulator:

	`$ chmod +x chip8.py`

	`$ ./chip8.py ROM_NAME`
	
3. Core options:

	* Enable/Disable Debug mode:
	Change the variable 'debug' to True|False into chip8.py
	
	
4. Keys
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

	`9`: Reset

	`ESC`: Exit emulator

## Documentation
[Cowgod's Chip-8 Technical Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#0.0)

[How to write an emulator (CHIP-8 interpreter) — Multigesture.net](http://www.multigesture.net/articles/how-to-write-an-emulator-chip-8-interpreter/)

[Wikipedia - CHIP-8](https://en.wikipedia.org/wiki/CHIP-8)
