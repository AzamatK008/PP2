import shutil
import os

source = "sample.txt"
destination_dir = "data/files"

# Copy file
shutil.copy(source, destination_dir)
print("File copied to directory.")

# Move file
shutil.move(source, destination_dir)
print("File moved to directory.")