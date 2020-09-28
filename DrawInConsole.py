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
        if self.game.border:
            print(horizontalBorder, end = "")
            for line in range(1, self.game.width + 2):
                if (line-1, -1) == self.game.snake.head():
                    print(horizontalBorder + "O", end = "")
                else:
                    print(horizontalBorder + horizontalBorder, end = "")
            print("")

        for line in range(self.game.height):
            if self.game.border:
                if (-1, line) == self.game.snake.head():
                    print("O", end = " ")
                else:
                    print(verticalBorder, end = " ")
            for column in range(self.game.width):
                print(self.drawGameInConsolePos(column, line), end = " ")            
            
            if self.game.border:
                if (self.game.width, line) == self.game.snake.head():
                    print("O", end = " ")
                else:
                    print(verticalBorder, end = " ")
            print("")
            
        if self.game.border:
            print(horizontalBorder, end = "")
            for line in range(1, self.game.width + 2):
                #if head[1] == self._height and head[0] == line - 1:
                if (line - 1, self.game.height) == self.game.snake.head():
                    print(horizontalBorder + "O", end = "")
                else:
                    print(horizontalBorder + horizontalBorder, end = "")
        print("")

    # draw position of grid according to it state
    def drawGameInConsolePos(self, x, y):
        if self.game.food.isFood(x, y):
            return "x"
        if self.game.snake.isSnake(x, y, False):
            if (x, y) == self.game.snake.head():
                return "O"
            return "o"
        return "."