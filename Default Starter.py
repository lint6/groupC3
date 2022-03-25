import data_importer
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os

index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?'))
DataArray = data_importer.fun_GetDataRaw(index_num)




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

FormattedData = data_importer.fun_data_format(DataArray)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])

#Plotting Data
#give in the two things you want to plot
variable1 = data.Time
variable2 = data.Y_raw

plt.scatter(variable1, variable2, s=1)
plt.show()
