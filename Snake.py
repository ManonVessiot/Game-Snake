import random

# manage snake move and evolution

class Snake:
    # constructor
    def __init__(self, width, height):
        self._width = width
        self._height = height

        self._lastRemoved = None

        x = random.randrange(0, width)
        y = random.randrange(0, height)
        self.body = [(x, y)]

    # check if pos is a snake part
    def isSnake(self, x, y):
        return (x, y) in self.body

    def getDiffsWithNeighbours(self, i):
        if (i not in range(len(self.body))) or len(self.body) < 2:
            return None

        index = i
        diff = []
        if index == 0:
            diff.append(None)
            diff1 = (self.body[index+1][0] - self.body[index][0], self.body[index+1][1] - self.body[index][1])
            diff.append(diff1)
        elif index == len(self.body) - 1:
            diff0 = (self.body[index-1][0] - self.body[index][0], self.body[index-1][1] - self.body[index][1])
            diff.append(diff0)
            diff.append(None)
        else:
            diff0 = (self.body[index-1][0] - self.body[index][0], self.body[index-1][1] - self.body[index][1])
            diff.append(diff0)
            diff1 = (self.body[index+1][0] - self.body[index][0], self.body[index+1][1] - self.body[index][1])
            diff.append(diff1)
        return diff



    # return len of snake body
    def lenOfBody(self):
        return len(self.body)

    # move snake according to the movement given
    def move(self, movement):
        snakeBiteHimself = False

        newHeadPos = (self.body[0][0] + movement[0], self.body[0][1] + movement[1])
        if newHeadPos in self.body[:-1]:
            snakeBiteHimself = True
        self._lastRemoved = self.body[-1]

        self.body = [newHeadPos] + self.body[:len(self.body) - 1]

        if snakeBiteHimself or newHeadPos[0] < 0 or newHeadPos[0] >= self._width or newHeadPos[1] < 0 or newHeadPos[1] >= self._height:
            return False
        return True

    # return head pos
    def head(self):
        return self.body[0]

    # add part in snake's body
    def addPArt(self, move, numberOfPart):
        part = 0
        while part < numberOfPart:
            part += 1
            if self._lastRemoved != None:
                self.body.append(self._lastRemoved)
                self._lastRemoved = None
            elif len(self.body) ==1 or not self._addPartWithEnd():
                self._addPartWithMove(move)

    # add part in snake's body according to a movement
    def _addPartWithMove(self, move):
        newPart = (self.body[-1][0] - move[0], self.body[-1][1] - move[1])
        if newPart[0] < 0 or newPart[0] >= self._width or newPart[1] < 0 or newPart[1] >= self._height:
            return False
        self.body.append(newPart)
        return True
    
    # add part in snake's body according to the end of the snake's body
    def _addPartWithEnd(self):
        endDiff = (self.body[-2][0] - self.body[-1][0], self.body[-2][1] - self.body[-1][1])
        return self._addPartWithMove(endDiff)