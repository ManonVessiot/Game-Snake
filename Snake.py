import random

# manage snake move and evolution

class Snake:
    # constructor
    def __init__(self, width, height, border):
        self._width = width
        self._height = height
        self.border = border
        self.startedMoving = False

        self._lastRemoved = None

        x = random.randrange(0, width)
        y = random.randrange(0, height)
        self.body = [(x, y)]
        part2Move = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        i = random.randrange(0, len(part2Move))
        partAdded = self.addPArt(part2Move[i], 1)
        print("partAdded : " + str(partAdded))

        print("Snake.body : " + str(self.body))


    # check if pos is a snake part
    def isSnake(self, x, y, border):
        pos = (x, y)
        if border:
            pos = (x+1, y+1)
        return pos in self.body

    def getDiffsWithNeighbours(self, i):
        if (i not in range(len(self.body))) or len(self.body) < 2:
            return None

        index = i
        diff = []
        if index == 0:
            diff.append(None)
            x = self.body[index+1][0] - self.body[index][0]
            y = self.body[index+1][1] - self.body[index][1]
            if abs(x) > 1:
                x = - x / abs(x)
            if abs(y) > 1:
                y = - y / abs(y)
            diff1 = (x, y)
            diff.append(diff1)
        elif index == len(self.body) - 1:
            x = self.body[index-1][0] - self.body[index][0]
            y = self.body[index-1][1] - self.body[index][1]
            if abs(x) > 1:
                x = - x / abs(x)
            if abs(y) > 1:
                y = - y / abs(y)
            diff0 = (x, y)
            diff.append(diff0)
            diff.append(None)
        else:
            x = self.body[index-1][0] - self.body[index][0]
            y = self.body[index-1][1] - self.body[index][1]
            if abs(x) > 1:
                x = - x / abs(x)
            if abs(y) > 1:
                y = - y / abs(y)
            diff0 = (x, y)
            diff.append(diff0)
            x = self.body[index+1][0] - self.body[index][0]
            y = self.body[index+1][1] - self.body[index][1]
            if abs(x) > 1:
                x = - x / abs(x)
            if abs(y) > 1:
                y = - y / abs(y)
            diff1 = (x, y)
            diff.append(diff1)
        return diff



    # return len of snake body
    def lenOfBody(self):
        return len(self.body)

    # move snake according to the movement given
    def move(self, movement):
        snakeBiteHimself = False

        newHeadPos = [self.body[0][0] + movement[0], self.body[0][1] + movement[1]]
        if not self.border:
            if newHeadPos[0] < 0:
                newHeadPos[0] = self._width-1
            if newHeadPos[0] >= self._width:
                newHeadPos[0] = 0
            if newHeadPos[1] < 0:
                newHeadPos[1] = self._height-1
            if newHeadPos[1] >= self._height:
                newHeadPos[1] = 0
        
        if (newHeadPos[0], newHeadPos[1]) in self.body[:-1]:
            snakeBiteHimself = True

        self._lastRemoved = self.body[-1]
        self.body = [(newHeadPos[0], newHeadPos[1])] + self.body[:-1]

        if snakeBiteHimself:
            return False
        elif self.border and (newHeadPos[0] < 0 or newHeadPos[0] >= self._width or newHeadPos[1] < 0 or newHeadPos[1] >= self._height):
            return False
            
        self.startedMoving = True
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
            elif len(self.body) == 1 or not self._addPartWithEnd():
                part2Move = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                partAdded = False
                while not partAdded and len(part2Move) > 0:
                    partAdded = self._addPartWithMove(move)
                    if not partAdded:
                        part2Move.remove(move)
                        i = random.randrange(0, len(part2Move))
                        move = part2Move[i]
                if not partAdded:
                    return False
        return True

    # add part in snake's body according to a movement
    def _addPartWithMove(self, move):
        newPart = [self.body[-1][0] - move[0], self.body[-1][1] - move[1]]
        if newPart[0] < 0 or newPart[0] >= self._width or newPart[1] < 0 or newPart[1] >= self._height:
            if self.border:
                return False
            else:
                if newPart[0] < 0:
                    newPart[0] = self._width-1
                if newPart[0] >= self._width:
                    newPart[0] = 0
                if newPart[1] < 0:
                    newPart[1] = self._height-1
                if newPart[1] >= self._height:
                    newPart[1] = 0

        if (newPart[0], newPart[1]) in self.body:
            return False

        self.body.append((newPart[0], newPart[1]))
        return True
    
    # add part in snake's body according to the end of the snake's body
    def _addPartWithEnd(self):
        endDiff = (self.body[-2][0] - self.body[-1][0], self.body[-2][1] - self.body[-1][1])
        return self._addPartWithMove(endDiff)