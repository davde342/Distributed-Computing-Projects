#!/bin/bash

DIR="csv3"

if [ -d $DIR ]; then
	echo "delete dir $DIR"
	rm -rd $DIR
fi

echo "create dir $DIR"
mkdir $DIR

for d in 1 2 5 10; do
		for lambda in 0.5 0.99; do 
			FILENAME="${DIR}/result_${d}_${lambda}.csv"
			for w in 0.25 0.5 0.75 1.0 1.25 1.5; do
				python3 queue_sim_wei.py --d $d --lambd $lambda  --csv_ql $FILENAME --shape ${w} &
			done
	done
done		


while [ $(jobs | wc -l) -gt 1 ]; do
	echo "rimangono $(jobs | wc -l)"
done

for d in 1 2 5 10; do
	for lambda in 0.5 0.99; do 
		FILENAME="${DIR}/result_${d}_${lambda}.csv"
		echo "shape,d,lambda,perc,length" | cat - $FILENAME > temp && mv temp $FILENAME 
	done
done		


