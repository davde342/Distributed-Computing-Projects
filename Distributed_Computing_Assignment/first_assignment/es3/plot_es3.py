import matplotlib.pyplot as plt 
import pandas as pd
import argparse
import csv 

data = []
name_file_d = [1, 2, 5, 10]
name_file_l = [0.5, 0.99]
num_el = 0

for x in range(len(name_file_d)):
    for y in range(len(name_file_l)):
        print("take data from file: csv3/result_" + str(name_file_d[x]) + "_" + str(name_file_l[y])+".csv")
        data.append(pd.read_csv("csv3/result_"+ str(name_file_d[x]) + "_" +str(name_file_l[y])+".csv"))
        num_el+=1

num_el = 0
plot_pos = 0
print(data)
for x in range(len(name_file_d)):
    for y in range(len(name_file_l)):
        plot_pos += 1
        plt.subplot(4, 2, (plot_pos))
        
        data[num_el] = data[num_el].sort_values(by='length')
            
        plot2 = data[num_el][(data[num_el]['shape'] == 0.5) & (data[num_el]['length'] != 0) ]
        plot4 = data[num_el][(data[num_el]['shape'] == 1.0) & (data[num_el]['length'] != 0)]
        plot6 = data[num_el][(data[num_el]['shape'] == 1.5) & (data[num_el]['length'] != 0)]


        plt.plot(plot2['length'], plot2['perc'],"-y",linestyle="dashed",  label =  "shape: 0.5")
        plt.plot(plot4['length'], plot4['perc'],"-r",linestyle="dashed",  label = "shape: 1.0")
        plt.plot(plot6['length'], plot6['perc'],"-p",linestyle="dashed",  label = "shape: 1.5")
        plt.xlabel("") 
        plt.ylabel("")
        num_el += 1
        plt.legend(loc = "upper right")
        plt.xlim(1,30)

plt.show()




