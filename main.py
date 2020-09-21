import random
import time
import sys
import os
from pynput import keyboard
import threading

from Movement import Movement
from SnakeGame import SnakeGame
from DrawInConsole import DrawInConsole
from DrawWithTkinter import DrawWithTkinter

def play():
    global width
    global height
    global secs
    global moveRef
    global playingRef
    global game


    while moveRef[0] == Movement.NONE:
        #print("waiting for moveRef[0]")
        time.sleep(secs)

    #print("start playing")
    playingRef[0] = True
    while playingRef[0]:
        time.sleep(secs)
        playingRef[0] = playingTurn(game)
  #  print("stop playingRef[0]")

# playing a turn in snake (make a move)
def playingTurn(game):
    global moveRef

   # print("playing")
    
    playing = game.moveSnake(moveRef[0])
    return playing

# draw game
def draw(drawer):
    global moveRef
    global playingRef
    global secs

    drawer.draw(moveRef, playingRef, game)


# change move on key press
def moveEvents():
    global moveRef
    global playingRef

    while playingRef[0]:
        # The event listener will be running in this block
        with keyboard.Events() as events:
            # Block at most one second
            event = events.get()
            if event is not None and isinstance(event, keyboard.Events.Press):
                if event.key == keyboard.Key.left:
                    moveRef[0] = Movement.LEFT
                elif event.key == keyboard.Key.up:
                    moveRef[0] = Movement.UP
                elif event.key == keyboard.Key.right:
                    moveRef[0] = Movement.RIGHT
                elif event.key == keyboard.Key.down:
                    moveRef[0] = Movement.DOWN

# stop program
def stopProgram():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

# globals variables
posSize = 25
width = 40
height = 20
secs = 0.15
move = Movement.NONE
moveRef = [move]
playing = True
playingRef = [playing]
game = SnakeGame(width, height)
drawMode = 2

if __name__ == '__main__':
    try:
        # change move in thread
        moveThread = threading.Thread(target=moveEvents, args=())
        moveThread.start()

        # play in thread
        playThread = threading.Thread(target=play, args=())
        playThread.start()

        if drawMode == 1:
            # draw console
            drawerConsole = DrawInConsole(game, secs)
            draw(drawerConsole)
        else:
            # draw console
            drawerTk = DrawWithTkinter(game, posSize, secs)
            draw(drawerTk)

    except KeyboardInterrupt:
        print('\nInterrupted')
        stopProgram()