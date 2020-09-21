import random

from Movement import Movement
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
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._grid = self.buildGrid()
        
        self._move = Movement.NONE
        self._snake = Snake(width, height)
        self._food = Food(width, height, self._snake)
        self.score = 0

    # return len of snake body
    def lenOfSnake(self):
        return self._snake.lenOfBody()

    # build grid for game
    def buildGrid(self):
        grid = [[]] * self.height
        for line in range(self.height):
            grid[line] = [0] * self.width
        return grid

    # return state of posiion in grid
    def posState(self, x, y):
        if self._snake.isSnake(x, y):
            head = self._snake.head()
            if head[0] == x and head[1] == y:
                return self.PositionState.SNAKE_HEAD
            return self.PositionState.SNAKE
        elif self._food.isFood(x, y):
            return self.PositionState.FOOD
        else:
            return self.PositionState.EMPTY

    # move snake
    def moveSnake(self, newMove):
        movement = (0, 0)
        if newMove == Movement.DOWN and (self._snake.lenOfBody() == 1 or self._move != Movement.UP):
            movement = (0, 1)
            self._move = newMove
        elif newMove == Movement.LEFT and (self._snake.lenOfBody() == 1 or self._move != Movement.RIGHT):
            movement = (-1, 0)
            self._move = newMove
        elif newMove == Movement.UP and (self._snake.lenOfBody() == 1 or self._move != Movement.DOWN):
            movement = (0, -1)
            self._move = newMove
        elif newMove == Movement.RIGHT and (self._snake.lenOfBody() == 1 or self._move != Movement.LEFT):
            movement = (1, 0)
            self._move = newMove
        else:
            movement = self.getMove(self._move)
        
        if self._snake.move(movement):
            head = self._snake.head()
            scoreFood = self._food.eatFood(head[0], head[1])
            if scoreFood > 0:
                self.score += 1
                self._snake.addPArt(movement, scoreFood)

            return True
        return False

    # return movement to do in the grid
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