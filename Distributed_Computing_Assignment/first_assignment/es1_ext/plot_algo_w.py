import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 
 
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--csv_file", help = "csv where i can read data", default = "out_w.csv")
args = parser.parse_args()

splitTitle = args.csv_file.split("_")

data = pd.read_csv(args.csv_file)
data_arr = []

for x in range(1, 6):
    data_arr.append(data.loc[data["algo"] == x].groupby(["algo"])["w"].mean())


data= data.groupby(["algo"], as_index = False)["w"].mean()
plt.suptitle("Number of Servers = " + str(splitTitle[4]), fontsize = 14)
plt.bar(data["algo"], data["w"])
plt.xlabel("Algorithm Number")
plt.ylabel("W Average")
plt.show()
