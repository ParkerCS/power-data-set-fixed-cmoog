import matplotlib.pyplot as plt
import csv
import matplotlib.patches as mpatches
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

def plot_legend():
    top_25 = mpatches.Patch(label="Top 25th percentile", color="red")
    fifty_to_seventy_five = mpatches.Patch(label="50th to 75th percentile", color="yellow")
    twenty_five_to_fifty = mpatches.Patch(label="25th to 50th percentile", color="orange")
    bottom_twenty_five = mpatches.Patch(label="Bottom 25th percentile", color="green")
    plt.legend(handles=[top_25, fifty_to_seventy_five, twenty_five_to_fifty, bottom_twenty_five])

with open("free-zipcode-database-Primary.csv", 'r') as f: ## the reader we usually use wasn't working correctly so I found this online
    reader = csv.reader(f)
    zip_code_data = list(reader)
with open("power_data.csv", 'r') as f: ## the reader we usually use wasn't working correctly so I found this online
    reader = csv.reader(f)
    your_list = list(reader)
power_data = your_list

bund_res = []  ## Here this is going to hold the entire list of data for IL bundles
for i in range(len(power_data)):
    if power_data[i][4] == "Bundled":
        bund_res.append(power_data[i])

zip_code_data = sorted(zip_code_data, key=lambda x: x[0])

long_data = []
lat_data = []
zips = []
size_list = []
res_rate = []
color_list = []
zip_code_data.remove(zip_code_data[0])
bund_res = sorted(bund_res, key=lambda x: x[8])

for i in range(len(zip_code_data)):
    if zip_code_data[i][3] != "AK" and zip_code_data[i][3] != "HI":
        try:
            if float(zip_code_data[i][6]) < -50 and float(zip_code_data[i][6]) > -140 and float(zip_code_data[i][5]) > 20:
                long_data.append(float(zip_code_data[i][6]))
                lat_data.append(float(zip_code_data[i][5]))
                zips.append(zip_code_data[i][0])
                res_rate.append(bund_res[binary_search(zip_code_data[i][0], bund_res)][8])

        except:
            print("Failure")

for j in range(len(res_rate)):
    if j / len(res_rate) > .75:
        color_list.append("red")
    elif j / len(res_rate) > .5:
        color_list.append("#eded1c")
    elif j / len(res_rate) > .25:
        color_list.append("orange")
    else:
        color_list.append("green")

plt.figure(figsize=[10, 6.5], tight_layout=True)

plt.scatter(long_data, lat_data, s=1, color=color_list)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Residential Electricity Rates by Zipcode")
plot_legend()
plt.show()