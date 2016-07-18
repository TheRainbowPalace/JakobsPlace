import random

"""
To create a game you have to define a game class first.
The game class contains informatins about the size of the game frame and if the
game is running. By default running is set to true.
All game objects get the game class passed so they can check if they are out of 
border and so on.
"""
class Game:
    def __init__(self, boundLeft = 0, boundRight = 20, boundBottom = 0, boundTop = 10):
        self.boundLeft = boundLeft
        self.boundRight = boundRight
        self.boundTop = boundTop
        self.boundBottom = boundBottom
        self.running = True
        self.won = False
        self.lost = False
        self.usrInput = "_"
    def resetInput(self):
        self.usrInput = "_"

class Background:
    def __init__(self, game):
        self.frame = [] #defines the background frame
        for i in range(0, self.boundTop):
            self.frame.append([])
            for j in range(0, self.boundRight):
                self.frame[i].append(0)
    def fill(self, object):
        pass
    def fillAt(self, x, y, object):
        pass

#defines a game object in general
class GameObject:
    def __init__(self, game, x = 0, y = 0):
        self.alive = True
        self.x = x
        self.y = y
        self.game = game
    def moveHorizontal(self, amount, moveInBounds = True):
        if (moveInBounds):
            if (amount < 0):
                if (self.x + amount >= self.game.boundLeft):
                    self.x += amount
            if (amount > 0):
                if (self.x + amount <= self.game.boundRight):
                    self.x += amount
        else:
            self.x += amount
            return True
    def moveVertical(self, amount, moveInBounds = True):
        if (moveInBounds):
            if (amount > 0):
                if (self.y + amount <= self.game.boundTop):
                    self.y += amount
            if (amount < 0):
                if (self.y + amount >= self.game.boundBottom):
                    self.y += amount
        else:
            self.y += amount

#defines a zombie
class Zombie(GameObject):
    def __init__(self, game):
        super().__init__(game)
    def update(self):
        self.moveVertical(-1, False)
        self.moveHorizontal(random.randint(-1, 1))
        #check if the zombie is out of vertical bounds
        if (self.y < self.game.boundBottom):
            self.y = self.game.boundTop
            self.x = random.randint(self.game.boundLeft, self.game.boundRight)
            return True
        else:
            return False

#create a player
class Player(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
        self.score = 0
    def update(self):
        if (self.left):
            self.moveHorizontal(-1)
            self.left = 0
        elif (self.right):
            self.moveHorizontal(1)
            self.right = 0
        elif (self.up):
            self.moveVertical(1)
            self.up = False
        elif (self.down):
            self.moveVertical(-1)
            self.down = False

#check player-zombie collision
def collisionCheck(player, zombies):
    for i in zombies:
        if (i.x == player.x and i.y == player.y):
            return True
    return False
