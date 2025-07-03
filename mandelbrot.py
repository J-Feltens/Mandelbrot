import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
from tqdm import tqdm
from datetime import datetime

def calc_convergence(c: np.complex128, N: int) -> int:
    '''
        Synopsis
            Calculates the convergence of the Mandelbrot Series 
                z_{n+1} = z_{n} + c,    n in [0, ..., N]
            Returns the iteration n in which the partial series 
            surpasses abs(z_n) < 2, i.e. is deemed as divergent.
    
        Returns 
            int:        an integer representing the color the 
                        pixel at c should be colored, 
                        between [0, N].
    '''
    z, z_ = 0, 0
    i = 0
    while N > 0:
        z_ = z**2 + c
        if np.sqrt(z_.real**2 + z_.imag**2) > 2: return i
        
        N, i = N-1, i+1
        z = z_
    return 0

def calc_block(M: np.ndarray, N: int, progress: bool=False) -> np.ndarray:
    '''
        Synopsis
            Calculates the Mandelbrot Set for a list of complex 
            numbers.

        Params
            M np.ndarray:       2x2 array of np.complex128 
                                complex numbers.
            
            progress bool:      Output the progress for the block
                                using a tqdm prog bar. Defaults to
                                False.

        Returns
            np.ndarray:         2x2 array of ints with the 
                                corresponding convergence index 
                                according to calc_convergence.
    '''
    pbar = tqdm(total=len(M) * len(M[0])) if progress else None

    R = np.zeros_like(M, dtype=int)
    for m in range(len(M)):
        for n in range(len(M[0])):
            R[m, n] = calc_convergence(M[m, n], N)

            if pbar: pbar.update(1)

    return R


if __name__ == '__main__':
    START = datetime.now()

    N = 255

    X_LIM = (-0.765987207792208, -0.7659472077922079)
    Y_LIM = (-0.10093071428571464, -0.10089071428571462)

    X_RES = 1920
    Y_RES = 1080

    X = np.linspace(*X_LIM, X_RES, dtype=np.float64)
    Y = np.linspace(*Y_LIM, Y_RES, dtype=np.float64)

    M = np.zeros((len(Y), len(X)), dtype=np.complex128)

    for m, y in enumerate(Y):
        for n, x in enumerate(X):
            M[m, n] = x + y*1j

    block_shape = (108, 192)
    block_height, block_width = block_shape
    blocks = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        futures = []
        for y in range(10):
            for x in range(10):
                B = M[int(y*block_height) : int((y+1)*block_height), int(x*block_width) : int((x+1)*block_width)]
                print(B.shape)
                futures.append(executor.submit(calc_block, B, N))

    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        # print(f"Result: {result}")


    print(f'\nDuration: {datetime.now() - START}')
