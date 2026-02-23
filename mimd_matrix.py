import multiprocessing
import numpy as np
import time

print("=== MIMD: Multiple Instruction Multiple Data ===")

size = 300
A = np.random.rand(size, size)
B = np.random.rand(size, size)

def multiply_row(args):
    row, B = args
    return np.dot(row, B)

if __name__ == "__main__":
    pool = multiprocessing.Pool()

    start = time.time()

    result = pool.map(multiply_row, [(A[i], B) for i in range(size)])

    pool.close()
    pool.join()

    end = time.time()

    print("Execution time (MIMD):", end - start)