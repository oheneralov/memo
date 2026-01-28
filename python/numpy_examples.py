"""
NumPy Examples - 10 Common Use Cases
"""

import numpy as np

# Example 1: Creating arrays
print("Example 1: Creating arrays")
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.zeros((3, 3))
arr3 = np.ones((2, 4))
arr4 = np.arange(0, 10, 2)
arr5 = np.linspace(0, 1, 5)
print(f"Basic array: {arr1}")
print(f"Zeros array:\n{arr2}")
print(f"Ones array:\n{arr3}")
print(f"Range array: {arr4}")
print(f"Linspace array: {arr5}\n")

# Example 2: Array operations and mathematical functions
print("Example 2: Array operations")
arr = np.array([1, 2, 3, 4, 5])
print(f"Original: {arr}")
print(f"Add 10: {arr + 10}")
print(f"Multiply by 2: {arr * 2}")
print(f"Square: {arr ** 2}")
print(f"Square root: {np.sqrt(arr)}")
print(f"Exponential: {np.exp(arr)}\n")

# Example 3: Array indexing and slicing
print("Example 3: Indexing and slicing")
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(f"2D array:\n{arr}")
print(f"Element at [1, 2]: {arr[1, 2]}")
print(f"First row: {arr[0, :]}")
print(f"Last column: {arr[:, -1]}")
print(f"Subarray:\n{arr[0:2, 1:3]}\n")

# Example 4: Array reshaping and transposing
print("Example 4: Reshaping and transposing")
arr = np.arange(12)
print(f"Original: {arr}")
print(f"Reshaped (3x4):\n{arr.reshape(3, 4)}")
print(f"Reshaped (2x6):\n{arr.reshape(2, 6)}")
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(f"Original matrix:\n{matrix}")
print(f"Transposed:\n{matrix.T}\n")

# Example 5: Statistical operations
print("Example 5: Statistical operations")
arr = np.array([10, 20, 30, 40, 50])
print(f"Array: {arr}")
print(f"Mean: {np.mean(arr)}")
print(f"Median: {np.median(arr)}")
print(f"Standard deviation: {np.std(arr)}")
print(f"Variance: {np.var(arr)}")
print(f"Min: {np.min(arr)}, Max: {np.max(arr)}")
print(f"Sum: {np.sum(arr)}\n")

# Example 6: Boolean indexing and filtering
print("Example 6: Boolean indexing")
arr = np.array([1, 15, 23, 8, 30, 12, 45])
print(f"Original array: {arr}")
print(f"Greater than 20: {arr[arr > 20]}")
print(f"Even numbers: {arr[arr % 2 == 0]}")
print(f"Between 10 and 30: {arr[(arr >= 10) & (arr <= 30)]}\n")

# Example 7: Matrix operations
print("Example 7: Matrix operations")
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
print(f"Matrix A:\n{a}")
print(f"Matrix B:\n{b}")
print(f"Element-wise multiplication:\n{a * b}")
print(f"Matrix multiplication:\n{np.dot(a, b)}")
print(f"Matrix inverse:\n{np.linalg.inv(a)}\n")

# Example 8: Random number generation
print("Example 8: Random numbers")
np.random.seed(42)  # For reproducibility
print(f"Random float [0,1): {np.random.random(5)}")
print(f"Random integers [0,10): {np.random.randint(0, 10, 5)}")
print(f"Normal distribution: {np.random.randn(5)}")
print(f"Random choice: {np.random.choice([10, 20, 30, 40], 3)}\n")

# Example 9: Array stacking and concatenation
print("Example 9: Stacking and concatenation")
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print(f"Array 1: {arr1}")
print(f"Array 2: {arr2}")
print(f"Horizontal stack: {np.hstack((arr1, arr2))}")
print(f"Vertical stack:\n{np.vstack((arr1, arr2))}")
print(f"Concatenate: {np.concatenate((arr1, arr2))}\n")

# Example 10: Broadcasting and vectorization
print("Example 10: Broadcasting")
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
vector = np.array([10, 20, 30])
print(f"Matrix:\n{arr}")
print(f"Vector: {vector}")
print(f"Matrix + Vector (broadcasting):\n{arr + vector}")
print(f"Matrix * Vector (broadcasting):\n{arr * vector}")
print(f"Comparing with scalar: {arr > 5}")
