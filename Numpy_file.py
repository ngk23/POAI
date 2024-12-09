import numpy as np

np.random.seed(0)
rows, cols = 20, 5

def generate_array():
    while True:
        array = np.random.randint(10, 100, size=(rows, cols))
        row_sums = array.sum(axis=1)
        total_sum = array.sum()

        for i in range(rows):
            if row_sums[i] % 2 != 0:
                array[i, 0] += 1 if not array[i, 0] % 2 == 0 else -1

        row_sums = array.sum(axis=1)
        total_sum = array.sum()
        if total_sum % 5 != 0:
            adjustment = 5 - (total_sum % 5)
            array[0, 0] += adjustment
            total_sum = array.sum()
        if all(i % 2 == 0 for i in row_sums) and total_sum % 5 == 0:
            return array

array = generate_array()
print("Generated Array:")
print(array)

divisible_by_3_and_5 = array[(array % 3 == 0) & (array % 5 == 0)]
print("\nDivisible by both 3 and 5 elements:")
print(divisible_by_3_and_5)

mean_value = array.mean()
array[array > 75] = mean_value
print("\nReplacing elements greater than 75 with mean:")
print(array)

mean = array.mean()
print("Mean of the array:", mean)

std_dev = array.std()
print("Standard deviation of the array:", std_dev)

median = np.median(array)
print("Median of the array:", median)

variance_per_column = array.var(axis=0)
print("Each column has the variance value as follows:")
print(variance_per_column)
