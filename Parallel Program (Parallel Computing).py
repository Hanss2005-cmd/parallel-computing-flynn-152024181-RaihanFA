from multiprocessing import Process, Queue

def partial_sum(start, end, q, pid):
    s = sum(range(start, end + 1))
    print(f"Process {pid}: sum({start} to {end}) = {s}")
    q.put(s)

if __name__ == "__main__":
    q = Queue()

    p1 = Process(target=partial_sum, args=(1, 3, q, 1))
    p2 = Process(target=partial_sum, args=(4, 5, q, 2))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    total = q.get() + q.get()
    print("Final Parallel Sum =", total)