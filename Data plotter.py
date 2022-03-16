#This file imports the data out of the MAT files and then formats it.

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os

"""
contain function for importing data
"""

# Functions
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
mat_sim = sio.loadmat(f'Data files/{index[index_num]}')


def fun_DataFormat(mat_sim):
    data_raw = mat_sim.pop('motiondata')
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
        data_trans[k] = (data_trans[k]*0.5)/16383
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
FormattedData = fun_DataFormat(mat_sim)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])


#Plotting Data
#defining variables
time = data.Time
roll = data.Roll_raw
pitch = data.Pitch_raw
yaw = data.Yaw_raw
x_coor = data.X_raw
y_coor = data.Y_raw
z_coor = data.Z_raw

#subplot creation
figure, axis = plt.subplots(2, 1)

# scatter plots for angles
axis[0].scatter(time, roll, s=0.2, label='roll')
axis[0].scatter(time, pitch, s=0.2, label='pitch')
axis[0].scatter(time, yaw, s=0.2, label='yaw')
axis[0].set_title("Angles")
axis[0].legend()

# scatter plots for coordinates
axis[1].scatter(time, x_coor, s=0.2, label='x')
axis[1].scatter(time, y_coor, s=0.2, label='y')
axis[1].scatter(time, z_coor, s=0.2, label='z')
axis[1].set_title("Coordinates")
axis[1].legend()

plt.show()
