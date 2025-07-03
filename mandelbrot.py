import numpy as np
import matplotlib.pyplot as plt
import concurrent.futures
import argparse
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


def calc_block_wrapper(M: np.ndarray, x: int, y: int, N: int):
    return [x, y, calc_block(M, N)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='Mandelbrot')
    parser.add_argument('workers_count') 
    args = parser.parse_args()

    max_workers = int(args.workers_count)

    CENTER = (-0.10091071428571463, -0.765967207792208)
    padding = 2
    
    for i in tqdm(range(10)):

        padding *= .9
    
        START = datetime.now()

        N = 255

        X_LIM = (-0.765987207792208, -0.7659472077922079)
        Y_LIM = (-0.10093071428571464, -0.10089071428571462)

        X_LIM = (CENTER[1] - padding, CENTER[1] + padding)
        Y_LIM = (CENTER[0] - padding, CENTER[0] + padding)

        X_RES = 500
        Y_RES = 500

        BLOCK_SHAPE = (Y_RES / 10, X_RES / 10)

        X = np.linspace(*X_LIM, X_RES, dtype=np.float64)
        Y = np.linspace(*Y_LIM, Y_RES, dtype=np.float64)

        M = np.zeros((len(Y), len(X)), dtype=np.complex128)
        R = np.zeros((len(Y), len(X)), dtype=int)

        for m, y in enumerate(Y):
            for n, x in enumerate(X):
                M[m, n] = x + y*1j

        block_height, block_width = BLOCK_SHAPE
        blocks = []

        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            for y in range(10):
                for x in range(10):
                    B = M[int(y*block_height) : int((y+1)*block_height), int(x*block_width) : int((x+1)*block_width)]
                    # print(f'Block shape: {B.shape}')
                    futures.append(executor.submit(calc_block_wrapper, B, x, y, N))

        blocks = []
        for future in concurrent.futures.as_completed(futures):
            blocks.append(future.result())


        for y in range(10):
            for x in range(10):
                n, m, block = blocks[x + 10*y]
                R[int(m*block_height) : int((m+1)*block_height), int(n*block_width) : int((n+1)*block_width)] = block



        print(f'\nDuration: {datetime.now() - START}')

        plt.imshow(R, cmap='cividis')
        plt.imsave(f'renders/render1/{i}.png', R, cmap='cividis')

        # plt.show()