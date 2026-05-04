from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Setiap proses punya angka
data = rank + 1  # misal: proses 0=1, 1=2, dst

print(f"Proses {rank} punya data: {data}")

# Kumpulkan semua data ke proses 0
total = comm.reduce(data, op=MPI.SUM, root=0)

# Hanya proses 0 yang tampilkan hasil akhir
if rank == 0:
    print(f"Total penjumlahan dari semua proses: {total}")