import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

N = 255

def calc_color(c, N=N) -> int:
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


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)


img = ax.imshow(np.zeros((200, 200)), vmin=0, vmax=N)


def recalc(center, padding):
    global img

    x_lim = (center[0] - padding, center[0] + padding)
    y_lim = (center[1] - padding, center[1] + padding)

    print(f'{x_lim}, {y_lim}')

    x = np.linspace(*x_lim, 200)
    y = np.linspace(*y_lim, 200)

    M = np.zeros((len(y), len(x)), dtype=np.float32)

    for m in range(len(y)):
        for n in range(len(x)):
            M[m, n] = calc_color(x[n] + y[m]*1j)

    # ax.clear()
    # ax.imshow(M, extent=[*x_lim, *np.flip(y_lim)])
    img.set_data(M)
    img.set_clim(np.min(M), np.max(M))
    img.set_extent([*x_lim, *np.flip(y_lim)])
    fig.canvas.draw()


recalc((0, 0), 1)

padding = 2

def onclick(event):
    global padding

    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    
    center = (event.xdata, event.ydata)

    zoom_fac = .1
    if event.dblclick:
        zoom_fac = 100

    padding = padding * zoom_fac
    recalc(center, padding)

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()