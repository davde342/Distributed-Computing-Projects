import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 

perc = [10, 20, 30, 40, 50, 60, 70, 80, 90]
time = [50, 100, 150, 200, 250, 300, 350, 400] 
num_el = 0

data = pd.read_csv("csv/csv_combination/perc_result_bkc0.5_res0.5.csv")

avg_back = {}
avg_res = {}
avg_m = []

pos=0

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(4, 4))

z = 0

for y in range(4):
    for x in range(2):
        plot = data[data["years"] == time[z]]
        plot = plot.sort_values(by="n_h_pr")
        axes[x][y].plot(plot['n_h_pr'], plot['avg_backup'], "-b", label="Average Backed Up % Blocks")
        axes[x][y].plot(plot['n_h_pr'], plot['avg_restore'], "-r",label= "Average To Store % Block")
        axes[x][y].set_title(str(time[pos]))
        pos+=1
        axes[x][y].legend(loc="upper right")
        axes[x][y].set_ylabel("%")
        axes[x][y].set_xlabel("% Priority Server")
        z += 1

plt.suptitle("Years = " + str(time))
plt.ylim(0, 0.1)
plt.show()

