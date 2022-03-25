import data_importer
import numpy as np
import matplotlib.pyplot as plt
import Least_Square_Regression
import random
import math

index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?\n'))
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

#Least Square Regression Step
#Defining the variables and arrays
NumberOfSplits = 5
variable1 = data.Time #Should always be time
variable2 = data.X_raw
plt.plot(variable1, variable2, color = 'b') #Blue Line
#Lines = np.empty((1,NumberOfSplits))
ArraySplitT = np.array_split(variable1, NumberOfSplits)
ArraySplitV = np.array_split(variable2, NumberOfSplits)
k = 0
Thresh = 0.003



Least_Square_Regression.fun_RemovedValsLinesAndProcessingForPlotting(ArraySplitT, ArraySplitV, k, Thresh, NumberOfSplits, variable1, variable2)


