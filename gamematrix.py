import sys
import os
import readchar
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from threading import Thread, Lock
from Matrixbase import MatrixBase
from rgbmatrix import graphics
from enum import Enum

running = True

snakecol = graphics.Color(255,255,0)

class Snake(object):
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    class Segment(object):
        def __init__(self, x, y, length, seg_dir):
            self.x = x
            self.y = y
            self.len = length
            self.dir = seg_dir

        def get_back_pos(self):
            back_x = self.x
            back_y = self.y

            match self.dir:
                case Snake.Direction.UP:
                    back_y = back_y + self.len
                case Snake.Direction.DOWN:
                    back_y = back_y - self.len
                case Snake.Direction.LEFT:
                    back_x = back_x + self.len
                case Snake.Direction.RIGHT:
                    back_x = back_x - self.len
            
            return (back_x, back_y)

        def draw(self, matrix):
            global snakecol
            (back_x,back_y) = self.get_back_pos()

            graphics.DrawLine(matrix, back_x, back_y, self.x, self.y, snakecol)

        def move(self):
            self.len = self.len - 1

    def __init__(self):
        self.x_pos = 20
        self.y_pos = 20
        self.dir = Snake.Direction.DOWN
        self.speed = 0.05

        #length of the head segment
        self.headlen = 8

        #total length of snake
        self.len = 8

        self.head = Snake.Segment(self.x_pos, self.y_pos, self.len, self.dir)
        self.segments = []
        
        #seperate user input thread
        self.input_t = Thread(target=self.user_input)
        self.input_t.start()

    def move(self, matrix):
        match self.dir:
            case Snake.Direction.UP:
                self.y_pos = self.y_pos - self.speed

            case Snake.Direction.DOWN:
                self.y_pos = self.y_pos + self.speed

            case Snake.Direction.LEFT:
                self.x_pos = self.x_pos - self.speed

            case Snake.Direction.RIGHT:
                self.x_pos = self.x_pos + self.speed
        self.head.x = self.x_pos
        self.head.y = self.y_pos
        
        self.head.draw(matrix)

        self.move_segs()

        self.draw_segs(matrix)

    def move_segs(self):

        for seg in self.segments:
            seg.move()
            if seg.len <= 0:
                self.segments.pop(0)


    def draw_segs(self, matrix):
        for seg in self.segments:
            seg.draw(matrix)
    
    def new_segment(self):
        seg = Snake.Segment(self.x_pos, self.y_pos, self.headlen, self.dir)
        self.segments.append(seg)
        
        self.headlen = 1

    
    def user_input(self):
        global running

        while running:
            key = readchar.readkey()
            match key:
                case 'w':
                    self.new_segment()
                    self.dir = Snake.Direction.UP
                case 's':
                    self.new_segment()
                    self.dir = Snake.Direction.DOWN
                case 'a':
                    self.new_segment()
                    self.dir = Snake.Direction.LEFT
                case 'd':
                    self.new_segment()
                    self.dir = Snake.Direction.RIGHT
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
            #graphics.DrawLine(self.matrix, snake.x_pos, snake.y_pos, snake.x_pos, snake.y_pos, paccol)


            #snake.y_pos = -6 if snake.y_pos >= 68 else snake.y_pos + 0.05
            snake.move(self.matrix)

            #self.usleep(100000)


            canvas = self.matrix.SwapOnVSync(canvas)
            
# Main function
if __name__ == "__main__":
    #input_t = Thread(target=user_input)
    #input_t.start()

    simple_square = LEDGame()
    if (not simple_square.process()):
        simple_square.print_help()

