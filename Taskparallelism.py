import threading
import time

def download_gambar():
    print("Memulai download gambar...")
    time.sleep(2)
    print("Download gambar selesai")

def download_video():
    print("Memulai download video...")
    time.sleep(3)
    print("Download video selesai")

def download_dokumen():
    print("Memulai download dokumen...")
    time.sleep(1)
    print("Download dokumen selesai")

t1 = threading.Thread(target=download_gambar)
t2 = threading.Thread(target=download_video)
t3 = threading.Thread(target=download_dokumen)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

print("Semua file berhasil didownload")