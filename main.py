import random
import time
import sys
import os
from pynput import keyboard

from Movement import Movement
from SnakeGame import SnakeGame

def trying():

    # The event listener will be running in this block
    with keyboard.Events() as events:
        # Block at most one second
        event = events.get(1.0)
        if event is None:
            print('You did not press a key within one second')
        else:
            print('Received event {}'.format(event))


def main():
    global move

    width = 20
    height = 10
    secs = 0.25

    game = SnakeGame(width, height)
    game.draw(True)

    while boucle(game):
        #time.sleep(secs)
        timeStart = time.time()
        timeToPass = secs
        while timeToPass > 0:
            # The event listener will be running in this block
            with keyboard.Events() as events:
                # Block at most one second
                event = events.get(secs)
                if event is not None and isinstance(event, keyboard.Events.Press):
                    if event.key == keyboard.Key.left:
                        move = Movement.LEFT
                    elif event.key == keyboard.Key.up:
                        move = Movement.UP
                    elif event.key == keyboard.Key.right:
                        move = Movement.RIGHT
                    elif event.key == keyboard.Key.down:
                        move = Movement.DOWN

            timePassed = time.time() - timeStart
            timeToPass -= timePassed

def boucle(game):
    global move
#    value = input("Move:\n")
#    move = Movement.NONE
#    if value == "l":
#        move = Movement.LEFT
#    elif value == "r":
#        move = Movement.RIGHT
#    elif value == "u":
#        move = Movement.UP
#    elif value == "d":
#        move = Movement.DOWN
#
    playing = game.moveSnake(move)
    game.draw(playing)
    return playing

#move = Movement.NONE
#main()

if __name__ == '__main__':
    try:
        move = Movement.NONE
        main()
    except KeyboardInterrupt:
        print('\nInterrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)