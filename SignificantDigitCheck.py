#This file will check whether all the data points are to the same significant digits.

import data_importer
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os

index = data_importer.fun_Index_Gen("Data files")
#index_num = int(input('Which file number would you like?'))
index_num = 3
mat = sio.loadmat(f'Data files/{index[index_num]}')

#Class defining
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

FormattedData = data_importer.fun_data_format(mat)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])

#print(data.Time)


def fun_SigFigCheck(data):
    i = 1
    j = 2
    WeirdVals = np.array([])
    Reference = len(str(FormattedData[j][1]))
    print(f"Reference {Reference}")
    running = True
    while running:
        check = data.X_raw[i]
        SigFigs = len(str(check))-1
        print (check)
        print (SigFigs)
        print ('')
        if SigFigs != Reference:
            WeirdVals = np.append(WeirdVals, check)
        if i >= len(FormattedData[j])-1:
            running = False
        else:
            i = i + 1
    return WeirdVals

test = fun_SigFigCheck(data)
print(test)

#Plotting Data
#give in the two things you want to plot
variable1 = data.Time
variable2 = data.Pitch_raw

plt.plot(variable1, variable2)
plt.show()








