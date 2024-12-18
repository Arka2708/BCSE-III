# Write a shell script called birthday_match.sh that takes two birthdays of the form DD/MM/YYYY and 
# returns whether there is a match if the two people were born on the same day of the week(eg:- Friday)

#! /bin/bash
read -p "Enter the First Birthday:" u1
read -p "Enter the Second Birthday:" u2

d1=$(date -d "$u1" "+%A")
d2=$(date -d "$u2" "+%A")
if [ "$d1" = "$d2" ]; then
    echo "Born on Same Day -" $d1
else
    echo "Born on Different Day - " $d1   $d2 
fi