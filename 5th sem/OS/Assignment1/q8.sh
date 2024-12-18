# Write a shell script that accepts a filename as an input and performs the following activities on the given file. 
#The program asks for a string of characters (that is, any word) to be provided by the user. 
#The file will be searched to find whether it contains the given word. If the file contains the given word, 
#the program will display (a) the number of occurrences of the word. The program is also required to display 
#(b) the line number in which the word has occurred and no. of times the word has occurred in that line 
#(Note: the word may occur more than once in a given line).
#If the file does not contain the word, an appropriate error message will be displayed.

#! /bin/bash
argc=$#
if [ $argc -eq 0 ]
then
    echo "NO INPUT"
elif [ $argc -eq 2 ]
then
    echo "MORE THAN 1 INPUT"
else
    FNAME=$1
    if ! [ -f $FNAME ]
    then
        echo "File Doesnt Exist, invalid input"
    else
        echo -n "Enter the word to find: "
        read str

        linecnt=`wc -l < $FNAME`
        echo "Number of lines in file: $linecnt"
        echo "No of lines having string \"$str\": `grep -w $str $FNAME | wc -l`"
        for (( i=1; i<=$linecnt; i++ ))
        do
            cnt=`awk "NR==$i {print}" $FNAME | grep -o -w $str | wc -l`
            if [ $cnt -ne 0 ]
            then
                echo "count in line $i: $cnt"
            fi
        done
    fi
fi