#!/usr/bin/python3

import pygame
import math
import random
import os
import time
import threading
import sys

# Chip8 Hardware
memory		= [0] * 4096		# Memory (4096 Bytes)						[uint8/byte type]
stack		= [0] * 16		# 16 16-bit Stack to store return addresses when subroutines are called
v		= [0] * 16		# 16 V[x] general purpose 8-bit registers
graphics	= [0] * 64 * 32		# 64x32-pixel monochrome display (0,0)	(63,0) | (0,31)	(63,31)
key		= [0] * 16		# 16 keys keyboard. 1 represent key pressed.
opcode		= 0			# CPU Operation Code						[uint16 type]
pc		= 512			# Program Counter (start on address 512)	[uint16 type]
i		= 0			# This register is generally used to store memory addresses, so only the lowest (rightmost) 12 bits are usually used.
sp		= 0			# Stack Pointer
dt		= 0			# The delay timer is active whenever the delay timer register (DT) is non-zero.
st		= 0			# The sound timer is active whenever the sound timer register (ST) is non-zero.
# Variables
cycle		= 1			# CPU Cycle
opc_family	= 0			# Define the main group of opsets
drawflag	= 0			# Inform the window manager to print the graphic vector
pause		= 0			# Pause emulation
cycle_fwd	= 0			# When paused, add one CPU cycle

# Graphics
# define the RGB values
# NUMBER OR COLUMNS (X) AND LINES (Y)
X		= 64
Y		= 32
# MULTIPLICATE THE SIZE OF X and Y TO BIGGER RESOLUTIONS
PIXEL_SIZE_X	= 20
PIXEL_SIZE_Y	= 20
# Colors
white		= (255, 255, 255)
green		= (0, 255, 0)
blue 		= (0, 0, 128)
black		= (0, 0, 0)
red		= (255, 0, 0)
# PyGame
display_surface = ""

################################################################################
################################## FUNCTIONS ###################################

######## SHOW DEBUG INFORMATION ########
def show():
    global cycle, opc_family
    print ("\n" + str(cycle) + "\tPC: " + str(pc) + "(" + hex(pc) + ")" + "\tOpcode: " + hex(opcode) + "(" + str(hex(opc_family)) + ")" + "\tSP: " + str(sp) + "\tStack: " + str(stack) + \
        "\tV[x]: " + str(v) + "\tI: " + str(i) + "\tDT: " + str(dt) + "\tST: " + str(st))


####### LOAD ROM FILE INTO MEMORY #######
def load_rom(romname, memory):
	rom = open(romname,"rb").read()
	for byte in range(0, len(rom)):
		memory[byte+512]=rom[byte]


######### LOAD FONTSET TO MEMORY #########
def initialize_fonts(memory):
	fonts = [
		0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
		0x20, 0x60, 0x20, 0x20, 0x70, # 1
		0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
		0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
		0x90, 0x90, 0xF0, 0x10, 0x10, # 4
		0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
		0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
		0xF0, 0x10, 0x20, 0x40, 0x40, # 7
		0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
		0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
		0xF0, 0x90, 0xF0, 0x90, 0x90, # A
		0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
		0xF0, 0x80, 0x80, 0x80, 0xF0, # C
		0xE0, 0x90, 0x90, 0x90, 0xE0, # D
		0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
		0xF0, 0x80, 0xF0, 0x80, 0x80, # F
	]

	for i in range (0, len(fonts)):
	    memory[i] = fonts[i]


########## SHOW MEMORY (BINARY) ##########
def show_memory_binary(memory):
	index=0 			# start  [0]
	while index < 4096: 		# end [4096]
	    print (memory[index:index+16])
	    index+=16
	exit()


############ SHOW MEMORY (HEX) ############
def show_memory_hex(memory):
	index=0 			# start  [0]
	while index < 810: 		# end [4096]
		for i in range(index, index + 16):
			print ("\"" + hex(int(memory[i])) + "\"", end =" ")
		index+=16
		print ("\n")
	exit()


