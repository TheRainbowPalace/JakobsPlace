#!/usr/bin/env python3

import sys
import os
import time
import random
import signal
import threading
import getch


#define the screen screen
class Screen:
    def __init__(self, right, bottom, platform):
        self.platform = platform
        self.top = 0
        self.bottom = bottom
        self.left = 0
        self.right = right
        self.running = 1
        self.screen = []
        #create the screen screen
        for i in range(self.bottom):
            self.screen.append([])
            for j in range(self.right):
                self.screen[i].append(0)
    def printScreen(self):
        #prints the screen screen
        for i in self.screen:
            result = ""
            for j in i:
                if (j == 0):
                    result += ". "
                else:
                    result += j + " "
            print(result)
    
def clearScreen():
    #clear the terminal
    os.system("clear")

class ScreenObject:
    def __init__(self, x, y, boundLeft, boundRight):
        self.alive = 1
        self.x = x
        self.y = y
        self.boundLeft = boundLeft
        self.boundRight = boundRight
    def moveLeft(self):
        if (self.x > self.boundLeft):
            self.x -= 1
    def moveRight(self):
        if (self.x < self.boundRight):
            self.x += 1

class Zombie(ScreenObject):
    def __init__(self, boundLeft, boundRight, boundTop, boundBottom):
        super().__init__(boundLeft, boundTop, boundLeft, boundRight)
        self.boundTop = boundTop
        self.boundBottom = boundBottom
    def update(self):
        self.y += 1
        #self.x += random.randint(-1, 1)

#create a player
class Player(ScreenObject):
    def __init__(self, x, y, boundLeft, boundRight):
        super().__init__(x, y, boundLeft, boundRight)
        self.left = 0
        self.right = 0
    def update(self):
        if (self.left):
            self.moveLeft()
            self.left = 0
        if (self.right):
            self.moveRight()
            self.right = 0

class Bcolors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLING = "\033[4m"



#define all screen variables
screen = Screen(5, 5, sys.platform)
player = Player(int(screen.right / 2), screen.bottom - 1, screen.left, screen.right - 1)
zombies = []
for i in range(3):
    zombie = Zombie(screen.left, screen.right - 1, screen.top, screen.bottom - 1)
    zombie.x = random.randint(screen.left, screen.right - 1)
    zombies.append(zombie)

userInput = getch._Getch()
#os.system("stty -echo") #turn of input echoing

def updatePlayer(self):
    screen.screen[player.y][player.x] = 0
    player.update()
    screen.screen[player.y][player.x] = Bcolors.GREEN + "X" + Bcolors.ENDC

def updateZombies():
    for i in zombies:
        if (i.y >= i.boundTop and i.y <= i.boundBottom and i.x >= i.boundLeft and i.x <= i.boundRight):
            screen.screen[i.y][i.x] = 0
        i.update()
        if (i.y >= i.boundTop and i.y <= i.boundBottom and i.x >= i.boundLeft and i.x <= i.boundRight):
            screen.screen[i.y][i.x] = Bcolors.RED + "O" + Bcolors.ENDC

#quit the application
def scriptEventQuit():
    clearScreen()
    sys.exit()

#stop the screen wait for the the threads to exit
def scriptEventStop():
    screen.running = 0
    #os.system("stty echo")
    time.sleep(500/1000) #sleep to make sure all threads are done
    #while(t.isAlive()):
    #    print("waiting")

#start the screen
def scriptEventStart():
    print("\nYou woke up, the clock say's it's 13' already and you ment to be at Jakob's place at 9, fuck!")
    print("We really gotta hurry!");
    print("You walk outside and BAM, Zombies, everywhere.\nGood to know that they are super slow.\n");
    userInput()

#the player lost the screen
def scriptEventLoose():
    clearScreen()
    print("Dammit! They got you!\nYou should probably call Jakob to tell him, you won't make it in time...")
    userInput()

#check if the player collided with a zombie
def collisionCheck():
    for i in zombies:
        if (i.x == player.x and i.y == player.y):
            scriptEventStop()
            scriptEventLoose()
            scriptEventQuit()

#get and evaluate the user input
def getInput():
    while(screen.running):
        key = userInput()
        if (key == "a"):
            player.left = 1
        if (key == "d"):
            player.right = 1
        if (key == "q"):
            scriptEventStop()
            scriptEventQuit()
        time.sleep(100/1000)

#update the screen logic
def logicloop():
    while(screen.running):
        updateZombies()
        updatePlayer()
        
        time.sleep(600/1000)
        collisionCheck()

#render the graphics at a given rate to the terminal
def renderloop():
    while(screen.running):
        #getInput()
        time.sleep(60/1000)
        clearScreen()
        screen.printScreen()

#scriptEventStart()

renderThread = threading.Thread(target = renderloop)
logicThread = threading.Thread(target = logicloop)
inputThread = threading.Thread(target = getInput)

logicThread.start()
renderThread.start()
inputThread.start()

