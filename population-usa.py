import matplotlib.pyplot as plt
import csv
import matplotlib.patches as mpatches

with open("free-zipcode-database-Primary.csv", 'r') as f: ## the reader we usually use wasn't working correctly so I found this online
    reader = csv.reader(f)
    zip_code_data = list(reader)

zip_code_data = sorted(zip_code_data, key=lambda x: x[0])

long_data = []
lat_data = []
zips = []
size_list = []
zip_code_data.remove(zip_code_data[0])

for i in range(len(zip_code_data)):
    if zip_code_data[i][3] != "AK" and zip_code_data[i][3] != "HI":
        try:
            if float(zip_code_data[i][6]) < -50 and float(zip_code_data[i][6]) > -140 and float(zip_code_data[i][5]) > 20:
                long_data.append(float(zip_code_data[i][6]))
                lat_data.append(float(zip_code_data[i][5]))
                zips.append(zip_code_data[i][0])
        except:
            print("Failure")
        #try:
         #   size_list.append(float(zip_code_data[i][10]))
        #except:
         #   size_list.append(0)

#for k in range(len(size_list)):
 #   size_list[k] = size_list[k] / 100


#plt.figure(1, figsize=[4.3*2, 6.6], tight_layout=True)
plt.figure(figsize=[10, 6.5], tight_layout=True)

plt.scatter(long_data, lat_data, s=1, alpha=0.3)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Zipcodes Scaled by Population")

plt.show()