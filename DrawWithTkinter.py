from tkinter import * 
import time 
import threading

from Movement import Movement
from SnakeGame import SnakeGame
# draw snake game in console

class DrawWithTkinter:
    # constructor
    def __init__(self, game, posSize, secs):
        self.game = game
        self.posSize = posSize
        self.secs = int(secs * 500)

        self.fen = Tk()
        self.fen.title('Snake game')
        self.heiht = (game.height + 2) * posSize
        self.width = (game.width + 2) * posSize
        self.fen.geometry(str(self.width) + "x" + str(self.heiht))

        self.canvas = Canvas(self.fen, width=self.width, height=self.heiht)

    def run(self):
        self.fen.mainloop()        

    def update(self, move, playing, game):
        if move[0] == Movement.NONE:
            self.fen.after(self.secs, self.update, move, playing, game)
        else:
            self.canvas.delete("all")

            self.drawGame(playing[0])
            self.canvas.pack(fill=X)
            if playing[0]:
                self.fen.after(self.secs, self.update, move, playing, game)
            else:        
                print("score : " + str(game.score))
                print("snake len : " + str(game.lenOfSnake()))



    def draw(self, move, playing, game):
        self.fen.after(self.secs, self.update, move, playing, game)
        self.drawGrid(playing[0])


    def drawGrid(self, playing):
        self.drawGame(playing)
        self.canvas.pack()
        self.run()

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

    def drawGame(self, playing):
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
                self.drawGamePos(column, line, playing)       
            
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
    def drawGamePos(self, x, y, playing):
        if self.game.posState(x, y) == self.game.PositionState.EMPTY:
            self.drawEmpty(x + 1, y + 1)
        if self.game.posState(x, y) == self.game.PositionState.SNAKE or self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
            if not playing and self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(x + 1, y + 1)
            else:
                self.drawSnake(x + 1, y + 1)
        if self.game.posState(x, y) == self.game.PositionState.FOOD:
            self.drawFood(x + 1, y + 1)