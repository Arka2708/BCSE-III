# Write a shell script multiplication_table that will generate a multiplication table for a number given on the command line

#! /bin/bash
read -p "Enter the number:" n
i=1
while [ $i -le 10 ]
do
res=`expr $i \* $n`
echo "$n * $i= $res"
((++i))
done
