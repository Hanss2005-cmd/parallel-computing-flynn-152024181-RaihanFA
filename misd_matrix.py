import numpy as np
import time

print("=== MISD: Multiple Instruction Single Data (Simulation) ===")

size = 300
A = np.random.rand(size, size)

def sum_matrix(M):
    return np.sum(M)

def mean_matrix(M):
    return np.mean(M)

def max_matrix(M):
    return np.max(M)

start = time.time()

s = sum_matrix(A)
m = mean_matrix(A)
mx = max_matrix(A)

end = time.time()

print("Sum:", s)
print("Mean:", m)
print("Max:", mx)
print("Execution time (MISD simulation):", end - start)