######### SHOW GRAPHICS (CONSOLE) #########
def show_graphics(graphics):
	colstart = 0
	colend 	 = 63
	while colend < 2048:
		for line in range (0, 32):
			#### Print 0 and 1s
			#print (line)
			#print (str(graphics[colstart:colend]))
			### Print just 1s
			print ("\n")
			for char in range (colstart, colend):
				if (graphics[char] == 0):
					print ("   ", end='')
				else:
					#print (graphics[char], end='')
					print ("[|]", end='')

			colend += 64
			colstart += 64


################################################################################
################################### OPCODES ####################################

############################ 0x0000 instruction set ############################
def x0000 ():
	global  opcode, pc, sp, stack, graphics

	# 00EE - RET
    # Return from a subroutine
    # The interpreter sets the program counter to the address at the top of the stack, then subtracts 1 from the stack pointer.
    # ### MUST MOVE TO NEXT ADDRESS AFTER THIS (PC+=2)
	if (hex(opcode) == "0xee"):
		# Return SP to the address in the top of the stack
		pc = stack[sp]
		# Move to next instruction
		pc += 2
		# Decrease the SP
		sp -= 1
		print ("\tOpcode 0xee executed. - Return from a subroutine")

	# 00E0 - CLS
	# Clear the display.
	elif (hex(opcode) !=" 0xee" ):
		graphics = [0] * 64 * 32
		pc += 2
		print ("\tOpcode 0xee executed. - Clear the display.")


############################ 0x1000 instruction set ############################
# 1nnn - JP addr
# Jump to location nnn.
# The interpreter sets the program counter to nnn.
def x1000():
    global pc

    nnn = opcode & int("0FFF", 16)
    pc = nnn

    print ("\tOpcode 1nnn executed. - JMP to NNN address.")


############################ 0x2000 instruction set ############################
# 2nnn - CALL addr
# Call subroutine at nnn.
# The interpreter increments the stack pointer, then puts the current PC on the top of the stack. The PC is then set to nnn.
def x2000():
    global sp, stack, pc, opcode

    sp += 1
    stack[sp] = pc
    nnn = opcode & int("0FFF", 16)
    pc = nnn

    print ("\tOpcode 2nnn executed. - Call Subroutine at NNN")


############################ 0x3000 instruction set ############################
# 3xkk - SE Vx, byte
# Skip next instruction if Vx = kk.
# The interpreter compares register Vx to kk, and if they are equal, increments the program counter by 2.
def x3000():
	global opcode, pc

	x = opcode & int("0F00", 16)
	x = x >> 8 # Need just the first byte

	kk = opcode & int("00FF", 16)

	if ( v[x] == kk ):
		pc += 4
		print ("\tOpcode 3xkk executed. - Equal SKIP ONE")
	else:
		pc += 2
		print ("\tOpcode 3xkk executed. - Different, NOT SKIP")


############################ 0x4000 instruction set ############################
# 4xkk - SNE Vx, byte
# Skip next instruction if Vx != kk.
# The interpreter compares register Vx to kk, and if they are not equal, increments the program counter by 2.
def x4000():
	global opcode, pc

	x = opcode & int("0F00", 16)
	x = x >> 8 # Just need the first byte

	kk = opcode & int("00FF", 16)

	if ( v[x] != kk ):
		pc += 4
		print ("\tOpcode 4xkk executed. - v[x] != kk, SKIP")
	else:
		pc += 2
		print ("\tOpcode 4xkk executed. - v[x] == kk, DONT SKIP")


############################ 0x5000 instruction set ############################
#5xy0 - SE Vx, Vy
#Skip next instruction if Vx = Vy.
#The interpreter compares register Vx to register Vy, and if they are equal, increments the program counter by 2.
def x5000 ():
	global opcode, pc, v

	# Map the value of x
	x = opcode & int("0F00", 16)
	x = x >> 8

	# Map the value of y
	y = opcode & int("00F0", 16)
	y = y >> 4

	if (v[x] == v[y]):
		pc += 4
		print ("\tOpcode 5xy0 executed. - v[x] == v[y], SKIP one instruction.")

	else:
		pc += 2
		print ("\tOpcode 5xy0 executed. - v[x] != v[y], DO NOT skip one instruction.")


