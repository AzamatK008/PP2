filename = "sample.txt"

# Write to file (w)
with open(filename, "w") as file:
    file.write("Apple\n")
    file.write("Banana\n")
    file.write("Cherry\n")

print("File written successfully.")

# Append to file (a)
with open(filename, "a") as file:
    file.write("Date\n")
    file.write("Elderberry\n")

print("Data appended successfully.")