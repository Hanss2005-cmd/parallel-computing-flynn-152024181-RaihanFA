import numpy as np
import time

print("=== SISD: Single Instruction Single Data ===")

size = 300
A = np.random.rand(size, size)
B = np.random.rand(size, size)

start = time.time()

C = np.zeros((size, size))
for i in range(size):
    for j in range(size):
        for k in range(size):
            C[i][j] += A[i][k] * B[k][j]

end = time.time()

print("Execution time (SISD):", end - start)