############################ 0x6000 instruction set ############################
# 6xkk - LD Vx, byte
# Set Vx = kk.
# The interpreter puts the value kk into register Vx.
def x6000():
	global opcode, pc

	x = opcode & int("0F00", 16)
	x = x >> 8 # Need just the first byte

	kk = opcode & int("00FF", 16)

	v[x] = kk

	pc += 2
	print ("\tOpcode 6xkk executed. Set Vx = kk.")


############################ 0x7000 instruction set ############################
# 7xkk - ADD Vx, byte
# Set Vx = Vx + kk.
# Adds the value kk to the value of register Vx, then stores the result in Vx.
def x7000():
	global opcode, pc

	x = opcode & int("0F00", 16)
	x = x >> 8 # Just need the first byte

	kk = opcode & int("00FF", 16)

	v[x] += kk

	# Every time the value exceeds the size of register,
	# Store only the 8 least significant bits
	if (v[x] > 255):
		tmp="{0:016b}".format(v[x])[8:]
		v[x]=(int(tmp, 2))

	pc += 2

	print ("\tOpcode 7xkk executed. - Vx = Vx + kk.")


############################ 0x8000 instruction set ############################
# 0x8000 instruction set
def x8000 ():
	global opcode, pc, v

	# Normalize the opcode to map the instruction
	opc = opcode & int("F00F", 16)
	opc = format(opc, '02x')

	# Map the value of x
	x = opcode & int("0F00", 16)
	x = x >> 8

	# Map the value of y
	y = opcode & int("00F0", 16)
	y = y >> 4


	# 8xy0 - LD Vx, Vy
	# Set Vx = Vy.
	# Stores the value of register Vy in register Vx.
	if (opc == "8000"):
		v[x] = v[y]
		pc += 2
		print ("\tOpcode 8xy0 executed. - Set Vx = Vy.")


	# Set Vx = Vx OR Vy.
	# Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx. A bitwise OR compares the corrseponding bits from two values,
	# and if either bit is 1, then the same bit in the result is also 1. Otherwise, it is 0.
	elif (opc == "8001"):
		v[x] = v[x] | v[y]
		pc += 2
		print ("\tOpcode 8xy1 executed. - Set Vx = Vx OR Vy.")


	# 8xy2 - AND Vx, Vy
	# Set Vx = Vx AND Vy.
	# Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx. A bitwise AND compares the corrseponding bits from two values,
	# and if both bits are 1, then the same bit in the result is also 1. Otherwise, it is 0.
	elif (opc == "8002"):
		v[x] = v[x] & v[y]
		pc = pc + 2
		print ("\tOpcode 8xy2 executed. - Set Vx = Vx AND Vy.")


	# 8xy3 - XOR Vx, Vy
	# Set Vx = Vx XOR Vy.
	# Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in Vx. An exclusive OR compares the corrseponding bits from two values,
	# and if the bits are not both the same, then the corresponding bit in the result is set to 1. Otherwise, it is 0.
	elif (opc == "8003"):
		v[x] = v[x] ^ v[y]
		pc += 2
		print ("\tOpcode 8xy3 executed. - Set Vx = Vx XOR Vy.")


	# 8xy4 - ADD Vx, Vy
	# Set Vx = Vx + Vy, set VF = carry.
	# The values of Vx and Vy are added together. If the result is greater than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0.
	# Only the lowest 8 bits of the result are kept, and stored in Vx.
	elif (opc == "8004"):

		if ( (v[x] + v[y]) > 255):
			v[0xF] = 1
		else:
			v[0xF] = 0

		# Every time the value exceeds the size of register,
		# Store only the 8 least significant bits
		# v[x] += v[y]
		tmp="{0:016b}".format(v[x] + v[y])[8:]
		v[x]=(int(tmp, 2))

		# Old implementation, sum values, READ THE DOCS IN CASE OF PROBLEMS

		pc += 2
		print ("\tOpcode 8xy4 executed. - Set Vx = Vx AND Vy.")


	# 8xy5 - SUB Vx, Vy
	# Set Vx = Vx - Vy, set VF = NOT borrow.
	# If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted from Vx, and the results stored in Vx.
	elif (opc == "8005"):
		if ( v[x] >= v[y] ):
			v[0xF] = 1
		else:
			v[0xF] = 0

		v[x] = v[x] - v[y]

		if (v[x] < 0):
			v[x] = 256 + v[x]


		pc += 2
		print ("\tOpcode 8xy5 executed. - Set Vx = Vx - Vy.")


	# 8xy6 - SHR Vx {, Vy}
	# Set Vx = Vx SHR 1.
	# If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is divided by 2 (SHR).
	elif (opc == "8006"):
		# Prepare the data
		# Get the last bit of V[x]
		tmp="{0:08b}".format(v[x])[7:]

		# If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0.
		if ( int(tmp, 2)  == 1 ):
			v[0xF] = 1
		else:
			v[0xF] = 0

		# Set Vx = Vx SHR 1
		v[x] = v[x] >> 1

		### Original Chip8 INCREMENT I in this instruction ###

		pc += 2
		print ("\tOpcode 8xy6 executed. - SHR Vx {, Vy}.")


	# 8xy7 - SUBN Vx, Vy
	# Set Vx = Vy - Vx, set VF = NOT borrow.
	# If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted from Vy, and the results stored in Vx.
	elif (opc == "8007"):
		if (v[y] > v[x]):
			v[0xF] = 1
		else:
			v[0xF] = 0

		v[x] = v[y] - v[x]

		if (v[x] < 0):
			v[x] = 256 + v[x]


		pc += 2

		print ("\tOpcode 8xy7 executed. - Vx = Vy - Vx, set VF = NOT borrow.")


	# 8xyE - SHL Vx {, Vy}
	# Set Vx = Vx SHL 1.
	# If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is multiplied by 2.
	elif (opc == "800e"):
		# Prepare the data

		# Get the FIRST bit of V[x]
		tmp="{0:08b}".format(v[x])[:1]
		print (tmp)

		# If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0.
		# Then Vx is divided by 2.???? (((THE SHR DO THIS, NOT NECESSARY!)))
		if ( int(tmp, 2)  == 1 ):
			v[0xF] = 1
		else:
			v[0xF] = 0

		# Set Vx = Vx SHL 1
		v[x] = v[x] << 1

		# Every time the value exceeds the size of register,
		# Store only the 8 least significant bits
		if (v[x] > 255):
			tmp="{0:016b}".format(v[x])[8:]
			v[x]=(int(tmp, 2))

		### Original Chip8 INCREMENT I in this instruction ###

		pc += 2
		print ("\tOpcode 8xyE executed. - SHL Vx {, Vy}. ----- SUSPICIOUS ------")


