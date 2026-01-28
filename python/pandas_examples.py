"""
Pandas Examples - 10 Common Use Cases
"""

import pandas as pd
import numpy as np

# Example 1: Creating DataFrames
print("Example 1: Creating DataFrames")
df1 = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 28],
    'City': ['New York', 'London', 'Paris', 'Tokyo']
})
print("From dictionary:")
print(df1)
print()

df2 = pd.DataFrame(np.random.randn(3, 4), columns=['A', 'B', 'C', 'D'])
print("From NumPy array:")
print(df2)
print("\n")

# Example 2: Reading and selecting data
print("Example 2: Selecting data")
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 22],
    'Salary': [50000, 60000, 75000, 55000, 48000],
    'Department': ['IT', 'HR', 'IT', 'Finance', 'HR']
})
print("Original DataFrame:")
print(df)
print(f"\nSelect column: \n{df['Name']}")
print(f"\nSelect multiple columns: \n{df[['Name', 'Age']]}")
print(f"\nSelect rows by index: \n{df.iloc[0:3]}")
print(f"\nSelect by condition: \n{df[df['Age'] > 25]}\n")

# Example 3: DataFrame operations
print("Example 3: DataFrame operations")
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50],
    'C': [100, 200, 300, 400, 500]
})
print("Original:")
print(df)
print("\nAdd new column:")
df['D'] = df['A'] + df['B']
print(df)
print("\nCalculate column statistics:")
print(f"Sum of A: {df['A'].sum()}")
print(f"Mean of B: {df['B'].mean()}")
print(f"Max of C: {df['C'].max()}\n")

# Example 4: Filtering and querying
print("Example 4: Filtering data")
df = pd.DataFrame({
    'Product': ['Apple', 'Banana', 'Orange', 'Mango', 'Grape'],
    'Price': [1.5, 0.8, 2.0, 3.5, 2.5],
    'Quantity': [100, 150, 80, 50, 120]
})
print("Original:")
print(df)
print("\nPrice > 2.0:")
print(df[df['Price'] > 2.0])
print("\nQuantity > 100 and Price < 3.0:")
print(df[(df['Quantity'] > 100) & (df['Price'] < 3.0)])
print("\nUsing query method:")
print(df.query('Price >= 2.0 and Quantity < 100'))
print()

# Example 5: GroupBy operations
print("Example 5: GroupBy operations")
df = pd.DataFrame({
    'Department': ['IT', 'HR', 'IT', 'Finance', 'HR', 'IT', 'Finance'],
    'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace'],
    'Salary': [50000, 45000, 60000, 55000, 48000, 58000, 52000]
})
print("Original:")
print(df)
print("\nGroup by Department - Mean salary:")
print(df.groupby('Department')['Salary'].mean())
print("\nGroup by Department - Count:")
print(df.groupby('Department').size())
print("\nGroup by Department - Multiple aggregations:")
print(df.groupby('Department')['Salary'].agg(['mean', 'min', 'max', 'count']))
print()

# Example 6: Handling missing data
print("Example 6: Handling missing data")
df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [10, np.nan, 30, np.nan, 50],
    'C': [100, 200, 300, 400, 500]
})
print("Original with NaN:")
print(df)
print("\nCheck for missing values:")
print(df.isnull().sum())
print("\nDrop rows with NaN:")
print(df.dropna())
print("\nFill NaN with 0:")
print(df.fillna(0))
print("\nFill NaN with mean:")
print(df.fillna(df.mean()))
print()

# Example 7: Merging and joining DataFrames
print("Example 7: Merging DataFrames")
df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    'Name': ['Alice', 'Bob', 'Charlie', 'David']
})
df2 = pd.DataFrame({
    'ID': [1, 2, 3, 5],
    'Salary': [50000, 60000, 55000, 48000]
})
print("DataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)
print("\nInner merge:")
print(pd.merge(df1, df2, on='ID', how='inner'))
print("\nLeft merge:")
print(pd.merge(df1, df2, on='ID', how='left'))
print("\nOuter merge:")
print(pd.merge(df1, df2, on='ID', how='outer'))
print()

# Example 8: Sorting and ranking
print("Example 8: Sorting data")
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 22, 28, 35],
    'Score': [85, 92, 78, 88, 95]
})
print("Original:")
print(df)
print("\nSort by Age:")
print(df.sort_values('Age'))
print("\nSort by Score (descending):")
print(df.sort_values('Score', ascending=False))
print("\nSort by multiple columns:")
print(df.sort_values(['Age', 'Score'], ascending=[True, False]))
print()

# Example 9: Pivot tables and cross-tabulation
print("Example 9: Pivot tables")
df = pd.DataFrame({
    'Date': ['2023-01', '2023-01', '2023-02', '2023-02', '2023-03', '2023-03'],
    'Product': ['A', 'B', 'A', 'B', 'A', 'B'],
    'Sales': [100, 150, 120, 140, 110, 160],
    'Region': ['East', 'West', 'East', 'West', 'East', 'West']
})
print("Original:")
print(df)
print("\nPivot table - Sales by Date and Product:")
pivot = df.pivot_table(values='Sales', index='Date', columns='Product', aggfunc='sum')
print(pivot)
print("\nPivot table with multiple aggregations:")
pivot2 = df.pivot_table(values='Sales', index='Region', columns='Product', aggfunc=['sum', 'mean'])
print(pivot2)
print()

# Example 10: String operations and datetime handling
print("Example 10: String and datetime operations")
df = pd.DataFrame({
    'Name': ['alice smith', 'BOB JONES', 'Charlie Brown'],
    'Email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'Date': ['2023-01-15', '2023-02-20', '2023-03-25']
})
print("Original:")
print(df)
print("\nString operations:")
df['Name_Upper'] = df['Name'].str.upper()
df['Name_Title'] = df['Name'].str.title()
df['Email_Domain'] = df['Email'].str.split('@').str[1]
print(df)
print("\nDatetime operations:")
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day_Name'] = df['Date'].dt.day_name()
print(df)
