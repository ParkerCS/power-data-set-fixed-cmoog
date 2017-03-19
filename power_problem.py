'''
Use the power_data.csv file AND the zipcode database
to answer the questions below.  Make sure all answers
are printed in a readable format. (i.e. "The city with the highest electricity cost in Illinois is XXXXX."

The power_data dataset, compiled by NREL using data from ABB,
the Velocity Suite and the U.S. Energy Information
Administration dataset 861, provides average residential,
commercial and industrial electricity rates by zip code for
both investor owned utilities (IOU) and non-investor owned
utilities. Note: the file includes average rates for each
utility, but not the detailed rate structure data found in the
OpenEI U.S. Utility Rate Database.

This is a big dataset.
Below are some questions that you likely would not be able
to answer without some help from a programming language.
It's good geeky fun.  Enjoy

FOR ALL THE RATES, ONLY USE THE BUNDLED VALUES (NOT DELIVERY).  This rate includes transmission fees and grid fees that are part of the true rate.
'''

#1  What is the average residential rate for YOUR zipcode? You will need to read the power_data into your program to answer this.  (7pts)

import matplotlib.pyplot as plt
import csv
import statistics

def selection_sort(list):
    for pos in range(len(list)):
        min_pos = pos
        for sort_pos in range(min_pos, len(list)):
            if list[sort_pos][0] < list[min_pos][0]:
                min_pos = sort_pos
        temp = list[pos]
        list[pos] = list[min_pos]
        list[min_pos] = temp
    return list

def binary_search(input_key, list):
    key = input_key.upper()
    lower_bound = 0
    upper_bound = len(list) - 1
    found = False
    # loop until we find item or the bounds meet
    while lower_bound <= upper_bound and not found:
        # find the middle
        middle_position = (lower_bound + upper_bound) // 2
        # figure out if we need to move up or down
        if list[middle_position][0] < key:
            lower_bound = middle_position + 1
        elif list[middle_position][0] > key:
            upper_bound = middle_position - 1
        else:
            found = True
    return middle_position

with open("power_data.csv", 'r') as f: ## the reader we usually use wasn't working correctly so I found this online
    reader = csv.reader(f)
    your_list = list(reader)
power_data = your_list


headers = power_data[0]
power_data.remove(power_data[0])
'''
power_data = sorted(power_data, key=lambda x: x[4])  # found this online
index = len(power_data)-1
while power_data[index][4] != "Bundled":
    power_data.remove(power_data[index])
    index -= 1
'''
power_data = sorted(power_data, key=lambda x: x[0])
print("The average residential rate for electricity in 60614 is", power_data[binary_search("60614", power_data)][8], "dollars per kWh.")

#2 What is the MEDIAN rate for all BUNDLED RESIDENTIAL rates in Illinois? Use the data you extracted to check all "IL" zipcodes to answer this. (10pts)
il_bund_res = []
for i in range(len(power_data)):
    if power_data[i][3] == "IL" and power_data[i][4] == "Bundled":
        il_bund_res.append(power_data[i][8])

print("The median rate for bundled residents in IL is", statistics.median(il_bund_res))
'''
##remove all delivery lines (only keeps bundled)
for item in power_data:
    if item[4] == "Delivery":
        power_data.remove(item)
'''

#3 What city in Illinois has the lowest residential rate?  Which has the highest?  You will need to go through the database and compare each value for this one. Then you will need to reference the zipcode dataset to get the city.  (15pts)
il_bund_res = []
for i in range(len(power_data)):
    if power_data[i][3] == "IL" and power_data[i][4] == "Bundled":
        il_bund_res.append(power_data[i])

il_bund_res = sorted(il_bund_res, key=lambda x: x[8])
print("LOOK AT THIS IT SHOULD BE:", il_bund_res[0][8])
lowest_rate_zip = il_bund_res[0][0]
highest_rate_zip = il_bund_res[len(il_bund_res)-1][0]

with open("free-zipcode-database-Primary.csv", 'r') as f: ## the reader we usually use wasn't working correctly so I found this online
    reader = csv.reader(f)
    zip_code_data = list(reader)

zip_code_data = sorted(zip_code_data, key=lambda x: x[0])

print("The city with the lowest residential rate in IL is", zip_code_data[binary_search(lowest_rate_zip, zip_code_data)][2])
print("The city with the highest residential rate in IL is", zip_code_data[binary_search(highest_rate_zip, zip_code_data)][2])


#FOR #4  CHOOSE ONE OF THE FOLLOWING TWO PROBLEMS. The first one is easier than the second.
#4  (Easier) USING ONLY THE ZIP CODE DATA... Make a scatterplot of all the zip codes in Illinois according to their Lat/Long.  Make the marker size vary depending on the population contained in that zip code.  Add an alpha value to the marker so that you can see overlapping markers.

#4 (Harder) USING BOTH THE ZIP CODE DATA AND THE POWER DATA... Make a scatterplot of all zip codes in Illinois according to their Lat/Long.  Make the marker red for the top 25% in residential power rate.  Make the marker yellow for the middle 25 to 50 percentile. Make the marker green if customers pay a rate in the bottom 50% of residential power cost.  This one is very challenging.  You are using data from two different datasets and merging them into one.  There are many ways to solve. (20pts)
def percentiles(list):
    selection_sort(list)
    print(list)

long_data = []
lat_data = []
zips = []
color_list = []
size = []
il_bund_res = sorted(il_bund_res, key=lambda x: x[8])
res_rate = []
for i in range(len(zip_code_data)):
    if zip_code_data[i][3] == "IL":
        long_data.append(zip_code_data[i][6])
        lat_data.append(zip_code_data[i][5])
        zips.append((zip_code_data[i][0]))
        res_rate.append(il_bund_res[binary_search(zip_code_data[i][0], il_bund_res)][8])

for j in range(len(res_rate)):
    if j / len(res_rate) > .75:
        color_list.append("red")
    elif j / len(res_rate) > .5:
        color_list.append("yellow")
    else:
        color_list.append("green")

print(res_rate)
print(selection_sort(res_rate))
#for k in range(len(res_rate)):

plt.figure(figsize=[4.7,6.5], tight_layout=True)
my_plot = plt.scatter(long_data,lat_data, color=color_list)


plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Illinois Zip Codes - Scaled by Residential Electricity Rate")

#plt.ylim([float(min(lat))- 5, float(max(long_data)) + 5])

plt.show()
