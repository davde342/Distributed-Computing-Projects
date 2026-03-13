import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 



bck = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
res = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
high = [10, 20, 30, 40, 50, 60, 70, 80, 90]
time = 50 
data = []
num_el = 0


for x in range(len(bck)):
    for y in range(len(res)):
        data.append(pd.read_csv("csv_ext/perc_result_bkc"+str(bck[x])+"_res"+str(res[y])+".csv"))
        if len(data) == 1:
            print(str(bck[x]) + " " + str(res[y]))
            print(data[0])
        data[len(data)-1] = data[len(data)-1].groupby([ 'years', 'n_h_pr'], as_index=False).agg({ 'avg_backup':'mean', 'avg_restore':'mean'})

plt.rcParams.update({'font.size': 10})

avg_back = {}
avg_res = {}
avg_m = []

for x in range(len(bck)):
    for y in range(len(res)):
        plot = data[num_el][data[num_el]["years"] == time]
        plot = plot.sort_values(by="n_h_pr")
        # group by the number of high priority value
        # and save the result inside the avg_back e av_res list
        for z in high:
            avg_back[str(z)] = []
            avg_res[str(z)] = []
            tmp_back = plot[plot['n_h_pr'] == z]['avg_backup']
            tmp_res = plot[plot['n_h_pr'] == z]['avg_restore']
            avg_back[str(z)].append(tmp_back)
            avg_res[str(z)].append(tmp_res)
        num_el+=1

plt.plot(res, [max(avg_back[str(x)]) - min(avg_back[str(x)]) for x in high], "-r")
plt.plot(res, [max(avg_res[str(x)]) - min(avg_res[str(x)]) for x in high], "-b")

plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.8)
plt.suptitle("Years = " + str(time))
plt.show()
