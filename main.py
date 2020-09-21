import random
import time
import sys
import os
from pynput import keyboard
import threading

from Movement import Movement
from SnakeGame import SnakeGame

def playInConsole():
    global width
    global height
    global secs
    global move
    global playing

    game = SnakeGame(width, height)
    game.draw(True)

    while move == Movement.NONE:
        time.sleep(secs)

    playing = True
    while playing:
        time.sleep(secs)
        playing = playingTurn(game)
        game.draw(playing)

def playingTurn(game):
    global move
    
    playing = game.moveSnake(move)
    return playing

def moveEvents():
    global move
    global playing

    while playing:
        # The event listener will be running in this block
        with keyboard.Events() as events:
            # Block at most one second
            event = events.get()
            if event is not None and isinstance(event, keyboard.Events.Press):
                if event.key == keyboard.Key.left:
                    move = Movement.LEFT
                elif event.key == keyboard.Key.up:
                    move = Movement.UP
                elif event.key == keyboard.Key.right:
                    move = Movement.RIGHT
                elif event.key == keyboard.Key.down:
                    move = Movement.DOWN

width = 20
height = 10
secs = 0.25
move = Movement.NONE
playing = True

if __name__ == '__main__':
    try:
        x = threading.Thread(target=moveEvents, args=())
        x.start()
        
        playInConsole()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)