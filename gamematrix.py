import sys
import os
import readchar
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from threading import Thread, Lock
from Matrixbase import MatrixBase
from rgbmatrix import graphics
from enum import Enum

running = True

class Snake(object):
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self):
        self.x_pos = 32
        self.y_pos = 32

        self.input_t = Thread(target=self.user_input)
        self.input_t.start()

    def user_input(self):
        global running

        while running:
            key = readchar.readkey()
            match key:
                case 'a':
                    self.x_pos = self.x_pos - 1
                case 'd':
                    self.x_pos = self.x_pos + 1
                case 'w':
                    self.y_pos = self.y_pos - 1
                case 's':
                    self.y_pos = self.y_pos + 1
                case 'q' | 0x1B | 0x04:
                    running = False
                case _:
                    pass
            print(key)


class LEDGame(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(LEDGame, self).__init__(*args, **kwargs)
    
    def run(self):
        global running
        
        snake = Snake()

        canvas = self.matrix.CreateFrameCanvas()

        paccol = graphics.Color(255,255,0)
        while running:
            self.matrix.Clear()
            #graphics.DrawCircle(self.matrix, snake.x_pos, snake.y_pos, 2, paccol)
            graphics.DrawLine(self.matrix, snake.x_pos, snake.y_pos -2, snake.x_pos, snake.y_pos, paccol)


            snake.y_pos = -6 if snake.y_pos >= 68 else snake.y_pos + 0.05


            canvas = self.matrix.SwapOnVSync(canvas)
            
# Main function
if __name__ == "__main__":
    #input_t = Thread(target=user_input)
    #input_t.start()

    simple_square = LEDGame()
    if (not simple_square.process()):
        simple_square.print_help()

