import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 

parser = argparse.ArgumentParser()
parser.add_argument("--years", default="200", type=int, help="select the duration time of the simulation")
args = parser.parse_args()

bck = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]
res = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
data = []
date = [10, 20, 30, 40, 50, 60, 70, 80, 90]
time = args.years
num_el = 0


for x in range(len(bck)):
    for y in range(len(res)):
        data.append(pd.read_csv("csv/csv_combination/perc_result_bkc"+str(bck[x])+"_res"+str(res[y])+".csv"))
        if len(data) == 1:
            print(str(bck[x]) + " " + str(res[y]))
            print(data[0])
        data[len(data)-1] = data[len(data)-1].groupby([ 'years', 'n_h_pr'], as_index=False).agg({ 'avg_backup':'mean', 'avg_restore':'mean'})

plt.rcParams.update({'font.size': 10})
fig, axes = plt.subplots(nrows=len(bck), ncols=len(res), figsize=(4, 4))


avg_m_bck = []
avg_m_res = []

for x in range(len(bck)):
    for y in range(len(res)):
        plot = data[num_el][data[num_el]["years"] == time]
        plot = plot.sort_values(by="n_h_pr")
        axes[x][y].plot(plot['n_h_pr'], plot['avg_backup'], "-b",  label = "Avg % Backed Up High-P")
        axes[x][y].plot(plot['n_h_pr'], plot['avg_restore'], "-r", label = "Avg % To Restore High-P")
        num_el+=1
        axes[x][y].set_title("Bck:" + str(bck[x]) + " Sto: " + str(res[y]), fontsize=10)

fig.tight_layout(pad=5.0)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.8)
plt.suptitle("Years = " + str(time))
plt.show()

