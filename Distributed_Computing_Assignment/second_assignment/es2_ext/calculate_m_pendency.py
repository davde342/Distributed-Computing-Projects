import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 

bck = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]
res = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
data = []
date = [10, 20, 30, 40, 50, 60, 70, 80, 90]
time = [50, 100, 150, 200, 250]


for x in range(len(bck)):
    for y in range(len(res)):
        data.append(pd.read_csv("csv/csv_combination/perc_result_bkc"+str(bck[x])+"_res"+str(res[y])+".csv"))
        data[len(data)-1] = data[len(data)-1].groupby([ 'years', 'n_h_pr'], as_index=False).agg({ 'avg_backup':'mean', 'avg_restore':'mean'})

plt.rcParams.update({'font.size': 10})
fig, axes = plt.subplots(nrows=len(bck), ncols=len(res), figsize=(4, 4))


avg_m_bck = {}
avg_m_res = {}

for z in range(len(time)):
    num_el = 0
    for x in range(len(bck)):
        for y in range(len(res)):
            avg_m_bck[time[z]] = []
            avg_m_res[time[z]] = []

            plot = data[num_el][data[num_el]["years"] == time[z]]
            plot = plot.sort_values(by="n_h_pr")
            
            f =  float(plot[plot['n_h_pr'] == 80]['avg_backup']) - float(plot[plot['n_h_pr'] == 10]['avg_backup']) 
            r =     80 - 10 
            avg_m_bck[time[z]].append(f/r)

             
            f =  float(plot[plot['n_h_pr'] == 80]['avg_restore']) - float(plot[plot['n_h_pr'] == 10]['avg_restore']) 
            r =     80 - 10 
            avg_m_res[time[z]].append(f/r)

            axes[x][y].plot(plot['n_h_pr'], plot['avg_backup'], "-b",  label = "Avg % Backed Up High-P")
            axes[x][y].plot(plot['n_h_pr'], plot['avg_restore'], "-r", label = "Avg % To Restore High-P")
            num_el+=1
            axes[x][y].set_title("Bck:" + str(bck[x]) + " Sto: " + str(res[y]), fontsize=10)

final_bck = []
final_res = []
for z in range(len(time)):
    final_bck.append(sum(avg_m_bck[time[z]])/len(avg_m_bck[time[z]]))
    final_res.append(sum(avg_m_res[time[z]])/len(avg_m_res[time[z]]))
print("slope for backup: ", sum(final_bck)/len(final_bck))
print("slope for restore: ", sum(final_res)/len(final_res))


