from csv import reader
import re
import matplotlib.pyplot as plt
from collections import deque
import os
import pandas as pd

# master_df = pd.DataFrame()
btp_dir = "combine"
lh_dir = "combinelh"
# for file in os.listdir(btp_dir):
#     if file.endswith('.csv'):
#         master_df = master_df.append(pd.read_csv(btp_dir + "/" + file))

# master_df.to_csv("BTP.csv", index = False)

# master_df = pd.DataFrame()
# for file in os.listdir(lh_dir):
#     master_df = master_df.append(pd.read_csv(lh_dir + "/" + file, error_bad_lines=False))

# master_df.to_csv("LH.csv", index = False)

fout=open("BTP.csv","a")
# first file:
for file in os.listdir(btp_dir):
    f = open(btp_dir + "/" + file, "r")
    for line in f:
         fout.write(line)
    f.close() # not really needed
fout.close()

fout=open("LH.csv","a")
# first file:
for file in os.listdir(lh_dir):
    f = open(lh_dir + "/" + file, "r")
    for line in f:
        if line:
         fout.write(line)
    f.close() # not really needed
fout.close()

#open file in read mode
with open('BTP.csv', 'r') as btp_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(btp_obj)
    btp_data = list(csv_reader)

with open('LH.csv', 'r') as lh_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(lh_obj)
    lh_data = sorted(list(csv_reader))
    lh_data = [l for l in lh_data if  l]

# #match first letter of the log message to character C if it is a match get the order id.
marker = "was sent"
x = []
y = []
z = []
look_back = deque()
# print(lh_data[0])

cutoff = 0
for i in range(len(btp_data)):
    if len(btp_data[i][0]) > 12 and btp_data[i][0][:12] < lh_data[0][0][:12]:
        continue
    cutoff = i
    break

btp_data = btp_data[cutoff:]

for i in range(len(btp_data)):
    if len(btp_data[i][0]) > 14 and (btp_data[i][0][14] == "C" or marker in btp_data[i][0]):
        if btp_data[i][0][14] == "C":
            order_id = btp_data[i][0].split()[-1]   #split the string on white space into a list and get the last string which is the order id
            order_id_bitbay = "Canceling order:  " + order_id
            order_id_bitso = "Canceling order " + order_id
        else:
            order_id_bitbay = re.search(r'\((.*?)\)', btp_data[i][0]).group(1)
            order_id_bitso = "place holder 11111"
        
        sentTime = int(float(btp_data[i][0][3:5] + btp_data[i][0][6:12]) * 1000)  #calculate the miliseconds into integers

        if not list(look_back):
            look_back.append(sentTime)
        else:
            for time in list(look_back):
                if sentTime - time <= 1000:
                    break
                else:
                    look_back.popleft()
            look_back.append(sentTime)

        for k in lh_data[i:]:   #starting at the ith index of LH data because LH data has to be equal to or after BTP data
            if k and order_id_bitbay in k[0] or k and order_id_bitso in k[0]:
                recieved_time = int(float(k[0][3:5] + k[0][6:12]) * 1000)   #calculate the miliseconds into integers
                latency = recieved_time - sentTime
                # print(sentTime)
                # print(recieved_time)
                print(btp_data[i][0][:20], end=" : latency ")
                print(latency, end =" : # of reqs ")
                print(len(look_back)-1)

                x.append((k[0][:12]))
                y.append(latency)
                z.append(len(look_back)-1)
                break
        
fig, ax1 = plt.subplots()
plt.ylim(-25,1000)

ax2 = ax1.twinx()
ax1.scatter(x, y,
          marker='o', color='blue', s=2)

ax2.plot(x, z, 'g-', linewidth=.2)

ax1.set_xlabel('X data')
ax1.set_ylabel('Y data', color='g')
ax2.set_ylabel('z data', color='b')

plt.show()    

file = "BTP.csv"
file2 = "LH.csv"
if(os.path.exists(file) and os.path.exists(file2)):
    os.remove(file)
    os.remove(file2)

#         # print(sentTime)
#         if not list(look_back):
#             look_back.append(sentTime)
#         else:
#             for time in list(look_back):
#                 if sentTime - time <= 1000:
#                     break
#                 else:
#                     look_back.popleft()
#             look_back.append(sentTime)

#         for k in lh_data[i:]:   #starting at the ith index of LH data because LH data has to be equal to or after BTP data
#             if order_id in k[0]:
#                 recieved_time = int(float(k[0][3:5] + k[0][6:12]) * 1000)   #calculate the miliseconds into integers
#                 latency = recieved_time - sentTime
#                 print(btp_data[i][0][:20], end=" : ")
#                 print(latency, end =" : # of reqs ")
#                 print(len(look_back))

#                 x.append((k[0][:12]))
#                 y.append(latency)
#                 break

#         elif marker in btp_data[i][0]:
#             # print(btp_data[j])
#             sent_id = re.search(r'\((.*?)\)', btp_data[i][0]).group(1)
#             # print(sent_id)
#             sent_time = int(float(btp_data[i][0][3:5] + btp_data[i][0][6:12]) * 1000)

#             for l in lh_data[i:]:
#                 if sent_id in l[0]:
#                     recieved_time = int(float(l[0][3:5] + l[0][6:12]) * 1000)
#                     latency = recieved_time - sentTime
#                     print(btp_data[i][0][:20], end=" : ")
#                     print(latency, end =" : # of reqs ")
#                     print(float(l[0][6:12]) - sent_time)
#                     x.append((l[0][:12]))
#                     y.append(int((float(l[0][6:12]) - sent_time) * 1000))
#                     break           






# plt.scatter(x, y,
#          marker='o', color='blue', s=5)
  
# plt.ylim(50,1000)
  
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
  
# # giving a title to my graph
# plt.title('Some cool customizations!')
  
# # function to show the plot
# plt.show()