############################ 0x9000 instruction set ############################
# 9xy0 - SNE Vx, Vy
# Skip next instruction if Vx != Vy.
# The values of Vx and Vy are compared, and if they are not equal, the program counter is increased by 2.
def x9000():
	global opcode, pc

	x = opcode & int("0F00", 16)
	x = x >> 8 # Just need the first byte

	y = opcode & int("00F0", 16)
	y = y >> 4

	if ( v[x] != v[y] ):
		pc += 4
		print ("\tOpcode 9xy0 executed. - Vx != Vy, SKIP one instruction.")
	else:
		pc += 2
		print ("\tOpcode 3xkk executed. - Vx = Vy, DO NOT SKIP one instruction.")


############################ 0xA000 instruction set ############################
# Annn - LD I, addr
# Set I = nnn.
# The value of register I is set to nnn.
def xA000():
	global opcode, pc, i

	nnn = opcode & int("0FFF", 16)
	i = nnn

	pc += 2

	print ("\tOpcode Annn executed. - Set I = nnn.")


############################ 0xB000 instruction set ############################
# Bnnn - JP V0, addr
# Jump to location nnn + V0.
# The program counter is set to nnn plus the value of V0.
def xB000():
	global opcode, pc, v

	nnn = opcode & int("0FFF", 16)
	pc = nnn + v[0x0]

	print ("\tOpcode Bnnn executed. - Jump to location nnn + V0.")


############################ 0xC000 instruction set ############################
# Cxkk - RND Vx, byte
# Set Vx = random byte AND kk.
# The interpreter generates a random number from 0 to 255, which is then ANDed with the value kk. The results are stored in Vx. See instruction 8xy2 for more information on AND.
def xC000():
	global opcode, v, pc

	x = opcode & int("0F00", 16)
	x = x >> 8 # Just need the first byte

	kk = opcode & int("00F0", 16)

	v[x] = random.randint(0,255) & kk

	pc += 2

	print ("\tOpcode Cxkk executed. - Vx = random byte AND kk.")


