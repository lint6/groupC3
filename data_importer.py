#This file will extract the code from the MAT files and put in python. It also has functions to fully format the code.

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os

"""contain function for importing data"""
#Functions
def fun_Index_Gen(foldername):
    presetlist = os.listdir(foldername)
    n = 0
    file_index = []
    print (f'Total file found: {len(presetlist)}')
    for i in presetlist:
        print(f'{n} -- {i}')
        file_index.append(i)
        n += 1
    print (f'Index Finished')
    return file_index

index = fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?'))

#Extracting Data from Matlab
mat = sio.loadmat(f'Data files/{index[index_num]}')

def fun_data_format(mat):
    data_raw = mat.pop('motiondata')
    data_trans = np.transpose(data_raw)
    #Scaling the values
    #Time column
    data_trans[0] = data_trans[0] - data_trans[0][0]
    data_trans[0] = data_trans[0] / 10000


    #Roll raw #Pitch_raw and Yaw Raw
    running = True
    k = 3
    while running:
        data_trans[k] = (data_trans[k]*180)/16383
        if k == 5:
            running = False
        k = k + 1

    #X_raw, Y_raw and Z_raw
    running = True
    k = 6
    while running:
        data_trans[k] = (data_trans[k]*180)/16383
        if k == 8:
            running = False
        k = k + 1
    return data_trans

#Class setup
class Data:
    def __init__(self, Time, xdotdot, FrameSignature, Roll_raw, Pitch_raw, Yaw_raw, X_raw, Y_raw, Z_raw):
        self.Time = Time
        self.xdotdot = xdotdot
        self.FrameSignature = FrameSignature
        self.Roll_raw = Roll_raw
        self.Pitch_raw = Pitch_raw
        self.Yaw_raw = Yaw_raw
        self.X_raw = X_raw
        self.Y_raw = Y_raw
        self.Z_raw = Z_raw

#Defining Class
FormattedData = fun_data_format(mat)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])


#Plotting Data
#give in the two things you want to plot
variable1 = data.Time
variable2 = data.Pitch_raw

plt.plot(variable1, variable2)
plt.show()
