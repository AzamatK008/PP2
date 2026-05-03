names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 88]

# enumerate()
for index, name in enumerate(names):
    print(index, name)

# zip()
for name, score in zip(names, scores):
    print(name, "scored", score)

# Type checking
x = 10
y = "20"

print(type(x))
print(type(y))

# Type conversion
y_int = int(y)
print("Converted y:", y_int, type(y_int))