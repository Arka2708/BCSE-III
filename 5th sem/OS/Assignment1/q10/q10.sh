#! /bin/bash

gcc common.c -o common
gcc option1.c -o option1
gcc option2.c -o option2
gcc option3.c -o option3
gcc option4.c -o option4

while true; do
    echo "[1] Display greetings [2] List large files [3] Disk usage [4] View Log File [5] Exit"
    echo -n "Your choice > "
    read choice

    case $choice in
        1)
            ./option1
            ./common 1
            ;;
        2)
            ./option2
            ./common 2
            ;;
        3)
            ./option3
            ./common 3
            ;;
        4)
            ./option4
            ./common 4
            ;;
        5)
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter a number between 1 and 5."
            ;;
    esac
done