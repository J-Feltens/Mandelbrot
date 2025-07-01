import numpy as np

def calc_series(c, N) -> float:
    if N <= 0: return 0
    return c + calc_series(c, N-1)**2

def calc_limit(c, N):
    z = calc_series(c, N)
    return np.sqrt(z.real**2 + z.imag**2)


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


c = .2 + .2j
c = .1 + .65j


# print(calc_limit(c, 16))

print(calc_color(c))