############################ 0xD000 instruction set ############################
# Dxyn - DRW Vx, Vy, nibble
# Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
def xD000():
	global opcode, i, v, graphics, pc, drawflag

	x = opcode & int("0F00", 16)
	x = x >> 8 # Just need the first byte

	y = opcode & int("00F0", 16)
	y = y >> 4

	n = opcode & int("000F", 16)

	v[0xF] = 0

	print ("\tOpcode: " + hex(opcode) + " Dxyn - DRAW GRAPHICS! - Address I: " + str(i) +  " Position V[x(" + str(x) + ")]: " + str(v[x]) + ", V[y(" + str(y) + ")]: " + str(v[y]) + " , N: " + str(n) + " bytes.")

    # Check if y is out of range
	if (v[y] > 31):
		v[y] = v[y] % 32
		print ("\tV[y] > 31, modulus applied")

    # Check if x is out of range
	if (v[x] > 63):
		v[x] = v[x] % 64
		print ("\tV[x] > 63, modulus applied")

	# Translate the x and Y to the Graphics Vector
	gpx_position = (v[x] + (64 * v[y]))

	# DEBUG
	# print ("\tGraphic vector position: " + str(gpx_position) + " (Value: " + str(graphics[x + (64 * y)]) + ")\n" )


	# Print N Bytes from address I in V[x]V[y] position of the screen
	for byte in range(0, n):

		sprite=memory[i + byte]
		binary="{0:08b}".format(sprite)

		# Always print 8 bits
		for bit in range (0, 8):
			# Set the index to write the 8 bits of each pixel
			index = gpx_position + bit + (byte*64)

			# If tryes to draw bits outside the vector size, ignore
			if ( index > 2047):
				continue

			# If bit=1, test current graphics[index], if is already set, mark v[F]=1 (colision)
			if (int(binary[bit]) == 1):
				if (graphics[index] == 1):
					v[0xF] = 1
				# After, XOR the graphics[index] (DRAW)
				graphics[index] ^= 1

			# DEBUG
			# print ("\tByte: " +str(byte)+ "\tSprite: "+str(sprite)+ "\tBinary: "+  binary + "\tbit: " +str(bit)+ "\tIndex: " + str(index) + "\tbinary[bit]: " + binary[bit] + "\tGraphics[index]: " + str(graphics[index]) )

	pc += 2
	drawflag = 1


############################ 0xE000 instruction set ############################
# 0xE000 instruction set
def xE000 ():
	global opcode, pc, key, v

	# Normalize the opcode to map the instruction
	opc = opcode & int("F0FF", 16)
	opc = format(opc, '02x')

	x = opcode & int("0F00", 16)
	x = x >> 8

	# ExA1 - SKNP Vx
	# Skip next instruction if key with the value of Vx is not pressed.
	# Checks the keyboard, and if the key corresponding to the value of Vx is currently in the up position, PC is increased by 2.
	if (opc == "e0a1"):
		if ( key[v[x]] == 0 ):
			pc += 4
			print ("\tOpcode e0a1 - Key " + str(v[x]) + " NOT pressed, skip one instruction")
		else:
			pc += 2
			print ("\tOpcode e0a1 - Key " + str(v[x]) + " Pressed, continue")


	# Ex9E - SKP Vx
	# Skip next instruction if key with the value of Vx is pressed.
	# Checks the keyboard, and if the key corresponding to the value of Vx is currently in the down position, PC is increased by 2.
	elif (opc == "e09e" ):
		if ( key[v[x]] == 1 ):
			pc += 4
			print ("\tOpcode e0a1 - Key " + str(v[x]) + " PRESSED, skip one instruction")
		else:
			pc += 2
			print ("\tOpcode e0a1 - Key " + str(v[x]) + " Not pressed, continue")


