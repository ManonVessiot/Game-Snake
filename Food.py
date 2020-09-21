import random

from Snake import Snake

class Food:
    def __init__(self, width, height, snake):
        self.width = width
        self.height = height
        self.snake = snake

        self.foodNumberSinceStart = 0

        self.positions = []
        self.scores = []
        self.createFood()
        print("Food")
        print(self.positions)

    def createFood(self):
        isSnake = True
        while isSnake:
            x = random.randrange(0, self.width)
            y = random.randrange(0, self.height)
            if not self.snake.isSnake(x, y) and (x, y) not in self.positions:
                isSnake = False

        self.foodNumberSinceStart += 1
        self.positions.append((x, y))
        self.scores.append(self.createScore())

    def createScore(self):
        mini = 3
        maxi = 10
        return random.randrange(mini, max(mini + 1, maxi - self.foodNumberSinceStart))

    def eatFood(self, x, y):
        score = 0
        if self.isFood(x, y):
            i = self.positions.index((x, y))
            score = self.scores[i]
            self.positions.remove((x, y))
            self.scores = self.scores[:i] + self.scores[i+1:]
            self.createFood()
        return score

    def isFood(self, x, y):
        return (x, y) in self.positions