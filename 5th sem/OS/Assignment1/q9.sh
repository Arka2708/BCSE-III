#Extend the shell script written in (8) to perform the following task: 
#User is asked to enter two different patterns or words. 
#The first pattern will have to be matched with the contents of the file and 
#replaced by the second pattern if a match occurs. 
#If the first pattern does not occur in the file, an appropriate error message will be displayed.
#! /bin/bash
argc=$#
if [ $argc -eq 0 ]; then
    echo "NO INPUT"
elif [ $argc -eq 2 ]; then
    echo "MORE THAN 1 INPUT"
else
    FNAME=$1
    if ! [ -f $FNAME ]; then
        echo "File Doesnt Exist, invalid input"
    else
        echo -n "Enter the word to find: "
        read str
        echo -n "Enter the second word to replace with: "
        read str2

        linecnt=`wc -l < $FNAME`
        echo "Number of lines in file: $linecnt"
        echo "No of lines having string \"$str\": `grep -w $str $FNAME | wc -l`"
        for (( i=1; i<=$linecnt; i++ ))
        do
            cnt=`awk "NR==$i {print}" $FNAME | grep -o -w $str | wc -l`
            if [ $cnt -ne 0 ]; then
                echo "count in line $i: $cnt"
            fi
        done
        if grep -q "$str" "$FNAME"; then
            # Perform the replacement using sed
            sed -i "s/$str/$str2/g" "$FNAME"
            echo "Replaced '$str' with '$str2' in the file."
        else
            echo "The pattern '$str' was not found in the file."
        fi
    fi
fi