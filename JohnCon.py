import sys
import turtle
import random
from PIL import Image
from scipy import misc
import numpy as np
import time

class LifeBoard:
    """Encapsulates a Life board

    Attributes:
    xsize, ysize : horizontal and vertical size of the board
    state : set containing (x,y) coordinates for live cells.

    Methods:
    display(update_board) -- Display the state of the board on-screen.
    erase() -- clear the entire board
    makeRandom() -- fill the board randomly
    set(x,y) -- set the given cell to Live; doesn't refresh the screen
    toggle(x,y) -- change the given cell from live to dead, or vice
                   versa, and refresh the screen display

    """
    def __init__(self, xsize, ysize, c, color, BIRTH_NUM, Smin_NUM, Smax_NUM):
        """Create a new LifeBoard instance.

        scr -- curses screen object to use for display
        char -- character used to render live cells (default: '*')
        """
        self.CELL_SIZE = c              # Measured in pixels
        self.COLOR = color

        self.start = time.time()

        self.state = set()
        self.xsize, self.ysize = xsize, ysize

        self.BIRTH_NUM = BIRTH_NUM
        self.Smin_NUM = Smin_NUM
        self.Smax_NUM = Smax_NUM

    def is_legal(self, x, y):
        "Returns true if the x,y coordinates are legal for this board."
        return (0 <= x < self.xsize) and (0 <= y < self.ysize)

    def set(self, x, y):
        """Set a cell to the live state."""
        if not self.is_legal(x, y):
            raise ValueError("Coordinates {}, {} out of range 0..{}, 0..{}".format(
                    x, y, self.xsize, self.ysize))
                             
        key = (x, y)
        self.state.add(key)

    def makeRandom(self):
        "Fill the board with a random pattern"
        self.erase()
        for i in range(0, self.xsize):
            for j in range(0, self.ysize):
                if random.random() > 0.5:
                    self.set(i, j)

    def makeSpecific(self, FILE_NAME):
        "Fill the board with a specific pattern"
        startPic = misc.imread(FILE_NAME)
        l = startPic.shape[0]
        w = startPic.shape[1]
        #startPic = np.transpose(startPic,(1,0,2))
        #print(startPic.shape)
        self.erase()

        #print(self.xsize)
        #print(self.ysize)
        if l < self.ysize and w < self.xsize:
            if len(startPic.shape) == 2:
                for i in range(0, l):
                    for j in range(0, w):
                        if startPic[i][j] < 175:
                            self.set(j,l-i-1)
            elif startPic.shape[2] == 2:
                for i in range(0, l):
                    for j in range(0, w):
                        if startPic[i][j][2] > 150:
                            self.set(j,l-i-1)
            elif startPic.shape[2] == 3:
                for i in range(0, l):
                    for j in range(0, w):
                        if sum(startPic[i][j]) < 100:
                            self.set(j,l-i-1)
            else:
                for i in range(0, l):
                    for j in range(0, w):
                        if startPic[i][j][0] < 175 and startPic[i][j][3] > 50:
                            self.set(j,l-i-1)
        else:
            print("Could not conjure too large...")

    def toggle(self, x, y):
        """Toggle a cell's state between live and dead."""
        if not self.is_legal(x, y):
            raise ValueError("Coordinates {}, {} out of range 0..{}, 0..{}".format(
                    x, y, self.xsize, self.ysize))
        key = (x, y)
        if key in self.state:
            self.state.remove(key)
        else:
            self.state.add(key)

    def erase(self):
        """Clear the entire board."""
        self.state.clear()

    def step(self):
        "Compute one generation, updating the display."
        d = set()
        for i in range(self.xsize):
            x_range = range( max(0, i-1), min(self.xsize, i+2) )
            for j in range(self.ysize):
                s = 0
                live = ((i,j) in self.state)
                for yp in range( max(0, j-1), min(self.ysize, j+2) ):
                    for xp in x_range:
                        if (xp, yp) in self.state:
                            s += 1

                # Subtract the central cell's value; it doesn't count.
                s -= live             
                ##print(d)
                ##print(i, j, s, live)
                if s == self.BIRTH_NUM:
                    # Birth
                    d.add((i,j))
                elif s >= self.Smin_NUM and s <= self.Smax_NUM and live: 
                    # Survival
                    d.add((i,j))
                elif live:
                    # Death
                    pass

        self.state = d

    #
    # Display-related methods
    #

    def draw(self, x, y):
        "Update the cell (x,y) on the display."
        turtle.penup()
        key = (x, y)
        if key in self.state:
            turtle.setpos(x*self.CELL_SIZE, y*self.CELL_SIZE)
            if self.COLOR == "rainbow":
                turtle.color("#%06x" % random.randint(0x000008, 0xFFFFFF))
            elif self.COLOR == "green":
                turtle.color("green")
            elif self.COLOR == "red":
                turtle.color("red")
            else:
                turtle.color("white")
            turtle.pendown()
            turtle.setheading(0)
            turtle.begin_fill()
            for i in range(4):
                turtle.forward(self.CELL_SIZE-1)
                turtle.left(90)
            turtle.end_fill()
            
    def display(self):
        """Draw the whole board"""
        turtle.clear()
        for i in range(self.xsize):
            for j in range(self.ysize):
                self.draw(i, j)
        turtle.update()

