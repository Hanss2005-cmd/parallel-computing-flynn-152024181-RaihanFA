n = 5
total = 0
print("serial computation")
for i in range (1, n + 1):
    total += i
    print(f"step {i}: total = {total}")
print(f"final total: {total}")