#!/usr/bin/python3
import sys
import subprocess

emulator="./chip8.py"

for i in range (0, 10):
    print ("\n")

print ("GAME LIST:\n")
print ("\t 1 - 15PUZZLE")
print ("\t 2 - BLINKY")
print ("\t 3 - BLITZ")
print ("\t 4 - BRIX")
print ("\t 5 - CONNECT4")
print ("\t 6 - GUESS")
print ("\t 7 - HIDDEN")
print ("\t 8 - INVADERS")
print ("\t 9 - KALEID")
print ("\t10 - MAZE")
print ("\t11 - MERLIN")
print ("\t12 - MISSILE")
print ("\t13 - PONG")
print ("\t14 - PONG2")
print ("\t15 - PUZZLE")
print ("\t16 - SYZYGY")
print ("\t17 - TANK")
print ("\t18 - TETRIS")
print ("\t19 - TICTAC")
print ("\t20 - UFO")
print ("\t21 - VBRIX")
print ("\t22 - VERS")
print ("\t23 - WIPEOFF")
print ("\t24 - PONG ALTERNATIVE")



game=input("\nType Game NUMBER:\n")
if (game == "1"):
    print ("15PUZZLE")
    game = "15PUZZLE"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "2"):
    print ("BLINKY")
    game = "BLINKY"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "3"):
    print ("BLITZ")
    game = "BLITZ"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "4"):
    print ("BRIX")
    game = "BRIX"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "5"):
    print ("CONNECT4")
    game = "CONNECT4"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "6"):
    print ("GUESS")
    game = "GUESS"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "7"):
    print ("HIDDEN")
    game = "HIDDEN"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "8"):
    print ("INVADERS")
    game = "INVADERS"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "9"):
    print ("KALEID")
    game = "KALEID"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "10"):
    print ("MAZE")
    game = "MAZE"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "11"):
    print ("MERLIN")
    game = "MERLIN"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "12"):
    print ("MISSILE")
    game = "MISSILE"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "13"):
    print ("PONG")
    game = "PONG"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "14"):
    print ("PONG2")
    game = "PONG2"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "15"):
    print ("PUZZLE")
    game = "PUZZLE"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "16"):
    print ("SYZYGY")
    game = "SYZYGY"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "17"):
    print ("TANK")
    game = "TANK"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "18"):
    print ("TETRIS")
    game = "TETRIS"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "19"):
    print ("TICTAC")
    game = "TICTAC"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "20"):
    print ("UFO")
    game = "UFO"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "21"):
    print ("VBRIX")
    game = "VBRIX"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "22"):
    print ("VERS")
    game = "VERS"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "23"):
    print ("WIPEOFF")
    game = "WIPEOFF"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "24"):
    print ("PONG3")
    game = "pong.ch8"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
elif (game == "2"):
    print ("BLINKY")
    game = "BLINKY"
    args=emulator + " " + game
    subprocess.call(args, shell=True)
else:
    print ("\nGame not found.\nExiting.\n")