############################ 0xF000 instruction set ############################
# 0xF000 instruction set (Fxyy)
def xF000 ():
	global opcode, pc, sp, stack, memory, v, i, dt, st, key

	# Normalize the opcode to map the instruction
	opc = opcode & int("F0FF", 16)
	opc = format(opc, '02x')

	# Map the value of x
	x = opcode & int("0F00", 16)
	x = x >> 8


	# Fx07 - LD Vx, DT
	# Set Vx = delay timer value.
	# The value of DT is placed into Vx.
	if (opc == "f007"):
		v[x] = dt
		pc += 2
		print ("\tOpcode Fx07 executed. - Set Vx = delay timer value.")


	# Fx0A - LD Vx, K
	# Wait for a key press, store the value of the key in Vx.
	# All execution stops until a key is pressed, then the value of that key is stored in Vx.
	elif (opc =="f00a"):
		for k in range (0, len(key)):
			if (key[k] == 1):
				v[x] = k
				pc +=2
				print ("\tOpcode Fx0A executed. - Wait for a key press (PRESSED)")
				# Stop after find the first key pressed
				break
			else:
				print ("\tOpcode Fx0A executed. - Wait for a key press (NOT PRESSED)")

	# Fx15 - LD DT, Vx
	# Set delay timer = Vx.
	# DT is set equal to the value of Vx.
	elif (opc =="f015"):
		dt = v[x]
		pc += 2
		print ("\tOpcode Fx15 executed. - Set delay timer = Vx.")


	# Fx18 - LD ST, Vx
	# Set sound timer = Vx.
	# ST is set equal to the value of Vx.
	elif (opc =="f018"):
		st = v[x]
		pc += 2
		print ("\tOpcode Fx18 executed. - Set sound timer = Vx.")


	# Fx1E - ADD I, Vx
	# Set I = I + Vx.
	# The values of I and Vx are added, and the results are stored in I.
	elif (opc =="f01e"):
		i += v[x]
		pc += 2
		print ("\tOpcode Fx1E executed. - Set I = I + Vx.")


	# Fx29 - LD F, Vx
	# Set I = location of sprite for digit Vx.
	# The value of I is set to the location for the hexadecimal sprite corresponding to the value of Vx. See section 2.4, Display, for more information on the Chip-8 hexadecimal font.
	elif (opc =="f029"):
		#print (v[x])
		i = v[x]  * 5
		pc += 2
		print ("\tOpcode Fx29 executed. - Set I = location of sprite for digit Vx. (*5)")


	# Fx33 - LD B, Vx
	# Store BCD representation of Vx in memory locations I, I+1, and I+2.
	#set_BCD(Vx);
	# Ex. V[x] = ff (maximum value) = 255
	# memory[i+0] = 2
	# memory[i+1] = 5
	# memory[i+2] = 5
	# % = modulus operator:
	# 3 % 1 would equal zero (since 3 divides evenly by 1)
	# 3 % 2 would equal 1 (since dividing 3 by 2 results in a remainder of 1).
	elif (opc =="f033"):
		# memory [i] = most important byte
		memory[i] = math.trunc(v[x] / 100)
		# memory [i+1] = second most important byte
		memory[i + 1] = math.trunc( (v[x] / 10) %10 )
		# memory [i+2] = third most important byte
		memory[i + 2] = math.trunc( (v[x] % 100) %10 )

		pc += 2

		print ("\tOpcode Fx33 executed. - Store BCD representation of Vx in memory locations I, I+1, and I+2.")


	# Fx55 - LD [I], Vx
	# Store registers V0 through Vx in memory starting at location I.
	# The interpreter copies the values of registers V0 through Vx into memory, starting at the address in I.
	#
	# Stores V0 to VX (including VX) in memory starting at address I. The offset from I is increased by 1 for each value written, but I itself is left unmodified.[d]
	# In the original CHIP-8 implementation, and also in CHIP-48, I is left incremented after this instruction had been executed. In SCHIP, I is left unmodified.
	elif (opc =="f055"):

		for j in range (0, x + 1):
			memory[i + j] = v[j]

		pc += 2

		### Original Chip8 INCREMENT I in this instruction ###

		print ("\tOpcode Fx55 executed. Store registers V0 through Vx in memory starting at location I.")


	# Fx65 - LD Vx, [I]
	# Read registers V0 through Vx from memory starting at location I.
	# The interpreter reads values from memory starting at location I into registers V0 through Vx.
	### I is set to I + X + 1 after operation²
	### ² Erik Bryntse’s S-CHIP documentation incorrectly implies this instruction does not modify
	### the I register. Certain S-CHIP-compatible emulators may implement this instruction in this manner.
	### MAYBE NEED TO IMPLEMENT NO S-CHIP8 ***
	elif (opc =="f065"):

		for j in range(0, x + 1):
			v[j] = memory[i + j]

		pc += 2

		### Original Chip8 INCREMENT I in this instruction ###

		print ("\tOpcode Fx65 executed. Read registers V0 through Vx from memory starting at location I.")

