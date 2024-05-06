import sys
import os
import readchar
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from threading import Thread, Lock
from Matrixbase import MatrixBase
from rgbmatrix import graphics
from enum import Enum

running = True
x_pos = 32
y_pos = 32

def user_input():
    global running
    global x_pos
    global y_pos

    while running:
        key = readchar.readkey()
        match key:
            case 'a':
                x_pos = x_pos - 1
            case 'd':
                x_pos = x_pos + 1
            case 'w':
                y_pos = y_pos - 1
            case 's':
                y_pos = y_pos + 1
            case 'q' | 0x1B | 0x04:
                running = False
            case _:
                pass
        print(key)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class LEDGame(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(LEDGame, self).__init__(*args, **kwargs)
    
    def run(self):
        global running
        global x_pos
        global y_pos

        canvas = self.matrix.CreateFrameCanvas()

        paccol = graphics.Color(255,255,0)
        while running:
            self.matrix.Clear()
            #graphics.DrawCircle(self.matrix, x_pos, y_pos, 2, paccol)
            graphics.DrawLine(self.matrix, x_pos, y_pos -2, x_pos, y_pos, paccol)


            y_pos = -6 if y_pos >= 68 else y_pos + 0.05


            canvas = self.matrix.SwapOnVSync(canvas)
            
# Main function
if __name__ == "__main__":
    input_t = Thread(target=user_input)
    input_t.start()

    simple_square = LEDGame()
    if (not simple_square.process()):
        simple_square.print_help()

