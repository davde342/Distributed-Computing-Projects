import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 
  
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--csv_file", help = "csv where i can read data", default = "out_qlcsv")
args = parser.parse_args()

data = pd.read_csv(args.csv_file)
data_arr = []

for x in range(1, 6):
    data_arr.append(data.loc[data["algo"] == x].groupby([ "number_row"])["%"].mean())


plt.rcParams.update({'font.size': 20})

plt.plot([x for x in range(len(data_arr[0]))], data_arr[0], "-r",  linestyle="dashed",label = "first function" )
plt.plot([x for x in range(len(data_arr[1]))], data_arr[1], "-b",linestyle="dashed" , label ="second function")
plt.plot([x for x in range(len(data_arr[2]))], data_arr[2], "-m", linestyle="dashed", label ="third function" )
plt.plot([x for x in range(len(data_arr[3]))], data_arr[3], "-y", linestyle="dashed", label ="fourth function" )
plt.plot([x for x in range(len(data_arr[4]))], data_arr[4], "-g", linestyle="dashed", label ="fifth function")

plt.legend()
plt.xlim(0, 40)
plt.title("Graph of length")
plt.ylabel("Franctions of queues with at least that size")
plt.xlabel("Queue Length")

plt.show()


