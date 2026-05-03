filename = "sample.txt"

# read()
with open(filename, "r") as file:
    content = file.read()
    print("Using read():")
    print(content)

# readline()
with open(filename, "r") as file:
    print("Using readline():")
    print(file.readline())

# readlines()
with open(filename, "r") as file:
    lines = file.readlines()
    print("Using readlines():")
    print(lines)