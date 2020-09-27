from tkinter import Tk, Canvas
from PIL import ImageTk
from PIL import Image
import random
from Move import Move

# draw snake game in console

class DrawWithTkinter_Texture:
    # constructor
    def __init__(self, game, posSize, secs):
        self.game = game
        self.posSize = posSize
        self.secs = int(secs * 250)
        self.reseting = False
        self.path = "/home/manon/Documents/Projects/MyProjects/SnakeGame_py/img/"

        self.grass = "grass.png"
        self.food = "food.png"
        self.snake = ["SnakePart/head.png", "SnakePart/body.png", "SnakePart/bodyTurnbis.png", "SnakePart/queue.png"]
        self.grassTexture = None
        self.foodTexture = None
        self.snakeTexture = []

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

        self.grassTexture = ImageTk.PhotoImage(Image.open(self.path + self.grass).resize((self.posSize, self.posSize)))
        self.foodTexture = ImageTk.PhotoImage(Image.open(self.path + self.food).resize((self.posSize, self.posSize)))

        for i in range(len(self.snake)):
            self.snakeTexture.append(ImageTk.PhotoImage(Image.open(self.path + self.snake[i]).resize((self.posSize, self.posSize))))
            if i != 1:
                for j in range(1, 4):
                    self.snakeTexture.append(ImageTk.PhotoImage(Image.open(self.path + self.snake[i]).resize((self.posSize, self.posSize)).rotate(angle=j * 90)))
            else:
                self.snakeTexture.append(ImageTk.PhotoImage(Image.open(self.path + self.snake[i]).resize((self.posSize, self.posSize)).rotate(angle=90)))
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
        self.drawEmpty(x, y)
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        state = self.stateOfSnake(x-1, y-1)
        self.canvas.create_image(xCorner, yCorner, image = self.snakeTexture[state], anchor = "nw")

    def drawSnakeHeadDead(self, x, y):
        self.drawSquare(x, y, "red", "red")
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_image(xCorner, yCorner, image = self.snakeTexture[self.stateOfSnake(x-1, y-1)], anchor = "nw")

    def drawFood(self, x, y):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_image(xCorner, yCorner, image = self.grassTexture, anchor = "nw")
        self.canvas.create_image(xCorner, yCorner, image = self.foodTexture, anchor = "nw")

    def drawEmpty(self, x, y):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_image(xCorner, yCorner, image = self.grassTexture, anchor = "nw")

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

    def stateOfSnake(self, x, y):
        diffs = self.game.snake.getDiffsWithNeighbours(x, y)
        if diffs != None:
            if diffs[0] == None:
                #head rotation depend on diff of the neighbour ; state in (0, 1, 2, 3)
                if diffs[1] == (0, -1):
                    return 0
                elif diffs[1] == (-1, 0):
                    return 1
                elif diffs[1] == (0, 1):
                    return 2
                elif diffs[1] == (1, 0):
                    return 3
            elif diffs[1] == None:
                #queue rotation depend on diff of the neighbour ; state in (10, 11, 12, 13)
                if diffs[0] == (0, 1):
                    return 10
                elif diffs[0] == (1, 0):
                    return 11
                elif diffs[0] == (0, -1):
                    return 12
                elif diffs[0] == (-1, 0):
                    return 13
            else:
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
        else:
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

