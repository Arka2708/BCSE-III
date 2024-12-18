# Write a shell program to duplicate the UNIX rm command with the following features:

# a. Instead of deleting the files , it will move them to a my-deleted-files directory. 
# If the file already exists in the my-deleted-files directory then the existing file(in the my-deleted-files)
# will have the version 0 appended to it and the newly deleted file will have version number one a
# appended to it.

#! /bin/bash
argc=$#
if [ $argc -eq 0 ]; then
    echo "NO INPUT"
elif [ $argc -eq 2 ]; then
    echo "MORE THAN 1 INPUT"
else
    REC_BIN="./my_deleted_files"
    if [ $1 == "-c" ]; then
        if ! [ -d $REC_BIN ]; then
            echo "Recycle bin doesnt exist, so it is already empty!"
        else
            echo "Recycle bin exists"
            #clear it
            echo "Are u sure u want to clear? (Y/N)"
            read conf
            if [ $conf == "Y" ]
            then
                rm -rf $REC_BIN
            fi
        fi
    else
        FNAME=$1
        if ! [ -f $FNAME ]; then
            echo "File Doesnt Exist, invalid input"
        else
            if ! [ -d $REC_BIN ]; then
                echo "Recycle bin not exist, created!"
                mkdir -p $REC_BIN
                mv $FNAME $REC_BIN"/"$FNAME
                echo "File deleted"
            else
                echo "Recycle bin exists"
                if [ -f $REC_BIN"/"${FNAME%.*}"(0)."${FNAME##*.} ]; then
                    count=0
                    while [ -f $REC_BIN"/"${FNAME%.*}"("$count")."${FNAME##*.} ]
                    do
                         count=$(($count + 1))
                    done
                    newFNAME=${FNAME%.*}"("$count")."${FNAME##*.}
                    mv $FNAME $REC_BIN"/"$newFNAME
                elif [ -f $REC_BIN"/"$FNAME ]; then
                    mv $REC_BIN"/"$FNAME $REC_BIN"/"${FNAME%.*}"(0)."${FNAME##*.}
                    mv $FNAME $REC_BIN"/"${FNAME%.*}"(1)."${FNAME##*.}
                else
                    mv $FNAME $REC_BIN"/"$FNAME
                fi
                echo "File deleted"
            fi
        fi
    fi
fi