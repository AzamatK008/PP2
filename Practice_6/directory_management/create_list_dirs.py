import os

# Create nested directories
os.makedirs("data/files", exist_ok=True)
print("Directories created.")

# Current working directory
print("Current directory:", os.getcwd())

# List directory contents
print("Contents of current directory:")
print(os.listdir())