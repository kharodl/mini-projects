"""
Minesweeper

description: An implementation of Minesweeper using tkinter

basics: Click on a button to reveal a mine or a number. The number
    indicates the number of mines touching that button. To win, reveal
    all "safe" spots without triggering a mine. Avoid the mines.

scoring criteria: 1 point for every win, no penalty for losing

usage: Homework8.py [-h] [-d] [-v] {easy, medium, hard} [size]

positional arguments:
  {easy, medium, hard}      What difficulty level?
  size                      How many columns/rows in the grid?

optional arguments:
  -h, --help           Show this help message and exit
  -d, --debug          Enter Debug Mode and highlight mines
  -v, --verbose        Print details
"""

import argparse
import tkinter as tk


class GameApp:
    """
    MineSweeper - A tkinter implementation of Minesweeper

    Argument:
    parent (tkinter.Tk): the root window object
    difficulty (int): the difficulty of the game
    size (int): the size of the grid
    debug (boolean): whether debug mode is on or off

    Attributes:
    parent (tkinter.Tk): the root window object
    difficulty (int): the chance of mines
    size (int): the size of the grid
    highlight_mines (boolean): a flag for highlighting mines

    header (tkinter.Label): the label showing score and win/loss
    c (tkinter.Canvas): the widget defining the text
    cell_w (int): width of each cell on the given size grid
    cell_h (int): height of each cell on the given size grid
    mine_image (tkinter.PhotoImage): a mine image
    redo_image (tkinter.PhotoImage): a redo button image

    end_game (boolean): flag for game over state
    score (int): the number of games won in this session
    delay (int): ms to wait per mine in self.show_all_mines()
    buttons (lists): a list of rectangles on the grid
    coord_table (dict): a dictionary mapping rectangles to coords
    mine_coords (set): a set of coords of placed mines
    visited (set): a set of visited grid coordinates
    mine_count (int): number of active mines
    """

    def __init__(self, parent, difficulty, size, debug):
        parent.title('MineSweeper')
        self.parent = parent
        self.difficulty = difficulty
        self.size = size
        self.highlight_mines = debug
        self.mine_image = tk.PhotoImage(file="mine.gif")
        self.redo_image = tk.PhotoImage(file="redo.gif")

        self.header = tk.Label(parent, text='\nScore: 0',
                               bg='white', font=("Calibri", 16))
        self.header.grid(row=0, column=0, sticky='nesw')
        self.c = tk.Canvas(self.parent, width=500, height=500)
        self.c.grid(row=1, column=0)
        self.parent.update_idletasks()
        w = self.c.winfo_width()
        h = self.c.winfo_height()
        self.cell_w = w / self.size
        self.cell_h = h / self.size
        while self.mine_image.width() > self.cell_w:
            self.mine_image = self.mine_image.subsample(2)
        restart_button = tk.Button(parent, image=self.redo_image,
                                   command=self.restart)
        restart_button.grid(row=2, column=0, sticky='nesw')

        self.end_game = False
        self.score = 0
        self.delay = 0
        self.buttons = [[None for _ in range(self.size)]
                        for _ in range(self.size)]
        self.coord_table = {}
        self.build_grid()
        self.mine_coords = set()
        self.visited = set()
        self.mine_count = 0
        self.lay_mines()

    def restart(self):
        """
        Restarts the game
        """
        self.end_game = False
        self.c.delete('mine')
        self.c.delete('mine_num')
        self.header.configure(text='\nScore: ' + str(self.score))
        self.mine_coords.clear()
        self.visited.clear()
        self.mine_count = 0
        self.lay_mines()

    def build_grid(self):
        """
        Builds the initial grid of rectangles
        """
        for x in range(self.size):
            for y in range(self.size):
                button = self.c.create_rectangle(x*self.cell_w,
                                                 y*self.cell_h,
                                                 (x+1)*self.cell_w,
                                                 (y+1)*self.cell_h,
                                                 fill='white',
                                                 outline='black')
                self.coord_table[button] = (x, y)
                self.buttons[x][y] = button

    def lay_mines(self):
        """
        Initiate mine coordinates based on difficulty
        """
        import random
        for x in range(self.size):
            for y in range(self.size):
                self.c.itemconfigure(self.buttons[x][y], fill='white')
                if self.difficulty > random.randint(0, 9):
                    if self.highlight_mines:
                        self.c.itemconfigure(self.buttons[x][y], fill='yellow')
                    self.mine_coords.add((x, y))
                    self.mine_count += 1
        self.c.bind("<Button-1>", self.check_util)
        self.delay = int(1000/self.mine_count)

    def check_util(self, event):
        """
        Checks if clicked area is valid
        :param event: (event) the event passed by binding
        """
        if not self.end_game:
            element = self.c.find_closest(event.x, event.y)[0]
            if 'mine_num' not in self.c.gettags(element):
                coords = self.coord_table[element]
                self.check_mine(coords)

    def check_mine(self, coords, first_run=True):
        """
        Checks if the button clicked contains a mine
        :param coords: (tuple) coordinates of the button clicked
        :param first_run: (boolean) whether it is the first run
        """
        x, y = coords
        if not self.end_game:
            mine_num = 0
            for dx in (x-1, x, x+1):
                for dy in (y-1, y, y+1):
                    if 0 <= dx < self.size and 0 <= dy < self.size \
                            and (dx, dy) in self.mine_coords:
                        mine_num += 1
            self.visited.add(coords)
            if mine_num == 0:
                self.c.itemconfigure(self.buttons[x][y], fill='dark gray')
                self.find_frees(coords)
            elif coords in self.mine_coords:
                self.c.create_image(x * self.cell_w + self.cell_w / 2,
                                    y * self.cell_h + self.cell_w / 2,
                                    image=self.mine_image, tags='mine')
                self.end_game = True
                self.show_all_mines()
                self.header.configure(text='You Lost...\nScore: '
                                           + str(self.score))
            else:
                self.c.itemconfigure(self.buttons[x][y], fill='blue')
                self.c.create_text(x*self.cell_w + self.cell_w/2,
                                   y*self.cell_h + self.cell_w/2,
                                   text=mine_num, fill='white',
                                   tags='mine_num')
            if first_run and len(self.visited) == (self.size ** 2 -
                                                   self.mine_count):
                self.end_game = True
                self.show_all_mines()
                self.score += 1
                self.header.configure(text='You Won!\nScore: '
                                           + str(self.score))

    def find_frees(self, coords):
        """
        Opens up non mine spaces adjacent to the coords
        :param coords: (tuple) coordinates of the item clicked
        """
        x, y = coords
        for dx in (x - 1, x, x + 1):
            for dy in (y - 1, y, y + 1):
                if dx in range(0, self.size) and dy in range(0, self.size) \
                        and (dx, dy) not in self.mine_coords \
                        and (dx, dy) not in self.visited:
                    self.c.itemconfigure(self.buttons[dx][dy], fill='black')
                    self.check_mine((dx, dy), False)

    def show_all_mines(self):
        """
        Displays all mines after game ends with animation
        """
        if self.end_game and self.mine_coords:
            x, y = self.mine_coords.pop()
            self.c.create_image(x * self.cell_w + self.cell_w / 2,
                                y * self.cell_h + self.cell_w / 2,
                                image=self.mine_image, tags='mine')
            self.c.after(self.delay, self.show_all_mines)


def get_arguments():
    """
    Parse and validate the command line arguments.
    :return: tuple containing the difficulty (int), size (int), debug
     mode (boolean), and the verbose option (boolean).
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('difficulty',
                        help='What difficulty level?',
                        choices=['easy', 'medium', 'hard'])

    parser.add_argument('size',
                        help='How many columns/rows in the grid?',
                        type=int,
                        nargs='?',
                        default=8)

    parser.add_argument('-d', '--debug',
                        help='Debug Mode?',
                        action='store_true')

    parser.add_argument('-v', '--verbose',
                        help='Print details?',
                        action='store_true')

    arguments = parser.parse_args()
    difficulty = arguments.difficulty
    size = arguments.size
    debug = arguments.debug
    verbose = arguments.verbose
    return difficulty, size, debug, verbose


def main():
    difficulty, size, debug, verbose = get_arguments()
    if verbose:
        print(f'Starting {difficulty} game with a grid of size {size}')
    import sys
    sys.setrecursionlimit(int(2.5*size**2))
    root = tk.Tk()
    app = GameApp(root, {'easy': 1, 'medium': 2, 'hard': 3}[difficulty],
                  size, debug)
    root.mainloop()


if __name__ == '__main__':
    main()
