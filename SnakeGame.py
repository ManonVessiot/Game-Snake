import random

from Movement import Movement
from Snake import Snake
from Food import Food

from enum import Enum


class SnakeGame:
    class PositionState(Enum):
        EMPTY = 0,
        SNAKE = 1,
        FOOD = 2,

    # constructor
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = self.buildGrid()
        
        self.move = Movement.NONE
        self.snake = Snake(width, height)
        self.food = Food(width, height, self.snake)
        self.score = 0
        print("SnakeGame")

    
    def buildGrid(self):
        grid = [[]] * self.height
        for line in range(self.height):
            grid[line] = [0] * self.width
        return grid

    def posState(self, x, y):
        if self.snake.isSnake(x, y):
            return self.PositionState.SNAKE
        elif self.food.isFood(x, y):
            return self.PositionState.FOOD
        else:
            return self.PositionState.EMPTY

    def draw(self, playing):
        verticalBorder = "#"
        horizontalBorder = "#"

        head = self.snake.head()

        print("")
        print(horizontalBorder, end = "")
        for line in range(1, self.width + 2):
            if head[1] == -1 and head[0] == line - 1:
                print(horizontalBorder + "X", end = "")
            else:
                print(horizontalBorder + horizontalBorder, end = "")
        print("")

        for line in range(self.height):
            if head[0] == -1 and head[1] == line:
                print("X", end = " ")
            else:
                print(verticalBorder, end = " ")
            for column in range(self.width):
                print(self.drawPos(column, line, playing), end = " ")            
            
            if head[0] == self.width and head[1] == line:
                print("X")
            else:
                print(verticalBorder)
        
        print(horizontalBorder, end = "")
        for line in range(1, self.width + 2):
            if head[1] == self.height and head[0] == line - 1:
                print(horizontalBorder + "X", end = "")
            else:
                print(horizontalBorder + horizontalBorder, end = "")
        print("")

    def drawPos(self, x, y, playing):
        if self.posState(x, y) == self.PositionState.EMPTY:
            return "."
        if self.posState(x, y) == self.PositionState.SNAKE:
            if not playing and self.snake.head() == (x, y):
                return "X"
            return "x"
        if self.posState(x, y) == self.PositionState.FOOD:
            return "o"

    def moveSnake(self, newMove):
        movement = (0, 0)
        if newMove == Movement.DOWN and (len(self.snake.body) == 1 or self.move != Movement.UP):
            movement = (0, 1)
            self.move = newMove
        elif newMove == Movement.LEFT and (len(self.snake.body) == 1 or self.move != Movement.RIGHT):
            movement = (-1, 0)
            self.move = newMove
        elif newMove == Movement.UP and (len(self.snake.body) == 1 or self.move != Movement.DOWN):
            movement = (0, -1)
            self.move = newMove
        elif newMove == Movement.RIGHT and (len(self.snake.body) == 1 or self.move != Movement.LEFT):
            movement = (1, 0)
            self.move = newMove
        else:
            movement = self.getMove(self.move)
        
        if self.snake.move(movement):
            head = self.snake.head()
            scoreFood = self.food.eatFood(head[0], head[1])
            if scoreFood > 0:
                self.snake.addPArt(movement, scoreFood)

            return True
        return False

    def getMove(self, move):
        if move == Movement.DOWN:
            return (0, 1)
        elif move == Movement.LEFT:
            return(-1, 0)
        elif move == Movement.UP:
            return (0, -1)
        elif move == Movement.RIGHT:
            return (1, 0)
        else:
            return (0, 0)