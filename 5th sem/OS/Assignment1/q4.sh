# Write a shell script to count the number of ordinary files (not directories) in the current
# working directory and its subdirectories.
#!/bin/bash
BASE_PATH="C:\Users\user1\Desktop\JU CSE 2021-2025\CSE UG-3\5th sem\OS"

if [ -d "$BASE_PATH" ]; then
  echo "Path exists"
else
  echo "Path does not exist"
  exit 1
fi

# Use the find command to count files recursively
FILES_COUNT=$(find "$BASE_PATH" -type f | wc -l)

echo "Total number of files: $FILES_COUNT"