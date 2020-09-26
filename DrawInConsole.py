import time 

# draw snake game in console

class DrawInConsole:
    # constructor
    def __init__(self, game, secs):
        self.game = game
        self.secs = secs
        self.reseting = False

    def reset(self):
        self.reseting = True

    def draw(self):
        while self.game.playing:
            self.reseting = False
            self.drawGrid()

            while self.game.playing and not self.game.isMoving() and not self.reseting:
                time.sleep(self.secs)

            while self.game.playing and self.game.isMoving() and not self.reseting:
                time.sleep(self.secs)
                self.drawGrid()

            if not self.reseting:
                print("score : " + str(self.game.score))
                print("snake len : " + str(self.game.lenOfSnake()))

            while self.game.playing and not self.reseting:
                time.sleep(self.secs)
        print("stop draw")

    # draw game's current state
    def drawGrid(self):
        verticalBorder = "#"
        horizontalBorder = "#"

        print("")
        print(horizontalBorder, end = "")
        for line in range(1, self.game.width + 2):
            #if head[1] == -1 and head[0] == line - 1:
            if self.game.posState(line - 1, -1) == self.game.PositionState.SNAKE_HEAD:
                print(horizontalBorder + "X", end = "")
            else:
                print(horizontalBorder + horizontalBorder, end = "")
        print("")

        for line in range(self.game.height):
            #if head[0] == -1 and head[1] == line:
            if self.game.posState(-1, line) == self.game.PositionState.SNAKE_HEAD:
                print("X", end = " ")
            else:
                print(verticalBorder, end = " ")
            for column in range(self.game.width):
                print(self.drawGameInConsolePos(column, line), end = " ")            
                
            #if head[0] == self._width and head[1] == line:
            if self.game.posState(self.game.width, line) == self.game.PositionState.SNAKE_HEAD:
                print("X")
            else:
                print(verticalBorder)
            
        print(horizontalBorder, end = "")
        for line in range(1, self.game.width + 2):
            #if head[1] == self._height and head[0] == line - 1:
            if self.game.posState(line - 1, self.game.height) == self.game.PositionState.SNAKE_HEAD:
                print(horizontalBorder + "X", end = "")
            else:
                print(horizontalBorder + horizontalBorder, end = "")
        print("")

    # draw position of grid according to it state
    def drawGameInConsolePos(self, x, y):
        if self.game.posState(x, y) == self.game.PositionState.EMPTY:
            return "."
        if self.game.posState(x, y) == self.game.PositionState.SNAKE or self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
            if self.game.dead and self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
                return "X"
            return "x"
        if self.game.posState(x, y) == self.game.PositionState.FOOD:
            return "o"