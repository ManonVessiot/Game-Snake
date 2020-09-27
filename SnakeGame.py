import random
import time

from Move import Move
from Snake import Snake
from Food import Food

from enum import Enum

# manage snake game

class SnakeGame:
    class PositionState(Enum):
        EMPTY = 0,
        SNAKE = 1,
        SNAKE_HEAD = 2,
        FOOD = 3,

    # constructor
    def __init__(self, width, height, secs):
        self.width = width
        self.height = height
        self.secs = secs

        self.playing = True
        self.dead = False
        self.reseting = False

        self.grid = self.buildGrid()
        
        self.move = Move()

        self.snake = Snake(width, height)

        part2Move = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.snake.addPArt(part2Move[random.randrange(0, 4)], 1)
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
            self.dead = True

            while self.playing and not self.reseting:
                time.sleep(self.secs)
            self.dead = False        
        print("stop playing")


    def stop(self):
        self.playing = False

    def reset(self):
        self.grid = self.buildGrid()
        
        self.move = Move()
        self.snake = Snake(self.width, self.height)
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
        grid = [[]] * self.height
        for line in range(self.height):
            grid[line] = [0] * self.width
        return grid

    # return state of posiion in grid
    def posState(self, x, y):
        if self.snake.isSnake(x, y):
            head = self.snake.head()
            if head[0] == x and head[1] == y:
                return self.PositionState.SNAKE_HEAD
            return self.PositionState.SNAKE
        elif self.food.isFood(x, y):
            return self.PositionState.FOOD
        else:
            return self.PositionState.EMPTY

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