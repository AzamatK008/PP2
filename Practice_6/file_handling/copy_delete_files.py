import shutil
import os

source = "sample.txt"
backup = "sample_backup.txt"

# Copy file
shutil.copy(source, backup)
print("File copied successfully.")

# Safe delete
if os.path.exists(backup):
    os.remove(backup)
    print("Backup file deleted.")
else:
    print("File does not exist.")