def delaytimer (value):
	#print (value)
	while (value > 0):
		time.sleep(0.016)
		#print (value)
		value -= 1

def soundtimer (value):
	#print (value)
	while (value > 0):
		time.sleep(0.016)
		#print (value)
		value -= 1
		if (value ==0):
			pygame.mixer.init()
			sound = pygame.mixer.Sound('sounds/beep.wav')
			sound.play()


############################ MAIN CPU LOOP ############################
def cpu():
	global memory, pc, opc_family, dt, opcode, cycle, st

        # Read the Opcode (mem[pc]+mem[pc+1])
	# Format used to always have 2 digits
	opcode_tmp=format(memory[pc], '02x') + format(memory[pc+1], '02x')
	# Make opcode binary after processing to save
	opcode=int(opcode_tmp, 16)

	# Set the Opcode Family
	opc_family=opcode & int("F000", 16)

	# Print the Debug Information
	show()

	# Delay Timer
	# if (dt > 0):
	# 	dt -= 1
	if (dt > 0):
		thread_delay = threading.Thread(target=delaytimer, args=(dt,))
		# Send the dt value to be handled by the threads
		dt=0
		#print (st)
		thread_delay.start()

	# Sound Timer
	# if (st > 0):
	# 	st -= 1
	# 	if (st == 0):
	# 		#print ("BEEP")
	# 		#os.system("afplay xp.wav")
	# 		pygame.mixer.init()
	# 		sound = pygame.mixer.Sound('sounds/beep.wav')
	# 		sound.play()
	### Implemented Threading for SoundTimer
	if (st > 0):
		thread_sound = threading.Thread(target=soundtimer, args=(st,))
		# Send the st value to be handled by the threads
		st=0
		#print (st)
		thread_sound.start()

	########### EXECUTE CPU OPCODE #########
	if (opc_family == 0):			# 0x0000
		x0000()
	elif (opc_family == 4096):		# 0x1000
		x1000()
	elif (opc_family == 8192):		# 0x2000
		x2000()
	elif (opc_family == 12288):		# 0x3000
		x3000()
	elif (opc_family == 16384):		# 0x4000
		x4000()
	elif (opc_family == 20480):		# 0x5000
		x5000()
	elif (opc_family == 24576):		# 0x6000
		x6000()
	elif (opc_family == 28672):		# 0x7000
		x7000()
	elif (opc_family == 32768):		# 0x8000
		x8000()
	elif (opc_family == 36864):		# 0x9000
		x9000()
	elif (opc_family == 40960):		# 0xA000
		xA000()
	elif (opc_family == 45056):		# 0xB000
		xB000()
	elif (opc_family == 49152):		# 0xC000
		xC000()
	elif (opc_family == 53248):		# 0xD000
		xD000()
	elif (opc_family == 57344):		# 0xE000
		xE000()
	elif (opc_family == 61440):		# 0F000
		xF000()

	# Increment the cycle (just for logging purposes)
	cycle += 1


################################################################################
################################### DISPLAY ####################################

def initialize_graphics():
	global display_surface

	pygame.init()

	# create the display surface object
	# of specific dimension..e(X,Y).
	display_surface = pygame.display.set_mode( ( X * PIXEL_SIZE_X, Y * PIXEL_SIZE_Y ) )

	# set the pygame window name
	pygame.display.set_caption('CHIP 8')

	# completely fill the surface object
	# with white colour
	display_surface.fill(black)
	#return display_surface
	######


################################################################################
################################## MAIN LOOP ###################################

