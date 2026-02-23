import numpy as np
import time

print("=== SIMD: Single Instruction Multiple Data ===")

size = 300
A = np.random.rand(size, size)
B = np.random.rand(size, size)

start = time.time()

C = np.dot(A, B)  # vectorized operation

end = time.time()

print("Execution time (SIMD - vectorized):", end - start)