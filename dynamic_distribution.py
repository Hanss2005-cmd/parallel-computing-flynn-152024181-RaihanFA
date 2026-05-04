import multiprocessing
import time
import random

def task(n):
    sleep_time = random.uniform(0.5, 2)  # beban random
    print(f"Task {n} dikerjakan selama {sleep_time:.2f} detik")
    time.sleep(sleep_time)
    return n * n

def worker(task_queue, result_queue):
    while not task_queue.empty():
        try:
            n = task_queue.get_nowait()
        except:
            break
        result = task(n)
        result_queue.put(result)

if __name__ == "__main__":
    start_time = time.time()

    num_workers = 4
    tasks = list(range(1, 11))  # 10 task

    task_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Masukkan task ke queue
    for t in tasks:
        task_queue.put(t)

    processes = []
    for _ in range(num_workers):
        p = multiprocessing.Process(target=worker, args=(task_queue, result_queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    end_time = time.time()

    print("\nHasil:", results)
    print(f"Total waktu eksekusi: {end_time - start_time:.2f} detik")