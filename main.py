import random
import time
import sys
import os
from pynput import keyboard
import threading

from Move import Move
from SnakeGame import SnakeGame
from DrawInConsole import DrawInConsole
from DrawWithTkinter import DrawWithTkinter
from DrawWithTkinter_Texture import DrawWithTkinter_Texture

# change move on key press
def moveEvents(game, drawer, secs):
    while game.playing:
        # The event listener will be running in this block
        with keyboard.Events() as events:
            # Block at most one second
            print("before event")
            event = events.get(secs * 100)
            print("after event")
            if event is not None and isinstance(event, keyboard.Events.Press):
                if event.key == keyboard.Key.left:
                    game.changeMoveOfSnake(Move.Movement.LEFT)
                elif event.key == keyboard.Key.up:
                    game.changeMoveOfSnake(Move.Movement.UP)
                elif event.key == keyboard.Key.right:
                    game.changeMoveOfSnake(Move.Movement.RIGHT)
                elif event.key == keyboard.Key.down:
                    game.changeMoveOfSnake(Move.Movement.DOWN)
                elif event.key == keyboard.Key.backspace:
                    print("reset")
                    game.reset()
                    drawer.reset()
                elif event.key == keyboard.Key.esc:
                    print("stop")
                    game.stop()
                else:
                    print("event.key : " + str(event.key))
            print("end event")

    print("stop moveEvents")

# stop program
def stopProgram():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)



def format():
    print("\nWrong use !")
    print("python3 main.py width height secs border drawMode (posSize)")
    print("   - width, height : size of game in number of cells")
    print("   - secs : seconds between frame")
    print("   - drawMode :")
    print("      - 0 : interface in console")
    print("      - 1 : interface with tkinter")
    print("   - border :")
    print("      - 0 : snake can go to the right area by passing by the left side")
    print("      - 1 : border kill snake")
    print("   - posSize : size of a cell (drawMode = 1) ")



if __name__ == '__main__':
    try:
        # game variables
        print("sys.argv[:] : " + str(sys.argv[:]))
        if len(sys.argv) >= 6:
            width = int(sys.argv[1])
            height = int(sys.argv[2])
            secs = float(sys.argv[3])

            drawMode = int(sys.argv[4])

            border = int(sys.argv[5])

            game = SnakeGame(width, height, secs, border==1)

            if drawMode == 0:
                # draw console
                drawer = DrawInConsole(game, secs)
            elif drawMode == 1:
                # draw tkinter
                if len(sys.argv) >= 7:
                    posSize = int(sys.argv[6])
                else:
                    posSize = 50
                
                drawer = DrawWithTkinter(game, posSize, secs)
            elif drawMode == 2:
                # draw tkinter with texture
                if len(sys.argv) >= 7:
                    posSize = int(sys.argv[6])
                else:
                    posSize = 50
                
                drawer = DrawWithTkinter_Texture(game, posSize, secs)
            else:
                format()
                stopProgram()

            # change move in thread
            moveThread = threading.Thread(target=moveEvents, args=(game,drawer,secs,))
            moveThread.start()

            # play in thread
            playThread = threading.Thread(target=game.play, args=())
            playThread.start()

            drawer.draw()
            stopProgram()
        else:
            format()
            stopProgram()

    except KeyboardInterrupt:
        print('\nInterrupted')
        stopProgram()