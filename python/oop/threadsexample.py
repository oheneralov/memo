import asyncio

async def task(name, delay):
    print(f"Start {name}")
    await asyncio.sleep(delay)
    print(f"End {name}")

async def main():
    await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3),
    )

print("Running tasks...")
asyncio.run(main())
print("All tasks completed.")