#Write a shell script to count the number of lines in a file.

#! /bin/bash
lines=0
file="test.txt"
if [ -e "$file" ]; then
  while read line; do
   lines=$(($lines+1))
  done < "$file"
  echo "No. of lines in file: $lines"
else
  echo "File not found: $file"
fi
