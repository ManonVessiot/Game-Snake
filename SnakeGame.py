import random
import time

from Move import Move
from Snake import Snake
from Food import Food

from enum import Enum

# manage snake game

class SnakeGame:
    # constructor
    def __init__(self, width, height, secs, border):
        self.width = width
        self.height = height
        self.secs = secs

        self.playing = True
        self.reseting = False
        self.border = border

        self.buildGrid()
        
        self.move = Move()

        self.snake = Snake(width, height, border)
        self.food = Food(width, height, self.snake)
        self.score = 0

    def play(self):
        while self.playing:
            self.reseting = False

            while self.playing and not self.isMoving():
                time.sleep(self.secs)

            while self.playing and self.isMoving():
                time.sleep(self.secs)
                self.moveSnake()

            while self.playing and not self.reseting:
                time.sleep(self.secs)    
        print("stop playing")


    def stop(self):
        self.playing = False

    def reset(self):
        self.move = Move()
        time.sleep(self.secs)
        
        self.buildGrid()
        
        self.move = Move()
        self.snake = Snake(self.width, self.height, self.border)
        self.food = Food(self.width, self.height, self.snake)
        self.score = 0

        self.reseting = True

    def isMoving(self):
        return self.move.isMoving()

    # return len of snake body
    def lenOfSnake(self):
        return self.snake.lenOfBody()

    # build grid for game
    def buildGrid(self):
        addBorder = 0
        if self.border:
            addBorder = 2
        self.grid = [[]] * (self.height + addBorder)
        for line in range(self.height + addBorder):
            self.grid[line] = [0] * (self.width + addBorder)

        if self.border:
            self.buildGridBorder()

    # build grid border
    def buildGridBorder(self):
        for line in range(self.height + 2):
            for column in range(self.width + 2):
                if line == 0 or line == self.height + 1 or column == 0 or column == self.width + 1:
                    self.grid[line][column] = -1

    def changeMoveOfSnake(self, newMove):
        turnBack = self.snake.lenOfBody() == 1
        self.move.changeMove(newMove, turnBack)


    # move snake
    def moveSnake(self):        
        movement = self.move.getMove()
        
        if self.snake.move(movement):
            head = self.snake.head()
            scoreFood = self.food.eatFood(head[0], head[1])
            if scoreFood > 0:
                self.score += 1
                self.snake.addPArt(movement, scoreFood)

            return True
        
        self.move.stop()
        return False