import numpy as np
import matplotlib.pyplot as plt


def calc_color(c, N) -> int:
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

N = 255

X_LIM = (np.float64(-0.765987207792208), np.float64(-0.7659472077922079))
Y_LIM = (np.float64(-0.10093071428571464), np.float64(-0.10089071428571462))

X_RES = 1920
Y_RES = 1080

X = np.linspace(*X_LIM, X_RES)
Y = np.linspace(*Y_LIM, Y_RES)

M = np.zeros((len(Y), len(X)), dtype=np.float32)

for m in range(len(Y)):
    for n in range(len(X)):
        M[m, n] = calc_color(X[n] + Y[m]*1j, N)

plt.imshow(M, extent=[*X_LIM, *np.flip(Y_LIM)], cmap='cividis')

plt.show()