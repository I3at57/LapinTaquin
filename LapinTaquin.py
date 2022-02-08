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

        if self.grid == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            App.register[self.appId].win()

    def update_grid(self):
        print(self.grid)
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


class Menu:

    def __init__(self, appId: int):
        self.appId = appId
        self.font = tkinter.font.Font(
            family='Helvetica',
            size=12,
            weight='bold',
            slant='italic'
        )
        self.frame = Frame(
            App.register[self.appId].root,
            background=FRAME_MENU_BG_COLOR,
            relief='ridge', borderwidth=FRAME_BORDER_WIDTH
        )
        self.dictButton = {
            'Random': Button(
                self.frame, text='Random', font=self.font,
                command=lambda: [App.register[self.appId].random_grid(3)]
            ),
            'Edit': Button(
                self.frame, text='Edit', font=self.font,
                # command=lambda: [new_grid()]
            ),
            'Default': Button(
                self.frame, text='Default', font=self.font,
                command=lambda: [App.register[self.appId].default_grid(3)]
            )
        }
        self.dictLabel = {
            'Win': Label(
                self.frame, text="Congratulation: You win !", font=self.font
            )
        }

    def display_label(self, label: str, unPack=False):
        print(label)
        if unPack:
            self.dictLabel[label].pack_forget()
        else:
            self.dictLabel[label].pack(side='right')

    def build(self):
        self.frame.pack(side='top', fill='both')
        for button in self.dictButton.values():
            button.pack(side='left')


class App:
    register = []

    def __init__(self):
        self.name = 'Lapin Taquin'
        self.appId = len(App.register)
        App.register.append(self)
        print(App.register[0])
        print(f"App Id: {self.appId}")
        self.root = Tk()
        self.board = Grid(self.appId, 3)
        self.menu = Menu(self.appId)

    @staticmethod
    def generate_grid(size):
        pool = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        newGrid = []

        for row in range(size):
            line = []
            for j in range(size):
                n = choice(pool)
                line.append(n)
                pool.remove(n)
            newGrid.append(line)

        return(newGrid)

    def random_grid(self, size):
        self.menu.display_label('Win', unPack=True)
        self.board.grid = App.generate_grid(size)
        self.board.update_grid()

    def default_grid(self, size):
        self.menu.display_label('Win', unPack=True)
        self.board.grid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.board.update_grid()

    def win(self):
        self.menu.display_label('Win')

    def buid(self):
        self.menu.build()
        self.board.build()
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
