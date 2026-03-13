import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 


## SCRIPT FOR PLOT ALL THE POSSIBLE DATA LOSS COMBINATION
## IN A SELECT YEARS, FOR COMBINATION IT MEANS ALL THE POSSIBLE 
## BACKUP % AND  RESTORE % FOR EVERY % OF HIGH PRIORITY 
## SERVER 

parser = argparse.ArgumentParser()
parser.add_argument("--years", default="200", type=int, help="select the duration time of the simulation")
args = parser.parse_args()

bck = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
res = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
data = []
time = args.years
num_el = 0

for x in range(len(bck)):
    for y in range(len(res)):
        data.append(pd.read_csv("csv/csv_combination/result_bkc"+str(bck[x])+"_res"+str(res[y])+".csv"))
        data[len(data)-1]['per_no_pr_loss']= data[len(data)-1]['per_no_pr_loss'].astype(float)
        data[len(data)-1]['per_pr_loss'] = data[len(data)-1]['per_pr_loss'].astype(float)
        data[len(data)-1] = data[len(data)-1].groupby([ 'years', 'h_pr_per'], as_index=False).agg({ 'per_no_pr_loss':'mean', 'per_pr_loss':'mean'})

plt.rcParams.update({'font.size': 10})
fig, axes = plt.subplots(nrows=len(bck), ncols=len(res), figsize=(4, 4))
print(data[0])

for x in range(len(bck)):
    for y in range(len(res)):
        plot = data[num_el][data[num_el]["years"] == time]
        plot = plot.sort_values(by="h_pr_per")
        axes[x][y].plot(plot['h_pr_per'], plot['per_no_pr_loss'], "-b",  label="Low-Pr %")
        axes[x][y].plot(plot['h_pr_per'], plot['per_pr_loss'], "-r",  label="High-Pr %")
        axes[x][y].plot(plot['h_pr_per'], plot['per_pr_loss'] +  plot['per_no_pr_loss'], "-m",  label="Overall")
        num_el+=1
        axes[x][y].set_title("Bck:" + str(bck[x]) + " Sto: " + str(res[y]), fontsize=10)
        axes[x][y].set_ylim([0,1])
#        axes[x][y].legend(loc="upper right")
        axes[x][y].set_ylabel("Data Loss %")
        axes[x][y].set_xlabel("% Priority Server")
fig.tight_layout(pad=5.0)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.8)
plt.suptitle("Years = " + str(time))
plt.show()




