#!/bin/bash

for i in {1..5}
do
   python Main.py 22 100 & a[$i]=$!
   python Main.py 24 100 & a[$i+5]=$!
   python Main.py 26 100 & a[$i+10]=$!
done

for i in {16..20}
do
   python Main.py 23 100 & a[$i]=$!
   python Main.py 25 100 & a[$i+20]=$!
done

echo "pid" >> log.txt
echo ${a[@]} >> log.txt
wait
echo 'all complete!' >> log.txt
