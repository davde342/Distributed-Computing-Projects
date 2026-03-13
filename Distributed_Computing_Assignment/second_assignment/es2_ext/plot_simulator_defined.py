import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 

#PLOT only the graphs for different time with the perc_backup perc_storage
#setup by program and not by user

time = [50, 100, 150, 200, 250]

num_el = 0
data = pd.read_csv("csv/csv_time/result_bkc_res.csv")
data = data.groupby([ 'years', 'h_pr_per'], as_index=False).agg({ 'per_no_pr_loss':'mean', 'per_pr_loss':'mean'})



for x in range(len(time)):
    plt.subplot(5, 1, num_el+1) 
    plot = data[data["years"] == time[x]]
    plot = plot.sort_values(by="h_pr_per")
    plt.plot(plot['h_pr_per'], plot['per_no_pr_loss'], "-b", label="Low-Pr %")
    plt.plot(plot['h_pr_per'], plot['per_pr_loss'], "-r" , label="High-Pr %")
    plt.plot(plot['h_pr_per'], plot['per_pr_loss'] + plot['per_no_pr_loss'], "-m" , label="Overall")
    plt.xlabel("High Priority Server Percentage")
    plt.ylabel("Avg % Data Loss")
    num_el+=1
    plt.title(time[x])
    plt.legend(loc  ="upper right")
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.8)
plt.suptitle("Data Loss % For Years = " + str(time))
plt.show()
plt.rcParams.update({'font.size': 20})