def initialize_cpu_loop():
	global key, display_surface, drawflag, pause, cycle_fwd
	# infinite loop
	while True :

		# Reset the Draw Flag
		drawflag = 0

		# Handle QUIT event
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
	            # deactivates the pygame library
				pygame.quit()
	            # Quit the program.
				quit()

		# Handle Keyboard INPUTS
		keys = pygame.key.get_pressed()

		# Close emulator
		if keys[pygame.K_ESCAPE]:
			pygame.quit()
			exit()

		if keys[pygame.K_0]:
			key[0] = 1

		if keys[pygame.K_1]:
			key[1] = 1

		if keys[pygame.K_4]:
			key[2] = 1

		if keys[pygame.K_3]:
			key[3] = 1

		if keys[pygame.K_2]:
			key[4] = 1

		if keys[pygame.K_5]:
			key[5] = 1

		if keys[pygame.K_6]:
			key[6] = 1

		if keys[pygame.K_7]:
			key[7] = 1

		if keys[pygame.K_8]:
			key[8] = 1

		if keys[pygame.K_9]:
			key[9] = 1

		if keys[pygame.K_LEFT]:
			key[10] = 1

		if keys[pygame.K_RIGHT]:
			key[11] = 1

		if keys[pygame.K_UP]:
			key[12] = 1

		if keys[pygame.K_DOWN]:
			key[13] = 1

		if keys[pygame.K_q]:
			key[14] = 1

		if keys[pygame.K_w]:
			key[15] = 1

		# Pause
		if keys[pygame.K_p]:
			if (pause == 0):
				pause = 1
				time.sleep(0.2)
			else:
				pause = 0
				time.sleep(0.2)


		if keys[pygame.K_LEFTBRACKET]:
			if (pause == 1):
					cycle_fwd = 1
					# Execute one cpu cycle
					cpu()
					time.sleep(0.3)

		# Call the main CPU Function
		# If pause button not pressed, run a new cpu cycle
		if (pause != 1):
			cpu()

		# Create the window and handle with Graphics
		if (drawflag == 1):
			display_surface.fill(black)
			#show_graphics(graphics)

			for gfxindex in range(0, len(graphics)):
				if (graphics[gfxindex]==1):
			        #print ("1 found, need to draw")
			        #print (graphics[gfxindex])
					if (gfxindex < 64):
						x=gfxindex
						y=0
						pygame.draw.rect(display_surface, white, (x*20, y*20, PIXEL_SIZE_X, PIXEL_SIZE_Y))
					else:
						y=0
						nro=gfxindex
						while (nro >= 64):
							nro -= 64
							y = y + 1
							x = nro
						pygame.draw.rect(display_surface, white, (x*20, y*20, PIXEL_SIZE_X, PIXEL_SIZE_Y))
			### RENDER MODE 1
			### Slow, need to draw the entire screen each draw instruction
			# pygame.display.flip()

		### RENDER MODE 2
		### Update the entire screen each X cycles
		############### FRAMESKIP #################
		# Force do draw when in pause/cycle forward debug mode
		if (cycle_fwd == 1):
			pygame.display.flip()
		else:
			if ( cycle % 16 == 0 ):
				pygame.display.flip()

		# Release Buttons
		key = [0] * 16
		# Unflag cycle_fwd Fla
		cycle_fwd = 0

		# DEBUG - SEARCH FOR VALUES LARGER THAN 255 in V[]
		#for k in range(0, 15):
		#	if (v[k] > 255):
		#		print ("\tValue bigger than 255 detected on v[x] (8bits array). EXITING")
		#		show()
		#		exit()

		# DEBUG - SEARCH FOR NEGATIVE VALUES in V[]
		#for k in range(0, 15):
		#	if (v[k] < 0):
		#		print ("\tNegative value detected. EXITING")
		#		show()
		#		exit()


################################################################################
################################## PROCESSING ##################################

# Receive ROM NAME as argument or exit
# if (len (sys.argv) != 2):
#     print ("\nUsage: " + sys.argv[0] + " ROM NAME!\nExiting.\n")
#     exit()
# load_rom("roms/"+sys.argv[1], memory)

# Load hardcoded ROM NAME
load_rom("roms/VBRIX", memory)
initialize_fonts(memory)
#show_memory_binary(memory)
#show_memory_hex(memory)
#show_graphics(graphics)
initialize_graphics()
initialize_cpu_loop()
