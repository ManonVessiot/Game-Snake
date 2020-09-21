import random

from Movement import Movement

class Snake:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.lastRemoved = None

        x = random.randrange(0, width)
        y = random.randrange(0, height)
        self.body = [(x, y)]
        print("Snake")
        print(self.body)

    def isSnake(self, x, y):
        return (x, y) in self.body

    def move(self, movement):
        snakeBiteHimself = False

        newHeadPos = (self.body[0][0] + movement[0], self.body[0][1] + movement[1])
        if newHeadPos in self.body[:-1]:
            snakeBiteHimself = True
        self.lastRemoved = self.body[-1]

        self.body = [newHeadPos] + self.body[:len(self.body) - 1]

        if snakeBiteHimself or newHeadPos[0] < 0 or newHeadPos[0] >= self.width or newHeadPos[1] < 0 or newHeadPos[1] >= self.height:
            return False
        return True

    def head(self):
        return self.body[0]

    def addPArt(self, move, numberOfPart):
        part = 0
        while part < numberOfPart:
            part += 1
            if self.lastRemoved != None:
                self.body.append(self.lastRemoved)
                self.lastRemoved = None
            elif len(self.body) ==1 or not self.addPartWithEnd():
                self.addPartWithMove(move)

    def addPartWithMove(self, move):
        newPart = (self.body[-1][0] - move[0], self.body[-1][1] - move[1])
        if newPart[0] < 0 or newPart[0] >= self.width or newPart[1] < 0 or newPart[1] >= self.height:
            return False
        self.body.append(newPart)
        return True
    
    def addPartWithEnd(self):
        endDiff = (self.body[-2][0] - self.body[-1][0], self.body[-2][1] - self.body[-1][1])
        return self.addPartWithMove(endDiff)