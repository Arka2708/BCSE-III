#! /bin/bash

#Write a shell script that has 2 user created variables, uv1 and uv2.
#Ask for the valus of the variables from the user and take in any values
#(real/integer/character) for the 2 variables.Print them as:
#(i)value of uv1 followed by value of uv2 separated by comma and
#(ii)value of uv2 followed by value of uv1 separated by the word "and"

read -p "Enter the variable 1:" uv1
read -p "Enter the variable 2:" uv2
echo $uv1","$uv2
echo $uv1 "and" $uv2