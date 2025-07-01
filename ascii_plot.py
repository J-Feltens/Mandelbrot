import os
from time import sleep

import numpy as np
from matplotlib import cm
from rich.console import Console
from rich.text import Text


X_CHARS, Y_CHARS = 400, 100

COLORS = 255

CENTER = (-.7957466931, -.1847704878)
PADDING = .5

def calc_color(c, N=32) -> int:
    '''
        returns an integer representing the color the pixel at c should be colored, between [0, N]
    '''
    z, z_ = 0, 0
    i = 0
    while N > 0:
        z_ = z**2 + c
        if np.sqrt(z_.real**2 + z_.imag**2) > 2: return i
        
        N, i = N-1, i+1
        z = z_
    return 0

def print_frame(padding, center=CENTER):
    x_lim = (CENTER[0] - padding, CENTER[0] + padding)
    y_lim = (CENTER[1] - padding, CENTER[1] + padding)

    x = np.linspace(*x_lim, X_CHARS)
    y = np.linspace(*y_lim, Y_CHARS)

    console = Console()

    M = np.zeros((len(y), len(x)), dtype=np.float64)

    for m in range(len(y)):
        row = Text()
        for n in range(len(x)):
            # value at x, y
            value = calc_color(x[n] + y[m]*1j, COLORS)
            M[m,n] = value
            r, g, b, a = cm.inferno(value)
            color_string = f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"
            row.append('#', color_string)

        console.print(row)



padding = 4

while True:
    padding *= .9
    os.system('clear')
    print_frame(padding)
    sleep(.1)