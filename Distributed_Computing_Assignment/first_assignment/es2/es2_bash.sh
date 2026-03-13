#!/bin/bash

DIR="csv2"

if [ -d $DIR ]; then
	echo "delete dir $DIR"
	rm -rd $DIR
fi

echo "create $DIR"
mkdir $DIR

for d in 1 2 5 10; do
	FILENAME="${DIR}/result_${d}.csv"
	for lambda in 0.5 0.9 0.95 0.99; do 
		echo "eseguo queue_sim con d = $d e lambda = $lambda"
		python3 queue_sim.py --d $d --lambd $lambda --csv_ql $FILENAME &
		echo "finita esecuzione, salvati dati in: $FILENAME"
	done
done

while [ $(jobs | wc -l) -gt 1 ]; do
	echo "rimangono $(jobs | wc -l)"
done

for d in 1 2 5 10; do
	FILENAME="${DIR}/result_${d}.csv"
	echo "d,lambda,perc,length" | cat - $FILENAME > temp && mv temp $FILENAME
done


