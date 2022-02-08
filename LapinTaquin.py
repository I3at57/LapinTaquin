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

    def __init__(self, master, text: str, id: int):
        # master: the Grid instance of the tile.
        # text: the text displayed on the tile
        # the id of the tile. Each tile of the project must have is own id
        self.master = master
        self.text = text

        # Check if the id is not already used
        for tile in Tile.all:
            if tile.id == id:
                print(f"This tile id: {id} is already used by {tile}")
                return(None)
        self.id = id

        # The tile with 0 id has specific text and color.
        if self.id == 0:
            self.element = Button(
                master.frame,
                text=text,
                height=TILE_HEIGHT, width=TILE_WIDTH,
                background=FRAME_TILE_BG_COLOR,
                command=lambda: [self.action(self.id)]
            )
        else:
            self.element = Button(
                master,
                text=text,
                height=TILE_HEIGHT, width=TILE_WIDTH,
                background=TILE_BG_COLOR,
                command=lambda: [self.action(self.id)]
            )

        # Add this tile to the register
        Tile.all.append(self)

    def action(self, id):
        # Action depend of the Ideap
        if id == 0:
            pass
        else:
            self.master.move(id)    # Call the 'move' action of the master Grid

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

    def __init__(self, master, name: str, size: int):
        self.name = name
        self.size = size
        self.frame = Frame(
            master,
            background=FRAME_MENU_BG_COLOR,
            relief='ridge', borderwidth=FRAME_BORDER_WIDTH
        )
        self.listOfTile = []
        count = 0
        for i in range(self.size*self.size):
            if i == 0:
                tile = Tile(self, " ", i)
            else:
                tile = Tile(self, str(i), i)
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

    def find_position_from_id(self, id):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == id:
                    return([i, j])
        return(None)

    def find_tile_from_id(self, id):
        for i in range(len(self.listOfTile)):
            if self.listOfTile[i].id == id:
                return(i)
        return(None)

    def remove_one_tile(self, id):
        num = self.find_tile_from_id(id)
        self.listOfTile[num].remove()

    def build_one_tile(self, id, pos):
        pos = self.find_position_from_id(id)
        num = self.find_tile_from_id(id)
        self.listOfTile[num].build(pos[0], pos[1])

    def switch_two_tile(self, posA, posB):
        stock = self.grid[posA[0]][posA[1]]
        self.grid[posA[0]][posA[1]] = self.grid[posB[0]][posB[1]]
        self.grid[posB[0]][posB[1]] = stock

    def move(self, id):
        zeroTilePosition = self.find_position_from_id(0)
        tilePosition = self.find_position_from_id(id)
        if Grid.are_next(tilePosition, zeroTilePosition):
            self.remove_one_tile(id)
            self.remove_one_tile(0)
            self.switch_two_tile(tilePosition, zeroTilePosition)
            self.build_one_tile(id, self.find_position_from_id(id))
            self.build_one_tile(0, self.find_position_from_id(0))

    def build(self):
        self.frame.pack(side='top', fill='both')
        for i in range(self.size):
            for j in range(self.size):
                self.listOfTile[
                    self.find_tile_from_id(self.grid[i][j])
                ].build(i, j)


class App:

    def __init__(self):
        self.name = 'Lapin Taquin'
        self.root = Tk()
        self.board = Grid(self.root, "Board", 3)

    def buid(self):
        self.board.build()
        self.root.resizable(0, 0)
        self.root.title(self.name)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    os.system("cls")

    lapinTaquin = App()
    lapinTaquin.buid()
    lapinTaquin.run()
