#!/usr/bin/env python

import time
import random
from tkinter import *
from PIL import Image
import sys
OUT = '#000000'
# FILL_B = '#ffffff'
FILL_B = '#223322'
ARC_WIDTH = 5
SMALL_SQ = 40
NO_OF_SQUARES = 8
WIDTH, HEIGHT = NO_OF_SQUARES * SMALL_SQ - 2, NO_OF_SQUARES * SMALL_SQ - 2


def one_tile(side, coordinates, orient, board):
    board.create_rectangle(coordinates[0], coordinates[1],
                           coordinates[0] + side, coordinates[1] + side,
                           fill=FILL_B, width=0, outline=FILL_B)
    if orient:
        board.create_arc(coordinates[0] + side / 2, coordinates[1] + side / 2,
                         coordinates[0] + side * 3 / 2,
                         coordinates[1] + side * 3 / 2, width=ARC_WIDTH,
                         style=ARC, start=87, extent=96, outline=OUT)
        board.create_arc(coordinates[0] + side / 2, coordinates[1] + side / 2,
                         coordinates[0] - side / 2,
                         coordinates[1] - side / 2, width=ARC_WIDTH, style=ARC,
                         start=1, extent=-92, outline=OUT)
    else:
        board.create_arc(coordinates[0] + side / 2, coordinates[1] + side / 2,
                         coordinates[0] + side * 3 / 2,
                         coordinates[1] - side / 2, width=ARC_WIDTH, style=ARC,
                         start=179, extent=92, outline=OUT)
        board.create_arc(coordinates[0] + side / 2, coordinates[1] + side / 2,
                         coordinates[0] - side / 2,
                         coordinates[1] + side * 3 / 2, width=ARC_WIDTH,
                         style=ARC, start=-1, extent=92, outline=OUT)


def big_square(small_n0, l_up_corner):
    for i in range(small_n0):
        for j in range(small_n0):
            orient = random.choice([True, False])
            one_tile(SMALL_SQ, (
                l_up_corner[0] + i * SMALL_SQ, l_up_corner[1] + j * SMALL_SQ),
                     orient, canv)


def get_pixel_c(image_name, x, y):
    get_c = "#"
    try:
        image_name.getpixel((x, y))
    except:
        return "#000000"
    for colour in image_name.getpixel((x, y)):
        get_c += str((hex(int(colour))))[2:]
    return get_c


def flood_fill(image_name, x, y, fill_color=(200, 0, 100)):
    pixels_to_check = [(x, y)]
    while True:
        if not pixels_to_check:
            break
        pixel = pixels_to_check[0]

        col = get_pixel_c(image_name, pixel[0], pixel[1])

        if col == FILL_B:
            image_name.putpixel((pixel[0], pixel[1]), fill_color)
            if pixel[0] + 1 <= LIMIT:
                pixels_to_check.append((pixel[0] + 1, pixel[1]))
            if pixel[0] - 1 >= 0:
                pixels_to_check.append((pixel[0] - 1, pixel[1]))
            if pixel[1] + 1 <= LIMIT:
                pixels_to_check.append((pixel[0], pixel[1] + 1))
            if pixel[1] - 1 >= 0:
                pixels_to_check.append((pixel[0], pixel[1] - 1))
        del pixels_to_check[0]


def fill_one_sq(image, x, y):
    sq_side = LIMIT // NO_OF_SQUARES

    pixels_set = [(3, 3), (sq_side // 2, sq_side // 2),
                  (3 * sq_side // 4+3, 3 * sq_side // 4+3),
                  (sq_side // 4, 3 * sq_side // 4),
                  (3 * sq_side // 4, sq_side // 4,)]
    for pixel in pixels_set:
        pixel_color = (get_pixel_c(image, x + pixel[0], y + pixel[1]))
        if pixel_color == FILL_B:
            p = [0.4, 0.4, 0.2]
            el_list=[(200, 0, 100), (255, 255, 255), (0, 0, 0)]
            list_to_choice = []
            for i in range(len(p)):
                element = el_list[i]
                while p[i] * 100 > 0:
                    p[i] -= 1 / 100
                    list_to_choice.append(element)
            fill_col = random.choice(list_to_choice)
            flood_fill(image, x + pixel[0], y + pixel[1], fill_col)



master = Tk()

canv = Canvas(master, width=WIDTH, height=HEIGHT)
canv.pack()

big_square(NO_OF_SQUARES, (0, 0))

canv.update()
canv.postscript(file="sq1.ps", colormode='color')
# mainloop()
img = Image.open("sq1.ps")
sys.setrecursionlimit(img.size[1] ** 2)
LIMIT = img.size[0]
print(LIMIT)
STEP = LIMIT// NO_OF_SQUARES
for i in range(NO_OF_SQUARES):
    for j in range(NO_OF_SQUARES):

        fill_one_sq(img, 0+j*STEP, 0+i*STEP)

img.show()
epoch_time = int(time.time())
img.save("{0}.png".format(epoch_time))