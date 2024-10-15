#!/bin/bash

for i in {1..2}
do
   python Main.py 11 100 10 2 & a[$i]=$!
done

for i in {3..4}
do
   python Main.py 9 100 1 2 & a[$i]=$!
done

for i in {5..6}
do
   python Main.py 11 100 1 2 & a[$i]=$!
done

for i in {7..8}
do
   python Main.py 11 100 5 2 & a[$i]=$!
done

for i in {9..10}
do
   python Main.py 6 100 1 2 & a[$i]=$!
done

for i in {11..12}
do
   python Main.py 4 100 1 0 & a[$i]=$!
done

echo "pid" >> log.txt
echo ${a[@]} >> log.txt
wait
echo 'all complete!' >> log.txt
