# Lists Examples
# 1. Creating and appending to a list
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
print("List after append:", fruits)

# 2. List comprehension
squares = [x**2 for x in range(5)]
print("Squares:", squares)

# 3. Accessing and modifying elements
fruits[1] = "blueberry"
print("Modified list:", fruits)

# 4. Slicing a list
print("Sliced list:", fruits[1:3])

# 5. Removing an element
fruits.remove("cherry")
print("List after removal:", fruits)

# Dicts Examples
# 1. Creating and adding to a dictionary
person = {"name": "Alice", "age": 30}
person["city"] = "New York"
print("Dictionary:", person)

# 2. Accessing values
print("Name:", person["name"])

# 3. Iterating over keys and values
for key, value in person.items():
	print(f"{key}: {value}")

# 4. Checking for a key
print("Has 'age'?", "age" in person)

# 5. Removing a key
del person["city"]
print("After deletion:", person)

# Tuples Examples
# 1. Creating a tuple
point = (3, 4)
print("Tuple:", point)

# 2. Tuple unpacking
x, y = point
print("x:", x, "y:", y)

# 3. Nested tuples
triangle = ((0, 0), (1, 0), (0, 1))
print("Triangle vertices:", triangle)

# 4. Concatenating tuples
colors = ("red", "green") + ("blue",)
print("Colors:", colors)

# 5. Using tuples as dict keys
locations = {}
locations[(40.7128, -74.0060)] = "New York"
print("Locations dict:", locations)

# Strings Examples
# 1. String concatenation
greeting = "Hello, " + "world!"
print(greeting)

# 2. String formatting
name = "Bob"
print(f"Hello, {name}!")

# 3. Splitting and joining
sentence = "one,two,three"
words = sentence.split(",")
print("Split:", words)
joined = "-".join(words)
print("Joined:", joined)

# 4. Changing case
print("Upper:", name.upper())
print("Lower:", name.lower())

# 5. Slicing strings
print("Slice:", greeting[0:5])
