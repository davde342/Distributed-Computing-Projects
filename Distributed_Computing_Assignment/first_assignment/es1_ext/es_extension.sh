#!/bin/bash


DIR="csv_extension"

FILE_SERVER_W="${DIR}/file_w_out"
FILE_SERVER_L="${DIR}/file_ql_out"

if [ -d $DIR ]; then
	rm -rd $DIR
fi
mkdir $DIR


for i in {1}; do
	for algo in {1..5}; do
		for n_server in  5 10 15 20 25 30; do
			for lambda in 0.5 0.99; do
				if [ $algo -eq 5 ]; then
					./queue_prof_sim.py --lambd $lambda   --n $n_server --csv_ql "${FILE_SERVER_L}_${n_server}_${lambda}.csv"   --csv_w "${FILE_SERVER_W}_${n_server}_${lambda}.csv" &
				else
					./queue_sim.py --lambd $lambda  --algo $algo --n $n_server --csv_ql "${FILE_SERVER_L}_${n_server}_${lambda}.csv"   --csv_w "${FILE_SERVER_W}_${n_server}_${lambda}.csv" &
				fi
			done
		done
	done
	while [ $(jobs | wc -l) -gt 1 ]; do
		echo "[LAP: $i || ALGO: $algo] remains $( jobs| wc -l)"
	done
done


for x in 5 10 15 20 25 30; do
	for lambda in 0.5  0.99; do
		echo 'algo,lambd,n,w' | cat - "${FILE_SERVER_W}_${x}_${lambda}.csv" > temp && mv temp "${FILE_SERVER_W}_${x}_${lambda}.csv"
		echo 'algo,lambd,%,number_row' | cat - "${FILE_SERVER_L}_${x}_${lambda}.csv"  > temp && mv temp "${FILE_SERVER_L}_${x}_${lambda}.csv"
	done
done


