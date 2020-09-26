from tkinter import Tk, Canvas

# draw snake game in console

class DrawWithTkinter:
    # constructor
    def __init__(self, game, posSize, secs):
        self.game = game
        self.posSize = posSize
        self.secs = int(secs * 500)
        self.reseting = False

        self.fen = Tk()
        self.fen.title('Snake game')
        self.heiht = (game.height + 2) * posSize
        self.width = (game.width + 2) * posSize
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

        self.drawBorder(0, 0)
        for column in range(1, self.game.width + 2):
            if self.game.posState(column - 1, -1) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(column, 0)
            else:
                self.drawBorder(column, 0)
        
        for line in range(self.game.height):
            if self.game.posState(-1, line) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(0, line + 1)
            else:
                self.drawBorder(0, line + 1)
            
            for column in range(self.game.width):
                self.drawGamePos(column, line)       
            
            if self.game.posState(self.game.width, line) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(self.game.width + 1, line + 1)
            else:
                self.drawBorder(self.game.width + 1, line + 1)

        
        self.drawBorder(0, self.game.height + 1)
        for column in range(1, self.game.width + 2):
            if self.game.posState(column - 1, self.game.height) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(column, self.game.height + 1)
            else:
                self.drawBorder(column, self.game.height + 1)
    
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