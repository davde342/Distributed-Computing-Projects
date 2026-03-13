import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 


data = []

name_file = ["1", "2", "5", "10"]

for x in range(4):
    print("take data from file: csv2/result_" + str(name_file[x])+".csv")
    data.append(pd.read_csv("csv2/result_"+str(name_file[x])+".csv"))

    
for x in range(len(name_file)):
    plt.subplot(2,2,x+1)

    data[x] = data[x].sort_values(by='length')

    plot1 = data[x][(data[x]['lambda'] == 0.5) & (data[x]['length'] != 0) ]
    plot2 = data[x][(data[x]['lambda'] == 0.9) & (data[x]['length'] != 0) ]
    plot3 = data[x][(data[x]['lambda'] == 0.95) & (data[x]['length'] != 0)]
    plot4 = data[x][(data[x]['lambda'] == 0.99) & (data[x]['length'] != 0)]

    plt.plot(plot1['length'], plot1['perc'],"-b",linestyle="dashed",  label="lambda: 0.5")
    plt.plot(plot2['length'], plot2['perc'],"-",linestyle="dashed",  label = "lambda: 0.9")
    plt.plot(plot3['length'], plot3['perc'],"-g",linestyle="dashed",  label = "lambda: 0.95")
    plt.plot(plot4['length'], plot4['perc'],"-r",linestyle="dashed",  label = "lambda: 0.99")
    plt.legend(loc = "upper right")

    plt.xlim(1,20)

plt.show()


