import threading
from enum import Enum

# movement of snake

class Move:

    # enum of snake's movements
    class Movement(Enum):
        NONE = 0,
        RIGHT = 1,
        LEFT = 2,
        UP = 3,
        DOWN = 4
    
    # constructor
    def __init__(self):
        self.lock = threading.Lock()
        self.move = self.Movement.NONE
        self.newMove = self.Movement.NONE

    def getMove(self):
        if self.newMove != self.Movement.NONE:
            self.move = self.newMove
            self.newMove = self.Movement.NONE

        if self.move == self.Movement.DOWN:
            return (0, 1)
        elif self.move == self.Movement.LEFT:
            return(-1, 0)
        elif self.move == self.Movement.UP:
            return (0, -1)
        elif self.move == self.Movement.RIGHT:
            return (1, 0)
        else:
            return (0, 0)

    def changeMove(self, newMove, turnBack):
        canChangeMove = (newMove == self.Movement.DOWN and (turnBack or self.move != self.Movement.UP))
        canChangeMove = canChangeMove or (newMove == self.Movement.LEFT and (turnBack or self.move != self.Movement.RIGHT))
        canChangeMove = canChangeMove or (newMove == self.Movement.UP and (turnBack or self.move != self.Movement.DOWN))
        canChangeMove = canChangeMove or (newMove == self.Movement.RIGHT and (turnBack or self.move != self.Movement.LEFT))

        if canChangeMove:
            self.newMove = newMove
            if self.move == self.Movement.NONE:
                self.move = self.newMove

    def stop(self):
        self.move = self.Movement.NONE

    def isMoving(self):
        return self.move != self.Movement.NONE
