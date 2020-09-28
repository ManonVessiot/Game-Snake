from tkinter import Tk, Canvas
from Move import Move

# draw snake game in console

class DrawWithTkinter:
    # constructor
    def __init__(self, game, posSize, secs):
        self.game = game
        self.posSize = posSize
        self.secs = int(secs * 250)
        self.reseting = False
        self.path = "/home/manon/Documents/Projects/MyProjects/SnakeGame_py/img/"

        self.grass = "grass.png"
        self.grassTexture = None

        self.food = "food.png"
        self.foodTexture = None

        self.rock = ["Rocks/rock1.png", "Rocks/rock2.png", "Rocks/rock3.png"]
        self.rockTexture = []
        self.rocksIndex = []

        self.snake = ["SnakePart/head.png", "SnakePart/body.png", "SnakePart/bodyTurn.png", "SnakePart/queue.png"]        
        self.snakeTexture = []

        self.fen = Tk()
        self.fen.title('Snake game')
        self.heiht = game.height * posSize
        self.width = game.width * posSize
        if self.game.border:
            self.heiht += 2 * posSize
            self.width += 2 * posSize

        print(str(self.width) + "x" + str(self.heiht))
        self.fen.geometry(str(self.width) + "x" + str(self.heiht))

        self.canvas = Canvas(self.fen, width=self.width, height=self.heiht)

    def reset(self):
        self.reseting = True

    def run(self):
        self.fen.mainloop()        

    def update1(self):
        if self.game.playing:
            self.reseting = False
            self.drawGrid()

            self.fen.after(self.secs, self.update2)
        else:
            print("stop draw")
            self.fen.destroy()

    def update2(self):
        if self.game.playing and not self.game.isMoving() and not self.reseting:
            self.fen.after(self.secs, self.update2)     
        else:
            self.fen.after(self.secs, self.update3)


    def update3(self):
        self.drawGrid()
        if self.game.playing and self.game.isMoving() and not self.reseting:
            self.fen.after(self.secs, self.update3)
        else:
            if not self.reseting:
                print("score : " + str(self.game.score))
                print("snake len : " + str(self.game.lenOfSnake()))
            self.fen.after(self.secs, self.update4)


    def update4(self):
        if self.game.playing and not self.reseting:
            self.fen.after(self.secs, self.update4)
        else:
            self.fen.after(self.secs, self.update1)


    def draw(self):
        self.fen.after(self.secs, self.update1)
        self.drawGrid()
        self.run()


    def drawGrid(self):
        self.drawGame()
        self.canvas.pack()

    def drawSquare(self, x, y, colorFill, colorOutline):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_rectangle(xCorner, yCorner, xCorner + self.posSize, yCorner + self.posSize, fill=colorFill, outline = colorOutline)

    def drawBorder(self, x, y):
        self.drawSquare(x, y, "black", "white")

    def drawSnake(self, x, y):
        self.drawSquare(x, y, "grey", "black")

    def drawSnakeHeadDead(self, x, y):
        self.drawSquare(x, y, "red", "white")

    def drawFood(self, x, y):
        self.drawSquare(x, y, "green", "black")

    def drawEmpty(self, x, y):
        self.drawSquare(x, y, "white", "black")

    def drawGame(self):
        self.canvas.delete("all")

        #Grid
        borderPart = 0
        if self.game.border:
            borderPart = 2
        for line in range(self.game.height + borderPart):
            for column in range(self.game.width + borderPart):
                self.drawEmpty(column, line)

        #Border
        if self.game.border:
            for line in range(self.game.height + 2):
                if line == 0 or line == self.game.height + 1:
                    for column in range(self.game.width + 2):
                        self.drawBorder(column, line)
                else:
                    self.drawBorder(0, line)
                    self.drawBorder(self.game.width + 1, line)
        
        #Food
        borderPart = 0
        if self.game.border:
            borderPart = 1
        for food in self.game.food.positions:            
            self.drawFood(food[0]+borderPart, food[1]+borderPart)
        
        #Snake
        for i in range(len(self.game.snake.body)-1, -1, -1):
            bodyPart = self.game.snake.body[i]
            state = -1
            if self.game.snake.startedMoving and not self.game.isMoving() and i == 0:
                self.drawSnakeHeadDead(bodyPart[0]+borderPart, bodyPart[1]+borderPart)
            else:
                self.drawSnake(bodyPart[0]+borderPart, bodyPart[1]+borderPart)

        
    
    # draw position of grid according to it state
    def drawGamePos(self, x, y):
        if self.game.posState(x, y) == self.game.PositionState.EMPTY:
            self.drawEmpty(x + 1, y + 1)
        if self.game.posState(x, y) == self.game.PositionState.SNAKE or self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
            if self.game.dead and self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(x + 1, y + 1)
            else:
                self.drawSnake(x + 1, y + 1)
        if self.game.posState(x, y) == self.game.PositionState.FOOD:
            self.drawFood(x + 1, y + 1)

    def stateOfSnake(self, i, part):
        diffs = self.game.snake.getDiffsWithNeighbours(i)
        if diffs != None:
            if (part == -1 or part == 0) and diffs[0] == None:
                #head rotation depend on diff of the neighbour ; state in (0, 1, 2, 3)
                if diffs[1] == (0, -1):
                    return 0
                if diffs[1] == (-1, 0):
                    return 1
                if diffs[1] == (0, 1):
                    return 2
                if diffs[1] == (1, 0):
                    return 3
            if (part == -1 or part == 2) and diffs[1] == None:
                #queue rotation depend on diff of the neighbour ; state in (10, 11, 12, 13)
                if diffs[0] == (0, 1):
                    return 10
                if diffs[0] == (1, 0):
                    return 11
                if diffs[0] == (0, -1):
                    return 12
                if diffs[0] == (-1, 0):
                    return 13
            
            #body rotation depend on diff of the 2 neighbour ; state in (4, 5, 6, 7, 8, 9)
            if diffs[0][0] == -diffs[1][0] and diffs[0][1] == -diffs[1][1]:
                if diffs[1][0] != 0:
                    return 4
                return 5
            if diffs[0][1] == 1 or diffs[1][1] == 1:
                if diffs[0][0] == -1 or diffs[1][0] == -1:
                    return 8
                if diffs[0][0] == 1 or diffs[1][0] == 1:
                    return 9
            if diffs[0][1] == -1 or diffs[1][1] == -1:
                if diffs[0][0] == -1 or diffs[1][0] == -1:
                    return 7
                if diffs[0][0] == 1 or diffs[1][0] == 1:
                    return 6
        
        if self.game.move.move == Move.Movement.DOWN:
            return 0
        elif self.game.move.move == Move.Movement.RIGHT:
            return 1
        elif self.game.move.move == Move.Movement.UP:
            return 2
        elif self.game.move.move == Move.Movement.LEFT:
            return 3
        else:
            return 0