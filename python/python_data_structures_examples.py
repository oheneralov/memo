"""
Python Data Structures Examples - 10 Common Use Cases
"""

# Example 1: Lists - Creating and basic operations
print("Example 1: Lists - Creating and basic operations")
fruits = ['apple', 'banana', 'orange', 'mango']
numbers = [1, 2, 3, 4, 5]
mixed = [1, 'hello', 3.14, True]
print(f"Fruits: {fruits}")
print(f"Numbers: {numbers}")
print(f"Mixed: {mixed}")
print(f"Access element: {fruits[0]}")
print(f"Slice: {numbers[1:4]}")
print(f"Length: {len(fruits)}")
fruits.append('grape')
print(f"After append: {fruits}")
fruits.insert(1, 'kiwi')
print(f"After insert: {fruits}")
fruits.remove('banana')
print(f"After remove: {fruits}\n")

# Example 2: List comprehensions and filtering
print("Example 2: List comprehensions")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Original: {numbers}")
squares = [x**2 for x in numbers]
print(f"Squares: {squares}")
evens = [x for x in numbers if x % 2 == 0]
print(f"Even numbers: {evens}")
doubled_evens = [x*2 for x in numbers if x % 2 == 0]
print(f"Doubled evens: {doubled_evens}")
matrix = [[i*j for j in range(1, 4)] for i in range(1, 4)]
print(f"Matrix: {matrix}\n")

# Example 3: Dictionaries - Creating and accessing
print("Example 3: Dictionaries")
person = {
    'name': 'Alice',
    'age': 25,
    'city': 'New York',
    'occupation': 'Engineer'
}
print(f"Person: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person.get('age')}")
print(f"Keys: {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"Items: {list(person.items())}")
person['email'] = 'alice@example.com'
print(f"After adding email: {person}")
person.update({'age': 26, 'phone': '555-1234'})
print(f"After update: {person}\n")

# Example 4: Dictionary comprehensions and methods
print("Example 4: Dictionary comprehensions")
numbers = [1, 2, 3, 4, 5]
squares_dict = {x: x**2 for x in numbers}
print(f"Squares dictionary: {squares_dict}")
words = ['apple', 'banana', 'orange']
lengths = {word: len(word) for word in words}
print(f"Word lengths: {lengths}")
filtered = {k: v for k, v in squares_dict.items() if v > 10}
print(f"Filtered (value > 10): {filtered}")
# Merging dictionaries
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
merged = {**dict1, **dict2}
print(f"Merged dictionaries: {merged}\n")

# Example 5: Sets - Unique elements and operations
print("Example 5: Sets")
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
print(f"Set 1: {set1}")
print(f"Set 2: {set2}")
print(f"Union: {set1 | set2}")
print(f"Intersection: {set1 & set2}")
print(f"Difference: {set1 - set2}")
print(f"Symmetric difference: {set1 ^ set2}")
# Remove duplicates from list
numbers = [1, 2, 2, 3, 4, 4, 5, 5, 5]
unique = list(set(numbers))
print(f"Original list: {numbers}")
print(f"Unique elements: {unique}\n")

# Example 6: Tuples - Immutable sequences
print("Example 6: Tuples")
coordinates = (10, 20)
person = ('Alice', 25, 'Engineer')
print(f"Coordinates: {coordinates}")
print(f"Person: {person}")
print(f"Access element: {person[0]}")
print(f"Slice: {person[1:3]}")
# Tuple unpacking
x, y = coordinates
print(f"Unpacked: x={x}, y={y}")
name, age, occupation = person
print(f"Unpacked person: name={name}, age={age}, occupation={occupation}")
# Named tuple
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
print(f"Named tuple: {p}, x={p.x}, y={p.y}\n")

# Example 7: Stacks and Queues
print("Example 7: Stacks and Queues")
# Stack using list (LIFO)
stack = []
stack.append(1)
stack.append(2)
stack.append(3)
print(f"Stack after pushes: {stack}")
print(f"Pop: {stack.pop()}")
print(f"Stack after pop: {stack}")
# Queue using collections.deque (FIFO)
from collections import deque
queue = deque()
queue.append(1)
queue.append(2)
queue.append(3)
print(f"Queue after enqueues: {list(queue)}")
print(f"Dequeue: {queue.popleft()}")
print(f"Queue after dequeue: {list(queue)}\n")

# Example 8: defaultdict and Counter
print("Example 8: defaultdict and Counter")
from collections import defaultdict, Counter
# defaultdict
word_count = defaultdict(int)
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
for word in words:
    word_count[word] += 1
print(f"Word count (defaultdict): {dict(word_count)}")
# Counter
counter = Counter(words)
print(f"Word count (Counter): {counter}")
print(f"Most common: {counter.most_common(2)}")
# Counter operations
counter2 = Counter(['apple', 'grape', 'banana'])
print(f"Counter 1: {counter}")
print(f"Counter 2: {counter2}")
print(f"Addition: {counter + counter2}")
print(f"Subtraction: {counter - counter2}\n")

# Example 9: Nested data structures
print("Example 9: Nested data structures")
students = [
    {
        'name': 'Alice',
        'age': 20,
        'grades': [85, 90, 88],
        'subjects': {'math', 'physics', 'chemistry'}
    },
    {
        'name': 'Bob',
        'age': 22,
        'grades': [78, 82, 85],
        'subjects': {'biology', 'chemistry', 'english'}
    }
]
print("Students:")
for student in students:
    print(f"  Name: {student['name']}")
    print(f"  Age: {student['age']}")
    print(f"  Average grade: {sum(student['grades']) / len(student['grades']):.2f}")
    print(f"  Subjects: {student['subjects']}")
    print()

# Nested dictionary
company = {
    'IT': {
        'employees': ['Alice', 'Bob'],
        'budget': 100000
    },
    'HR': {
        'employees': ['Charlie', 'David'],
        'budget': 80000
    }
}
print("Company structure:")
for dept, info in company.items():
    print(f"  {dept}: {info['employees']}, Budget: ${info['budget']}\n")

# Example 10: Advanced list operations
print("Example 10: Advanced list operations")
numbers = [5, 2, 8, 1, 9, 3, 7]
print(f"Original: {numbers}")
print(f"Sorted: {sorted(numbers)}")
print(f"Reversed: {list(reversed(numbers))}")
print(f"Max: {max(numbers)}")
print(f"Min: {min(numbers)}")
print(f"Sum: {sum(numbers)}")
# zip and enumerate
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]
zipped = list(zip(names, ages))
print(f"Zipped: {zipped}")
for i, (name, age) in enumerate(zipped):
    print(f"  {i}: {name} is {age} years old")
# any and all
numbers = [2, 4, 6, 8]
print(f"All even: {all(x % 2 == 0 for x in numbers)}")
print(f"Any odd: {any(x % 2 != 0 for x in numbers)}")
