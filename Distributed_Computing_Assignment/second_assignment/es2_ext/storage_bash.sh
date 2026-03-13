#!/bin/bash

#################################################################################
#																																								#
#-VARIABLE 																																			#
#																																								#
#################################################################################

#################################################################################
#-DIR VARIABLE																																	#
#################################################################################

DIR="csv"
DIR_TIME="${DIR}/csv_time"
DIR_COMBINATION="${DIR}/csv_combination"

#################################################################################
#-ARRAY VARIABLE																															  #
#################################################################################

FILE_YEARS_ARRAY=(50 100 150 200 250 300 350 400)
FILE_PERC_ARRAY_BCK=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
FILE_PERC_ARRAY_RES=(0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9)
FILE_SERVER_PERC=(0 10 20 30 40 50 60 70 80 90)

#################################################################################
#-RUN VARIABLE																															    #
#################################################################################

RUN_COMBINATION=1
RUN_TIME=1

#################################################################################
#-HEADER VARIABLE																															  #
#################################################################################

FILE_HEADER="years,h_pr_per,per_no_pr_loss,per_pr_loss"
FILE_HEADER_PERC="years,n_h_pr,per_bck,per_res,avg_backup,avg_restore"

#################################################################################
#																																								#
#-PROGRAM                                                                       #
#																																								#
#################################################################################

## DELETE THE DIRECTORY csv AND RECREATEIT WITH csv_time and csv_combination INSIDE IT

if [ ! -d $DIR ]; then
	mkdir -p $DIR $DIR_TIME $DIR_COMBINATION
else 
	if [ ! -d $DIR_COMBINATION ]; then
		mkdir -p $DIR_COMBINATION
	fi
	if [ ! -d $DIR_TIME ]; then
		mkdir -p $DIR_TIME
	fi

	sed -i '/years,h_pr_per,per_no_pr_loss,per_pr_loss/d'  csv/csv_combination/*.csv
	sed -i '/years,n_h_pr,per_bck,per_res,avg_backup,avg_restore/d'  csv/csv_combination/*.csv
	sed -i '/years,n_h_pr,per_bck,per_res,avg_backup,avg_restore/d'  csv/csv_time/*.csv
	sed -i '/years,h_pr_per,per_no_pr_loss,per_pr_loss/d'  csv/csv_time/*.csv                
fi 


##################################################################################
##-POPULATE_CSV_COMBINATION_DIR																									#
##################################################################################

echo "Make All The Execution With backup % and restore % set manual"
#
for (( r=0; r< $RUN_COMBINATION; r++ )); do
	for perc in  ${FILE_SERVER_PERC[@]}; do
		for years in "${FILE_YEARS_ARRAY[@]}"; do
			for per_restore in "${FILE_PERC_ARRAY_RES[@]}"; do
				for per_backup in "${FILE_PERC_ARRAY_BCK[@]}"; do
					FILENAME="${DIR_COMBINATION}/result_bkc${per_backup}_res${per_restore}.csv"
					FILENAME_PERC="${DIR_COMBINATION}/perc_result_bkc${per_backup}_res${per_restore}.csv"
					python3 storage.py p2p.cfg --high_priority_per $perc --csv_file $FILENAME --csv_perc $FILENAME_PERC --per_restore $per_restore --per_backup $per_backup --max-t "${years} years"  & 
				done
			done

		while [ $(jobs | wc -l) -gt 1 ]; do
			echo "-{1} [$perc || $years]  $(($(jobs | wc -l)))"
		done
		
		done
	done

done

while [ $(jobs | wc -l) -gt 1 ]; do
	echo "-{1} [$perc || $years]  $(($(jobs | wc -l)))"
done

#################################################################################
#-ADD_HEADER_TO_CSV_IN_COMBINATION_DIR																					#
#################################################################################

echo "Add header to all the file that are saved in the following dir: $DIR"

for per_backup in  "${FILE_PERC_ARRAY_BCK[@]}" ; do
		for per_restore in "${FILE_PERC_ARRAY_RES[@]}";  do
			FILENAME_PERC="${DIR_COMBINATION}/perc_result_bkc${per_backup}_res${per_restore}.csv"
			FILENAME="${DIR_COMBINATION}/result_bkc${per_backup}_res${per_restore}.csv"
			echo "result: $FILENAME "
			echo "per: $FILENAME_PERC"
			echo  $FILE_HEADER | cat - $FILENAME > temp && mv temp $FILENAME 
			echo  $FILE_HEADER_PERC | cat - $FILENAME_PERC > temp && mv temp $FILENAME_PERC 
			
		done
done

#################################################################################
#-POPULATE_CSV_TIME_DIR                                                         #
#################################################################################

echo "We run the for a $RUN_TIME the same simulator but with the % restore and % backup setted by the simulator itself"

FILENAME="${DIR_TIME}/result_bkc_res.csv"
FILENAME_PERC="${DIR_TIME}/perc_result_bkc_res.csv"
for (( r=0; r<$RUN_TIME; r++ )); do
	for perc in  ${FILE_SERVER_PERC[@]}; do
		for years in "${FILE_YEARS_ARRAY[@]}"; do
					python3 storage.py p2p.cfg --high_priority_per $perc --csv_file $FILENAME --csv_perc $FILENAME_PERC --auto_per 1 --max-t "${years} years"  & 
		done
	done			
	while [ $(jobs | wc -l) -gt 1 ]; do
			echo "-{2} [$perc || $years]  $(($(jobs | wc -l)))"
	done
done

while [ $(jobs | wc -l) -gt 1 ]; do
	echo "-{2} [$perc || $years]  $(($(jobs | wc -l)))"
done

#################################################################################
#-ADD_HEADER_TO_CSV_IN_TIME_DIR																					        #
#################################################################################

echo "Add header to all the file that are saved in the following dir: $DIR"

FILENAME="${DIR_TIME}/result_bkc_res.csv"
FILENAME_PERC="${DIR_TIME}/perc_result_bkc_res.csv"

echo  $FILE_HEADER | cat - $FILENAME > temp && mv temp $FILENAME 
echo  $FILE_HEADER_PERC | cat - $FILENAME_PERC > temp && mv temp $FILENAME_PERC 




