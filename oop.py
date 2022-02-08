"""
Change the project to add a oop version
"""

from constantes import *
from tkinter import *
import tkinter.font
from random import choice
import os


class Tile:
    def __init__(self, master, board, value: int, text: str, position=[0, 0]):

        self.value = value
        self.text = text
        self.position = position

        if value == 0:
            self.element = Button(
                master,
                text=text,
                height=TILE_HEIGHT, width=TILE_WIDTH,
                background=FRAME_TILE_BG_COLOR,
            )
        else:
            self.element = Button(
                master,
                text=text,
                height=TILE_HEIGHT, width=TILE_WIDTH, background=TILE_BG_COLOR,
                # command=lambda: [board.move(value)]
                command=lambda: self.remove()
            )

    def build(self):
        self.element.grid(row=self.position[0], column=self.position[1])

    def remove(self):
        self.element.pack_forget()


class Board:
    def __init__(self, master):
        self.frame = Frame(
            master,
            background=FRAME_MENU_BG_COLOR,
            relief='ridge', borderwidth=FRAME_BORDER_WIDTH
        )
        self.listOfTile = []
        count = 1
        for i in range(3):
            tab = []
            for j in range(3):
                if count == 9:
                    tt = Tile(self.frame, self, 0, str(" "), [i, j])
                else:
                    tt = Tile(self.frame, self, count, str(count), [i, j])
                tab.append(tt)
                count += 1
            self.listOfTile.append(tab)

    def build(self):
        self.frame.pack(side='top', fill='both')
        for row in self.listOfTile:
            for tt in row:
                tt.build()

    def get_information(self):
        # Return on console the state of all tile
        for row in self.listOfTile:
            for tt in row:
                print(tt.__dict__)

    def get_tile_position_in_list_from_value(self, tile):
        for i in range(3):
            for j in range(3):
                if self.listOfTile[i][j].value == tile:
                    return([i, j])
        return(None)

    def get_tile_position_in_list_from_position(self, pos):
        print(pos)
        for i in range(3):
            for j in range(3):
                # print(self.listOfTile[i][j].position)
                if self.listOfTile[i][j].position == pos:
                    return([i, j])
        return(None)

    def get_tile_position_from_value(self, tile):
        for row in self.listOfTile:
            for tt in row:
                if tile == tt.value:
                    return(tt.position)
        return(None)

    def get_tile_value_from_position(self, pos):
        for row in self.listOfTile:
            for tt in row:
                if pos == tt.position:
                    return(tt.value)

    def are_next(self, pos_tile, pos_0):
        if pos_tile[0] == pos_0[0]:
            if (
                (pos_tile[1] == pos_0[1] + 1) or
                (pos_tile[1] == pos_0[1] - 1)
            ):
                return(True)
            else:
                return(False)
        elif pos_tile[1] == pos_0[1]:
            if (
                (pos_tile[0] == pos_0[0] + 1) or
                (pos_tile[0] == pos_0[0] - 1)
            ):
                return(True)
            else:
                return(False)
        else:
            return(False)

    def remove_all_tile(self):
        for row in self.listOfTile:
            for tt in row:
                tt.remove()

    def pack_all_tile(self):
        for i in range(3):
            for j in range(3):
                pos = self.get_tile_position_in_list_from_position([i, j])
                print(pos)
                self.listOfTile[pos[0]][pos[1]].build()

    def move(self, tile):
        print(tile)
        pos_tile = self.get_tile_position_from_value(tile)
        pos_0 = self.get_tile_position_from_value(0)
        print(pos_tile, pos_0)
        if self.are_next(pos_tile, pos_0):
            self.remove_all_tile()
            self.listOfTile[pos_tile[0]][pos_tile[1]].position = pos_0
            self.listOfTile[pos_0[0]][pos_0[1]].position = pos_tile
            self.pack_all_tile()


class Menu:

    def __init__(self, master):
        self.frame = Frame(
            master,
            background=FRAME_MENU_BG_COLOR,
            relief='ridge', borderwidth=FRAME_BORDER_WIDTH
        )
        self.buttonRandom = Button(
            self.frame,
            text='Random'
        )

    def build(self):
        self.frame.pack(side='top', fill='both')
        self.buttonRandom.pack(side='left')


class App:

    def __init__(self):
        self.name = 'Lapin Taquin'
        self.root = Tk()
        self.board = Board(self.root)
        self.menu = Menu(self.root)

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
    lapinTaquin.buid()
    lapinTaquin.run()
