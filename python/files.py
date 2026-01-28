# 6. Reading a large file in chunks
def read_in_chunks(file_path, chunk_size=1024):
	with open(file_path, 'r') as f:
		while True:
			data = f.read(chunk_size)
			if not data:
				break
			print("Chunk read:", data[:50], "...")  # Print first 50 chars

# Example usage:
# read_in_chunks("bigfile.txt", 4096)

# 7. Processing a large file line by line (generator)
def process_large_file(file_path):
	with open(file_path, 'r') as f:
		for line in f:
			yield line.strip()

# Example usage:
# for line in process_large_file("bigfile.txt"):
#     print(line)

# 8. Writing to a large file in chunks
def write_in_chunks(file_path, data_iter, chunk_size=1024):
	with open(file_path, 'w') as f:
		for chunk in data_iter:
			f.write(chunk)

# Example usage:
# write_in_chunks("output.txt", ["A"*4096]*10)

# 9. Copying a large file efficiently
def copy_large_file(src, dst, buffer_size=1024*1024):
	with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
		while True:
			buf = fsrc.read(buffer_size)
			if not buf:
				break
			fdst.write(buf)

# Example usage:
# copy_large_file("bigfile.txt", "bigfile_copy.txt")

# 10. Using mmap for random access to big files
import mmap
def mmap_read(file_path):
	with open(file_path, 'r+b') as f:
		mm = mmap.mmap(f.fileno(), 0)
		print("First 100 bytes:", mm[:100])
		mm.close()

# Example usage:
# mmap_read("bigfile.txt")
# 1. Writing to a file
with open("example.txt", "w") as f:
	f.write("Hello, world!\n")
	f.write("Second line\n")

# 2. Reading from a file
with open("example.txt", "r") as f:
	content = f.read()
	print("File content:", content)

# 3. Reading file line by line
with open("example.txt", "r") as f:
	for line in f:
		print("Line:", line.strip())

# 4. Appending to a file
with open("example.txt", "a") as f:
	f.write("Appended line\n")

# 5. Using StringIO as an in-memory stream
from io import StringIO
stream = StringIO()
stream.write("This is in memory!\n")
stream.seek(0)
print("Stream content:", stream.read())
