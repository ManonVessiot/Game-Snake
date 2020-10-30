from tkinter import Tk, Canvas
from tkinter.ttk import Style, Button
from PIL import ImageTk
from PIL import Image
import random
import math
from Move import Move

# draw snake game in console

class DrawWithTkinter_Texture:
    # constructor
    def __init__(self, game, posSize, secs):
        self.game = game
        self.posSize = posSize
        self.secs = int(secs * 250)
        self.reseting = False
        self.path = "/home/manon/Documents/Projects/MyProjects/python/SnakeGame/img/"

        self.grass = "grass.png"
        self.grassTexture = None

        self.food = ["Foods/food1.png", "Foods/food2.png", "Foods/food3.png", "Foods/food4.png", "Foods/food5.png", "Foods/food6.png"]
        self.foodTexture = []

        self.rock = ["Rocks/rock1.png", "Rocks/rock2.png", "Rocks/rock3.png", "Rocks/rock4.png"]
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

        self.buttonHeight = 30

        self.fen.geometry(str(max(self.width, 180)) + "x" + str(self.heiht + self.buttonHeight))
        self.fen.configure(bg='white')

        self.canvas = Canvas(self.fen, width=self.width, height=self.heiht)
        self.canvasButton = Canvas(self.fen, width=self.width, height=self.buttonHeight)

        style = Style() 
        style.configure('Quit.TButton', font = ('calibri', 10, 'bold'), foreground = 'red') 
        style.configure('Retry.TButton', font = ('calibri', 10, 'bold'), foreground = 'green') 

        Button(self.canvasButton, text ="Quit", style = 'Quit.TButton', command = self.game.stop).pack(side="right")
        Button(self.canvasButton, text ="Retry", style = 'Retry.TButton', command = self.reset).pack(side="left")
        self.canvasButton.pack(side="bottom")

    def reset(self):
        self.game.reset()
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

        for i in range(len(self.food)):
            self.foodTexture.append(ImageTk.PhotoImage(Image.open(self.path + self.food[i]).resize((self.posSize, self.posSize))))

        for i in range(len(self.rock)):
            self.rockTexture.append(ImageTk.PhotoImage(Image.open(self.path + self.rock[i]).resize((self.posSize, self.posSize))))
        
        #Border
        if self.game.border:
            for line in range(self.game.height + 2):
                if line == 0 or line == self.game.height + 1:
                    column = 0
                    while column < self.game.width + 2:
                        self.rocksIndex.append(random.randrange(0, len(self.rockTexture)))
                        column +=1
                else:
                    self.rocksIndex.append(random.randrange(0, len(self.rockTexture)))
                    self.rocksIndex.append(random.randrange(0, len(self.rockTexture)))

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
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        index = 0
        if x == 0:
            index = y
        elif x == self.game.height + 1:
            index = self.game.height + 2 + 2 * self.game.width + y
        else:
            index = self.game.height + 2 + 2 * (x - 1)
            if y == 0:
                index += 1
            else: 
                index +=2

        if index >= len(self.rocksIndex):
            print("x, y = " + str(x) + ", " + str(y))
            print("len(self.rocksIndex) = " + str(len(self.rocksIndex)))
            print("index = " + str(index))
            index = 0
        self.canvas.create_image(xCorner, yCorner, image = self.rockTexture[self.rocksIndex[index]], anchor = "nw")

    def drawSnake(self, x, y, state):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_image(xCorner, yCorner, image = self.snakeTexture[state], anchor = "nw")

    def drawSnakeHeadDead(self, x, y, state):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_image(xCorner, yCorner, image = self.snakeTexture[state], anchor = "nw")

    def drawFood(self, x, y):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        borderLimit = 0
        if self.game.border:
            borderLimit = 1

        index = (self.game.food.randomNum + int(math.tan(self.game.food.numbers[self.game.food.positions.index((x-borderLimit, y-borderLimit))]))) % len(self.foodTexture)
        self.canvas.create_image(xCorner, yCorner, image = self.foodTexture[index], anchor = "nw")

    def drawEmpty(self, x, y):
        xCorner = x * self.posSize
        yCorner = y * self.posSize
        self.canvas.create_image(xCorner, yCorner, image = self.grassTexture, anchor = "nw")

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
            if i == 0:
                state = self.stateOfSnake(i, 0)
            elif i == len(self.game.snake.body)-1:
                state = self.stateOfSnake(i, 2)
            else:
                state = self.stateOfSnake(i, 1)
            
            self.drawSnake(bodyPart[0]+borderPart, bodyPart[1]+borderPart, state)

        
    
    # draw position of grid according to it state
    def drawGamePos(self, x, y):
        if self.game.posState(x, y) == self.game.PositionState.EMPTY:
            self.drawEmpty(x + 1, y + 1)
        if self.game.posState(x, y) == self.game.PositionState.SNAKE or self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
            if self.game.dead and self.game.posState(x, y) == self.game.PositionState.SNAKE_HEAD:
                self.drawSnakeHeadDead(x + 1, y + 1, 0)
            else:
                self.drawSnake(x + 1, y + 1, -1)
        if self.game.posState(x, y) == self.game.PositionState.FOOD:
            self.drawFood(x + 1, y + 1)

    def stateOfSnake(self, i, part):
        diffs = self.game.snake.getDiffsWithNeighbours(i)
        if diffs != None:
            if (part == -1 or part == 0) and diffs[0] == None and diffs[1] != None:
                #head rotation depend on diff of the neighbour ; state in (0, 1, 2, 3)
                if diffs[1] == (0, -1):
                    return 0
                if diffs[1] == (-1, 0):
                    return 1
                if diffs[1] == (0, 1):
                    return 2
                if diffs[1] == (1, 0):
                    return 3
            if (part == -1 or part == 2) and diffs[0] != None and diffs[1] == None:
                #queue rotation depend on diff of the neighbour ; state in (10, 11, 12, 13)
                if diffs[0] == (0, 1):
                    return 10
                if diffs[0] == (1, 0):
                    return 11
                if diffs[0] == (0, -1):
                    return 12
                if diffs[0] == (-1, 0):
                    return 13
            
            if diffs[0] != None and diffs[1] != None:
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
            print("stateOfSnake ???????????")
            return 0

