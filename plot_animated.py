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

CENTER = (-.7957402762, -.1848230535)
CENTER = (-.79574719, -.18477084)
CENTER = (-.7957466931, -.1847704878)

CENTER = (-.7523932387219849, -.0386979842015857)


FRAME_COUNT = 20000

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)


img = ax.imshow(np.zeros((200, 200)), vmin=0, vmax=N, cmap='inferno')

padding = 2

def animate(frame):
    global img, padding

    padding = padding / 1.2

    x_lim = (CENTER[0] - padding, CENTER[0] + padding)
    y_lim = (CENTER[1] - padding, CENTER[1] + padding)

    x = np.linspace(*x_lim, 200)
    y = np.linspace(*y_lim, 200)

    M = np.zeros((len(y), len(x)), dtype=np.float32)

    for m in range(len(y)):
        for n in range(len(x)):
            M[m, n] = calc_color(x[n] + y[m]*1j, N)

    ax.clear()
    ax.imshow(M, extent=[*x_lim, *np.flip(y_lim)], cmap='inferno')
    # img.set_data(M)
    # img.set_extent([*x_lim, *np.flip(y_lim)])
    # fig.canvas.draw()

    return [img]

ani = FuncAnimation(fig, animate, frames=FRAME_COUNT, interval=1)

plt.show()