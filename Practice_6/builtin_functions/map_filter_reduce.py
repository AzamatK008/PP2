from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map()
squares = list(map(lambda x: x * x, numbers))
print("Squares:", squares)

# filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)

# reduce()
product = reduce(lambda a, b: a * b, numbers)
print("Product:", product)

# Built-in aggregates
print("Sum:", sum(numbers))
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Sorted descending:", sorted(numbers, reverse=True))