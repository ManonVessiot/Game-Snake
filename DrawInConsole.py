
# draw snake game in console

class DrawInConsole:
    # constructor
    def __init__(self, game):
        self.game = game

    # draw game's current state
    def drawGameInConsole(self, playing):
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
                print(self.drawGameInConsolePos(column, line, playing), end = " ")            
                
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
    def drawGameInConsolePos(self, x, y, playing):
        if self.game.posState(x, y) == self.game.PositionState.EMPTY:
            return "."
        if self.game.posState(x, y) == self.game.PositionState.SNAKE or self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
            if not playing and self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
                return "X"
            return "x"
        if self.game.posState(x, y) == self.game.PositionState.FOOD:
            return "o"