# 1. Basic async function and running it
import asyncio

async def say_hello():
	print("Hello ...")
	await asyncio.sleep(1)
	print("...world!")

asyncio.run(say_hello())

# 2. Running multiple coroutines concurrently
async def task(name, delay):
	print(f"Task {name} started")
	await asyncio.sleep(delay)
	print(f"Task {name} finished")

async def main():
	await asyncio.gather(
		task("A", 1),
		task("B", 2),
		task("C", 1.5)
	)

asyncio.run(main())

# 3. Using asyncio.create_task
async def quick_task():
	print("Quick task running")
	await asyncio.sleep(0.5)
	print("Quick task done")

async def main2():
	t = asyncio.create_task(quick_task())
	print("Main2 continues...")
	await t

asyncio.run(main2())

# 4. Using asyncio.Queue
async def producer(queue):
	for i in range(3):
		await queue.put(i)
		print(f"Produced {i}")

async def consumer(queue):
	while not queue.empty():
		item = await queue.get()
		print(f"Consumed {item}")

async def main3():
	queue = asyncio.Queue()
	await producer(queue)
	await consumer(queue)

asyncio.run(main3())

# 5. Timeout with asyncio.wait_for
async def long_task():
	await asyncio.sleep(2)
	return "done"

async def main4():
	try:
		result = await asyncio.wait_for(long_task(), timeout=1)
	except asyncio.TimeoutError:
		print("Timeout!")
	else:
		print("Result:", result)

asyncio.run(main4())
