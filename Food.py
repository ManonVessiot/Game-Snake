import random

# mange food in grid

class Food:
    # constructor
    def __init__(self, width, height, snake):
        self._width = width
        self._height = height
        self._snake = snake

        self._foodNumberSinceStart = 0

        self.positions = []
        self.scores = []
        self._createFood()

    # create food
    def _createFood(self):
        isSnake = True
        while isSnake:
            x = random.randrange(0, self._width)
            y = random.randrange(0, self._height)
            if not self._snake.isSnake(x, y, False) and (x, y) not in self.positions:
                isSnake = False

        self._foodNumberSinceStart += 1
        self.positions.append((x, y))
        self.scores.append(self._createScore())

    # create score or food
    def _createScore(self):
        mini = 3
        maxi = 10
        score = random.randrange(mini, max(mini + 1, maxi - self._foodNumberSinceStart))
        print("new score created : " + str(score))
        return score

    # snake try to eat where his head is
    def eatFood(self, x, y):
        score = 0
        if self.isFood(x, y):
            i = self.positions.index((x, y))
            score = self.scores[i]
            self.positions.remove((x, y))
            self.scores = self.scores[:i] + self.scores[i+1:]
            self._createFood()
        return score

    # check if pos si food
    def isFood(self, x, y):
        return (x, y) in self.positions