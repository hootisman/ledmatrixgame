import sys
import os
import readchar
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from threading import Thread, Lock
from Matrixbase import MatrixBase
from rgbmatrix import graphics
from enum import Enum

running = True
gamespeed = 0.05
snakecol = graphics.Color(255,255,0)


class Segment(object):
    def __init__(self, x, y, length, seg_dir):
        """
        params:
        x -- x position of line end position
        y -- y position of line end position
        """
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
        """draws the segment"""
        global snakecol

        (back_x,back_y) = self.get_back_pos()

        graphics.DrawLine(matrix, back_x, back_y, self.x, self.y, snakecol)

    def move(self):
        """internal movement of segment"""
        global gamespeed
        self.len = self.len - gamespeed


class Snake(object):
    class Direction(Enum):
        UP = 1
        DOWN = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self):
        #total length of snake
        self.snake_len = 4

        self.head = Segment(20, 20, self.snake_len, Snake.Direction.DOWN)
        self.segments = []
        
        #seperate user input thread
        self.input_t = Thread(target=self.user_input)
        self.input_t.start()

    def move(self, matrix):
        global gamespeed
        
        #draw head
        match self.head.dir:
            case Snake.Direction.UP:
                self.head.y = self.head.y - gamespeed

            case Snake.Direction.DOWN:
                self.head.y = self.head.y + gamespeed

            case Snake.Direction.LEFT:
                self.head.x = self.head.x - gamespeed

            case Snake.Direction.RIGHT:
                self.head.x = self.head.x + gamespeed
        
        if self.head.len <= self.snake_len:
            self.head.len = self.head.len + gamespeed
    
        #move each segment
        for seg in self.segments:
            if seg.len <= 0:
                self.segments.pop(0)
            else:
                seg.move()

    def draw(self, matrix):
        #draw head
        self.head.draw(matrix)

        #draw each segment
        for seg in self.segments:
            seg.draw(matrix)
    
    def invalid_move(self, direction):
        """
        returns move that snake cannot do depending on direction parameter
        """
        result = None
        match direction:
            case Snake.Direction.UP:
                result = Snake.Direction.DOWN
            case Snake.Direction.DOWN:
                result = Snake.Direction.UP
            case Snake.Direction.LEFT:
                result = Snake.Direction.DOWN
            case Snake.Direction.UP:
                result = Snake.Direction.DOWN

        return result

    
    def new_segment(self):
        seg = Segment(self.head.x, self.head.y, self.head.len - 1, self.head.dir)
        self.segments.append(seg)
        
        self.head.len = 1

        print("new seg" )

    
    def user_input(self):
        """
        waits for key press and processes through match statement

        *runs on seperate thread*
        """
        global running

        while running:
            key = readchar.readkey()
            match key:
                case 'w':
                    if self.head.dir != Snake.Direction.UP and self.head.dir != Snake.Direction.DOWN:
                        self.new_segment()
                        self.head.dir = Snake.Direction.UP
                        self.head.y = self.head.y - 1   #offset head
                case 's':
                    if self.head.dir != Snake.Direction.DOWN and self.head.dir != Snake.Direction.UP:
                        self.new_segment()
                        self.head.dir = Snake.Direction.DOWN
                        self.head.y = self.head.y + 1   #offset head
                case 'a':
                    if self.head.dir != Snake.Direction.LEFT and self.head.dir != Snake.Direction.RIGHT:
                        self.new_segment()
                        self.head.dir = Snake.Direction.LEFT
                        self.head.x = self.head.x - 1   #offset head
                case 'd':
                    if self.head.dir != Snake.Direction.RIGHT and self.head.dir != Snake.Direction.LEFT:
                        self.new_segment()
                        self.head.dir = Snake.Direction.RIGHT
                        self.head.x = self.head.x + 1   #offset head
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
            snake.draw(self.matrix)

            #self.usleep(100000)


            canvas = self.matrix.SwapOnVSync(canvas)
            
# Main function
if __name__ == "__main__":
    #input_t = Thread(target=user_input)
    #input_t.start()

    simple_square = LEDGame()
    if (not simple_square.process()):
        simple_square.print_help()

