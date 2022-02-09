from constantes import *
from tkinter import *
import tkinter.font
from random import choice
import os


class Tile:
    """
    Class that represent the tiles on the grid
    """
    all = []   # Acces to all instance of the class

    def __init__(self, master, font, text: str, id: int):
        # master: the Grid instance of the tile.
        # text: the text displayed on the tile
        # the id of the tile. Each tile of the project must have is own id
        self.text = text

        # Check if the id is not already used
        for tile in Tile.all:
            if tile.id == id:
                print(f"This tile id: {id} is already used by {tile}")
                return(None)
        self.id = id

        self.element = Button(
            master.frame,
            text=text,
            height=TILE_HEIGHT, width=TILE_WIDTH,
            background=TILE_BG_COLOR, font=font,
            command=lambda: [master.move(self.id)]
        )

        # Add this tile to the register
        Tile.all.append(self)

    def build(self, x, y):
        # build the tile on the gui
        # @ -> y
        # |
        # x
        self.element.grid(row=x, column=y)

    def remove(self):
        # Remove the tile of the gui
        self.element.pack_forget()


class Grid:
    """
    Class that represent a grid of taquin
    """
    all = []   # Acces to all instance of the class

    def __init__(self, appId, size: int, objectif=[]):
        # master: the Tk() father instance of the grid.
        # text: the text displayed on the tile
        # the id of the tile. Each tile of the project must have is own id
        self.appId = appId
        self.font = tkinter.font.Font(
            family='Helvetica',
            size=20,
            weight='bold',
            slant='italic'
        )
        self.frame = Frame(
            App.register[self.appId].root,
            background=FRAME_TILE_BG_COLOR,
            relief='ridge', borderwidth=FRAME_BORDER_WIDTH
        )

        self.size = size

        self.listOfTile = []
        for i in range(self.size*self.size):
            tile = Tile(self, self.font, str(i+1), i+1)
            self.listOfTile.append(tile)

        self.grid = []
        count = 1
        for i in range(self.size):
            tab = []
            for j in range(self.size):
                if count == self.size*self.size:
                    tab.append(0)
                else:
                    tab.append(count)
                count += 1
            self.grid.append(tab)

        # Add this grid to the register
        Grid.all.append(self)

    @staticmethod
    def are_next(tileA, tileB):
        if tileA[0] == tileB[0]:
            if (
                (tileA[1] == tileB[1] + 1) or
                (tileA[1] == tileB[1] - 1)
            ):
                return(True)
            else:
                return(False)
        elif tileA[1] == tileB[1]:
            if (
                (tileA[0] == tileB[0] + 1) or
                (tileA[0] == tileB[0] - 1)
            ):
                return(True)
            else:
                return(False)
        else:
            return(False)

    def find_position_from_id(self, id: int):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == id:
                    return([i, j])
        return(None)

    def find_tile_from_id(self, id: int):
        for i in range(len(self.listOfTile)):
            if self.listOfTile[i].id == id:
                return(i)
        return(None)

    def remove_one_tile(self, id: int):
        num = self.find_tile_from_id(id)
        if num is not None:
            self.listOfTile[num].remove()

    def build_one_tile(self, id: int, pos):
        pos = self.find_position_from_id(id)
        num = self.find_tile_from_id(id)
        if num is not None:
            self.listOfTile[num].build(pos[0], pos[1])

    def switch_two_tile(self, posA, posB):
        stock = self.grid[posA[0]][posA[1]]
        self.grid[posA[0]][posA[1]] = self.grid[posB[0]][posB[1]]
        self.grid[posB[0]][posB[1]] = stock

    def move(self, id: int):
        zeroPosition = self.find_position_from_id(0)
        tilePosition = self.find_position_from_id(id)
        if Grid.are_next(tilePosition, zeroPosition):
            self.remove_one_tile(id)
            self.switch_two_tile(tilePosition, zeroPosition)
            self.build_one_tile(id, self.find_position_from_id(id))

        if self.grid == App.generate_default_grid(self.size):
            App.register[self.appId].win()

    def update_grid(self):
        for row in self.grid:
            for id in row:
                self.remove_one_tile(id)
        for i in range(self.size):
            for j in range(self.size):
                self.build_one_tile(
                    self.grid[i][j],
                    [i, j]
                )

    def build(self):
        self.frame.pack(side='top', fill='both')
        for i in range(self.size):
            for j in range(self.size):
                if not (i == (self.size - 1) and j == (self.size - 1)):
                    self.listOfTile[
                        self.find_tile_from_id(self.grid[i][j])
                    ].build(i, j)


