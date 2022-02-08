from constantes import *
from tkinter import *
import tkinter.font
from random import choice

###############################################################################

# Main element of the gui
root = Tk()

# Declare Font
font_tile = tkinter.font.Font(
    family='Helvetica',
    size=20,
    weight='bold',
    slant='italic'
)

# Frames
frameMenu = Frame(
    root,
    background=FRAME_MENU_BG_COLOR,
    relief='ridge', borderwidth=FRAME_BORDER_WIDTH
)
frameTile = Frame(
    root,
    background=FRAME_TILE_BG_COLOR,
    relief='ridge', borderwidth=FRAME_BORDER_WIDTH
)

# Button of frameMenu
buttonMenuFile = Button(
    frameMenu, text='File',
    command=lambda: [new_grid()]
)
buttonMenuEdit = Button(frameMenu, text='Edit')
buttonMenuHelp = Button(frameMenu, text='Help')
buttonMenuResult = Button(frameMenu, text='YOU WIN !', foreground='red')

# tile of frameTile
buttonTile1 = Button(
    frameTile, text='1', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(1)],
    font=font_tile
)
buttonTile2 = Button(
    frameTile, text='2', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(2)],
    font=font_tile
)
buttonTile3 = Button(
    frameTile, text='3', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(3)],
    font=font_tile
)
buttonTile4 = Button(
    frameTile, text='4', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(4)],
    font=font_tile
)
buttonTile5 = Button(
    frameTile, text='5', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(5)],
    font=font_tile
)
buttonTile6 = Button(
    frameTile, text='6', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(6)],
    font=font_tile
)
buttonTile7 = Button(
    frameTile, text='7', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(7)],
    font=font_tile
)
buttonTile8 = Button(
    frameTile, text='8', height=TILE_HEIGHT, width=TILE_WIDTH,
    background=TILE_BG_COLOR,
    command=lambda: [move_case(8)],
    font=font_tile
)
buttonTileEmpty = Button(
    frameTile, height=TILE_HEIGHT, width=TILE_WIDTH,
    background=FRAME_TILE_BG_COLOR,
    font=font_tile
)

###############################################################################
# Deflaut state of the grid
taquinGrid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
goalGrid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
###############################################################################


# Pack all element as the default state
def pack_all():
    frameMenu.pack(side='top', fill='both')
    frameTile.pack(side='top', fill='both')

    buttonMenuFile.pack(side='left')
    buttonMenuEdit.pack(side='left')
    buttonMenuHelp.pack(side='left')

    buttonTile1.grid(row=0, column=0)
    buttonTile2.grid(row=0, column=1)
    buttonTile3.grid(row=0, column=2)
    buttonTile4.grid(row=1, column=0)
    buttonTile5.grid(row=1, column=1)
    buttonTile6.grid(row=1, column=2)
    buttonTile7.grid(row=2, column=0)
    buttonTile8.grid(row=2, column=1)
    buttonTileEmpty.grid(row=2, column=2)


# Remove all button
def unpack_button():
    buttonTile1.pack_forget()
    buttonTile2.pack_forget()
    buttonTile3.pack_forget()
    buttonTile4.pack_forget()
    buttonTile5.pack_forget()
    buttonTile6.pack_forget()
    buttonTile7.pack_forget()
    buttonTile8.pack_forget()
    buttonTileEmpty.pack_forget()


# Return a button place
def find_case_on_grid(val):

    global taquinGrid

    for i in range(3):
        for j in range(3):
            if taquinGrid[i][j] == val:
                return(i, j)
    return -1


def find_all_position():

    global taquinGrid

    position = []

    for i in range(9):
        values = find_case_on_grid(i)
        position.append(values)

    return(position)


# Update the gui in line with the taquinGrid
def update_grid():

    global taquinGrid

    unpack_button()

    position = find_all_position()
    print(position)

    buttonTileEmpty.grid(row=position[0][0], column=position[0][1])
    buttonTile1.grid(row=position[1][0], column=position[1][1])
    buttonTile2.grid(row=position[2][0], column=position[2][1])
    buttonTile3.grid(row=position[3][0], column=position[3][1])
    buttonTile4.grid(row=position[4][0], column=position[4][1])
    buttonTile5.grid(row=position[5][0], column=position[5][1])
    buttonTile6.grid(row=position[6][0], column=position[6][1])
    buttonTile7.grid(row=position[7][0], column=position[7][1])
    buttonTile8.grid(row=position[8][0], column=position[8][1])

    if taquinGrid == goalGrid:
        buttonMenuResult.pack(side='left')


def is_next_to_zero(num, num_position, zero_position):

    global taquinGrid

    if num_position[0] == zero_position[0]:
        if (
            (num_position[1] == zero_position[1] + 1) or
            (num_position[1] == zero_position[1] - 1)
        ):
            return(True)
        else:
            return(False)
    elif num_position[1] == zero_position[1]:
        if (
            (num_position[0] == zero_position[0] + 1) or
            (num_position[0] == zero_position[0] - 1)
        ):
            return(True)
        else:
            return(False)
    else:
        return(False)


def move_case(num):

    global taquinGrid

    position = find_case_on_grid(num)
    zeroPosition = find_case_on_grid(0)

    if is_next_to_zero(num, position, zeroPosition):
        taquinGrid[zeroPosition[0]][zeroPosition[1]] = num
        taquinGrid[position[0]][position[1]] = 0
        update_grid()
    else:
        return -1


def generate_grid():

    global taquinGrid

    pool = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    grid = []

    while len(grid) < 9:
        n = choice(pool)
        grid.append(n)
        pool.remove(n)

    taquinGrid = [
        [grid[0], grid[1], grid[2]],
        [grid[3], grid[4], grid[5]],
        [grid[6], grid[7], grid[8]]
    ]


def verifier_configuration():

    global taquinGrid

    grid = []

    for i in taquinGrid:
        for j in i:
            grid.append(j)

    coeefficient_desordre = 0

    for i in range(len(grid)):
        for j in grid[i:][1:]:
            if i > j:
                coeefficient_desordre += 1

    print(coeefficient_desordre)

    if coeefficient_desordre % 2 == 0:
        print(True)
        return(True)
    else:
        print(False)
        return(False)


def new_grid():

    buttonMenuResult.pack_forget()

    generate_grid()
    while not verifier_configuration():
        generate_grid()

    update_grid()

###############################################################################


if __name__ == '__main__':
    pass