class JohnCon:
    def __init__(self, c, color = "white", BIRTH_NUM = 3, Smin_NUM = 2, Smax_NUM = 2):
        """Encapsulates a new LifeBoard instance.

        scr -- curses screen object to use for display
        char -- character used to render live cells (default: '*')
        """
        self.CELL_SIZE = c
        self.COLOR = color

        self.BIRTH_NUM = BIRTH_NUM
        self.Smin_NUM = Smin_NUM
        self.Smax_NUM = Smax_NUM

    def display_help_window(self):
        from turtle import TK
        root = TK.Tk()
        frame = TK.Frame()
        canvas = TK.Canvas(root, width=300, height=200, bg="white")
        canvas.pack()
        help_screen = turtle.TurtleScreen(canvas)
        help_t = turtle.RawTurtle(help_screen)
        help_t.penup()
        help_t.hideturtle()
        help_t.speed('fastest')

        width, height = help_screen.screensize()
        line_height = 20
        y = height // 2 - 30
        for s in ("Click on cells to make them alive or dead.",
                "Key commands:",
                " E- Erase ",
                " R- Random ",
                " P- Upload Pic ",
                " S- Step ",
                " C- Loop ",
                " Q- Quit "):
            help_t.setpos(-(width / 2), y)
            help_t.write(s, font=('sans-serif', 14, 'normal'))
            y -= line_height
        

    def render(self,FILE_LIST, MONTAGE=False, MONTAGE_CYCLES=100, MONTAGE_STEPS=200, DISPLAY_WAIT=5):
        self.display_help_window()

        scr = turtle.Screen()
        turtle.mode('standard')
        scr.bgcolor("black")
        xsize, ysize = scr.screensize()
        xsize = int(xsize/2)
        ysize = int(ysize/2)
        #print(xsize,", ",ysize)
        turtle.setworldcoordinates(0, 0, xsize, ysize)

        turtle.hideturtle()
        turtle.speed('fastest')
        turtle.tracer(0, 0)
        turtle.penup()

        board = LifeBoard(xsize // self.CELL_SIZE, 1 + ysize // self.CELL_SIZE, self.CELL_SIZE, self.COLOR, self.BIRTH_NUM, self.Smin_NUM, self.Smax_NUM)

        # Set up mouse bindings
        def toggle(x, y):
            cell_x = x // self.CELL_SIZE
            cell_y = y // self.CELL_SIZE
            if board.is_legal(cell_x, cell_y):
                board.toggle(cell_x, cell_y)
                board.display()

        turtle.onscreenclick(turtle.listen)
        turtle.onscreenclick(toggle)

        board.makeRandom()
        board.display()

        # Set up key bindings
        def erase():
            board.erase()
            board.display()
        turtle.onkey(erase, 'e')

        def makeRandom():
            board.makeRandom()
            board.display()
        turtle.onkey(makeRandom, 'r')

        def makeSpecific():
            board.makeSpecific(FILE_LIST[0])
            board.display()
        turtle.onkey(makeSpecific, 'p')

        turtle.onkey(sys.exit, 'q')

        # Set up keys for performing generation steps, either one-at-a-time or not.
        continuous = False
        def step_once():
            nonlocal continuous
            continuous = False
            perform_step()

        def step_continuous():
            nonlocal continuous
            continuous = True
            perform_step()

        def perform_step():
            board.step()
            board.display()
            # In continuous mode, we set a timer to display another generation
            # after 25 millisenconds.
            if continuous:
                turtle.ontimer(perform_step, 25)

        turtle.onkey(step_once, 's')
        turtle.onkey(step_continuous, 'c')
        if MONTAGE:
            for i in range(MONTAGE_CYCLES):
                for filename in FILE_LIST:
                    board.makeSpecific(filename)
                    board.display()
                    time.sleep(DISPLAY_WAIT)
                    for i in range(MONTAGE_STEPS):
                        step_once()
                        time.sleep(0.025)

        # Enter the Tk main loop
        turtle.listen()
        turtle.mainloop()