class Display:

    def __init__(self, appId):
        self.appId = appId
        self.frame = Frame(
            App.register[self.appId].root,
            background=FRAME_TILE_BG_COLOR,
        )
        self.font = tkinter.font.Font(
            family='Helvetica',
            size=20,
            weight='bold',
            slant='italic',
        )
        self.dictLabel = {
            'Default': Label(
                self.frame, text="Lapin Taquin", font=self.font,
                bg=FRAME_TILE_BG_COLOR, fg=DISPLAY_MESSAGE_COLOR
            ),
            'Win': Label(
                self.frame, text="You Win !", font=self.font,
                bg=FRAME_TILE_BG_COLOR, fg=DISPLAY_MESSAGE_COLOR
            )
        }
        self.currentLabel = 'Default'

    def change_label(self, label):
        self.dictLabel[self.currentLabel].pack_forget()
        self.dictLabel[label].pack()
        self.currentLabel = label

    def build(self):
        self.frame.pack(side='top', fill='both')
        self.dictLabel['Default'].pack()


class App:
    register = []

    def __init__(self):
        self.name = 'Lapin Taquin'
        self.appId = len(App.register)
        App.register.append(self)
        print(App.register[0])
        print(f"App Id: {self.appId}")
        self.root = Tk()
        self.board = Grid(self.appId, 5)
        self.display = Display(self.appId)

        # Crée le menu
        self.menu = Menu(self.root)     # Menu widget
        file = Menu(self.menu, tearoff=0)   # Sub Menu File
        self.menu.add_cascade(label="File", menu=file)
        edit = Menu(self.menu, tearoff=0)   # Sub Menu Edit
        self.menu.add_cascade(label="Edit", menu=edit)
        dev = Menu(self.menu, tearoff=0)    # Sub Menu Edit
        self.menu.add_cascade(label="Dev", menu=dev)

        # Sous menu File
        file.add_command(label="Quit", command=self.root.destroy)
        # Sous menu edit
        edit.add_command(
            label="Default", command=lambda: [self.default_grid(5)]
        )
        edit.add_command(
            label="Random", command=lambda: [self.random_grid(5)]
        )
        # Sous menu Dev
        dev.add_command(
            label="Test", command=lambda: [App.generate_default_grid(5)]
        )

    @staticmethod
    def generate_grid(size):
        pool = [i for i in range(size*size)]
        newGrid = []

        for i in range(size):
            line = []
            for j in range(size):
                n = choice(pool)
                line.append(n)
                pool.remove(n)
            newGrid.append(line)

        return(newGrid)

    @staticmethod
    def generate_default_grid(size):
        pool = [i for i in range(size*size)]
        defaultGrid = []

        for i in range(size):
            line = []
            for j in range(size):
                if len(pool) == 1:
                    n = pool[0]
                else:
                    n = pool[1]
                line.append(n)
                pool.remove(n)
            defaultGrid.append(line)

        return(defaultGrid)

    def random_grid(self, size):
        self.display.change_label('Default')
        self.board.grid = App.generate_grid(size)
        print(self.board.grid)
        self.board.update_grid()

    def default_grid(self, size):
        self.display.change_label('Default')
        self.board.grid = App.generate_default_grid(size)
        print(self.board.grid)
        self.board.update_grid()

    def win(self):
        self.display.change_label('Win')

    def buid(self):
        self.board.build()
        self.display.build()
        self.root.config(menu=self.menu)
        self.root.resizable(0, 0)
        self.root.title(self.name)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    os.system("cls")

    lapinTaquin = App()
    print(App.register)
    lapinTaquin.buid()
    lapinTaquin.run()
