import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 

#PLOT only the graph that is out when we esecute the original
#system, this will mean when high piority server = 0


data = pd.read_csv("csv/csv_time/result_bkc_res.csv")
data = data.groupby([ 'years', 'h_pr_per'], as_index=False).agg({ 'per_no_pr_loss':'mean', 'per_pr_loss':'mean'})


plt.rcParams.update({'font.size': 20})
plot = data[data['h_pr_per']==0]
plt.plot(plot["years"], plot["per_no_pr_loss"])
plt.xlabel("Time")
plt.ylabel("Data loss")
plt.title("High priority server percentage = 0")

plot.show()
