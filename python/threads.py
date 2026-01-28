# 6. Using ThreadPoolExecutor (thread pool)
from concurrent.futures import ThreadPoolExecutor, as_completed

def square(n):
	time.sleep(0.5)
	return n * n

with ThreadPoolExecutor(max_workers=4) as executor:
	futures = [executor.submit(square, i) for i in range(5)]
	for future in as_completed(futures):
		print("Result:", future.result())

# 7. Mapping functions with ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
	results = list(executor.map(square, range(5, 10)))
	print("Mapped results:", results)
# 1. Basic threading example
import threading
import time

def print_numbers():
	for i in range(5):
		print(f"Number: {i}")
		time.sleep(0.5)

t1 = threading.Thread(target=print_numbers)
t1.start()
t1.join()

# 2. Thread with arguments
def greet(name):
	print(f"Hello, {name}!")

t2 = threading.Thread(target=greet, args=("Alice",))
t2.start()
t2.join()

# 3. Multiple threads
def worker(num):
	print(f"Worker {num} starting")
	time.sleep(1)
	print(f"Worker {num} done")

threads = []
for i in range(3):
	t = threading.Thread(target=worker, args=(i,))
	threads.append(t)
	t.start()
for t in threads:
	t.join()

# 4. Using threading.Lock
counter = 0
lock = threading.Lock()

def increment():
	global counter
	for _ in range(1000):
		with lock:
			counter += 1

threads = [threading.Thread(target=increment) for _ in range(10)]
for t in threads:
	t.start()
for t in threads:
	t.join()
print("Counter:", counter)

# 5. Daemon threads
def background_task():
	while True:
		print("Background task running...")
		time.sleep(1)

daemon_thread = threading.Thread(target=background_task, daemon=True)
daemon_thread.start()
time.sleep(3)
print("Main thread done. Daemon will exit.")
