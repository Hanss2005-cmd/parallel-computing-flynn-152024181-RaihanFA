from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading


def simulate_task(task):
    task_id, duration = task
    start = time.time()
    print(
        f"Worker {threading.current_thread().name} mengerjakan task {task_id} "
        f"(beban {duration:.1f} detik)"
    )
    time.sleep(duration)
    finish = time.time()
    return {
        "task_id": task_id,
        "duration": duration,
        "worker": threading.current_thread().name,
        "elapsed": finish - start,
    }


if __name__ == "__main__":
    print("=== LOAD BALANCING DENGAN PARALLEL WORKER ===")

    tasks = [
        ("T1", 1.0),
        ("T2", 0.5),
        ("T3", 1.5),
        ("T4", 0.7),
        ("T5", 1.2),
        ("T6", 0.8),
        ("T7", 1.8),
        ("T8", 0.6),
    ]

    num_workers = 4
    print(f"Jumlah worker : {num_workers}")
    print(f"Jumlah task   : {len(tasks)}")
    print("Daftar beban  :", tasks)

    start_time = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(simulate_task, task) for task in tasks]
        for future in as_completed(futures):
            results.append(future.result())

    total_time = time.time() - start_time

    print("\n=== HASIL EKSEKUSI ===")
    for result in sorted(results, key=lambda item: item["task_id"]):
        print(
            f"{result['task_id']} selesai oleh {result['worker']} "
            f"dalam {result['elapsed']:.2f} detik"
        )

    worker_loads = {}
    for result in sorted(results, key=lambda item: item["task_id"]):
        worker_loads.setdefault(result["worker"], 0)
        worker_loads[result["worker"]] += result["duration"]

    print("\n=== RINGKASAN LOAD BALANCING ===")
    for worker, load in sorted(worker_loads.items()):
        print(f"{worker} total beban: {load:.1f} detik")

    print(f"\nTotal waktu eksekusi paralel: {total_time:.2f} detik")
    print(
        "Kesimpulan: task dibagi dinamis ke worker yang tersedia, "
        "sehingga beban kerja lebih merata."
    )
