import math

from foundrymatrix.base import MatrixBase
from foundrymatrix.input import MatrixUserInput
from random import randrange
from rgbmatrix import graphics
from enum import Enum

running = True
gamespeed = 1
snakecol = graphics.Color(255,255,0)

class Fruit(object):
    def __init__(self, color):
        self.color = color
        self.rand_pos()

    def draw(self, matrix):
        graphics.DrawLine(matrix, self.x, self.y, self.x, self.y, self.color)
        

    def rand_pos(self):
        self.x = randrange(60) + 4
        self.y = randrange(60) + 4
        
current_fruit = Fruit(graphics.Color(255,0,0))

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
        

    def get_back_pos(self, x, y):
        back_x = x
        back_y = y

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
        self.draw_pos(matrix, self.x, self.y)

    def draw_pos(self, matrix, x, y):
        global snakecol

        (back_x,back_y) = self.get_back_pos(x, y)

        graphics.DrawLine(matrix, math.floor(back_x), math.floor(back_y), math.floor(x), math.floor(y), snakecol)
        

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

    def up(self):
        if self.head.dir != Snake.Direction.UP and self.head.dir != Snake.Direction.DOWN:
            self.new_segment()
            self.head.dir = Snake.Direction.UP
            self.head.y = self.head.y - 1   #offset head
    def down(self):
        if self.head.dir != Snake.Direction.DOWN and self.head.dir != Snake.Direction.UP:
            self.new_segment()
            self.head.dir = Snake.Direction.DOWN
            self.head.y = self.head.y + 1   #offset head
    def left(self):
        if self.head.dir != Snake.Direction.LEFT and self.head.dir != Snake.Direction.RIGHT:
            self.new_segment()
            self.head.dir = Snake.Direction.LEFT
            self.head.x = self.head.x - 1   #offset head
    def right(self):
        if self.head.dir != Snake.Direction.RIGHT and self.head.dir != Snake.Direction.LEFT:
            self.new_segment()
            self.head.dir = Snake.Direction.RIGHT
            self.head.x = self.head.x + 1   #offset head

    def __init__(self):
        #total length of snake
        self.snake_len = 4

        #user input functions
        def stop():
            global running
            running = False
            self.input.exit()
        
        #user input
        self.input = MatrixUserInput()
        self.input.attach_key('q', stop)
        self.input.attach_key('w', self.up)
        self.input.attach_key('s', self.down)
        self.input.attach_key('a', self.left)
        self.input.attach_key('d', self.right)


        self.head = Segment(20, 20, self.snake_len, Snake.Direction.DOWN)
        self.segments = []

    def move(self, matrix):
        global gamespeed
        global current_fruit

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
       
        if self.head.x == current_fruit.x and self.head.y == current_fruit.y:
            #snake has eaten the fruit
            self.snake_len = self.snake_len + 1
            current_fruit.rand_pos()

        
        if len(self.segments) == 0:
            return
        
        seg = self.segments[0]

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
    
    def new_segment(self):
        seg = Segment(self.head.x, self.head.y, self.head.len - 1, self.head.dir)
        self.segments.append(seg)
        
        self.head.len = 1
    


class LEDGame(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(LEDGame, self).__init__(*args, **kwargs)
    
    def run(self):
        global running
        global current_fruit
        
        snake = Snake()

        #canvas = self.matrix.CreateFrameCanvas()

        paccol = graphics.Color(255,255,0)
        while running:

            current_fruit.draw(self.matrix)

            snake.move(self.matrix)
            snake.draw(self.matrix)

            self.usleep(100000)

            
            self.clear_screen()

        snake.input.exit()
            
# Main function
if __name__ == "__main__":

    simple_square = LEDGame()
    if (not simple_square.process()):
        simple_square.print_help()

