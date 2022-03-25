import data_importer
import numpy as np
import matplotlib.pyplot as plt



# index = data_importer.fun_Index_Gen("Data files")
# index_num = int(input('Which file number would you like?'))
# DataArray = data_importer.fun_GetDataRaw(index_num)
#
# class Data:
#     def __init__(self, Time, xdotdot, FrameSignature, Roll_raw, Pitch_raw, Yaw_raw, X_raw, Y_raw, Z_raw):
#         self.Time = Time
#         self.xdotdot = xdotdot
#         self.FrameSignature = FrameSignature
#         self.Roll_raw = Roll_raw
#         self.Pitch_raw = Pitch_raw
#         self.Yaw_raw = Yaw_raw
#         self.X_raw = X_raw
#         self.Y_raw = Y_raw
#         self.Z_raw = Z_raw

# FormattedData = data_importer.fun_data_format(DataArray)
# data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])


#LSR
#Defining the variables and arrays
# NumberOfSplits = 20
# variable1 = data.Time #Should always be time
# variable2 = data.Y_raw
# plt.plot(variable1, variable2) #Blue Line
# #Lines = np.empty((1,NumberOfSplits))
# ArraySplitT = np.array_split(variable1, NumberOfSplits)
# ArraySplitV = np.array_split(variable2, NumberOfSplits)
# k = 0
# Thresh = 5

def fun_MakeLinRegression(TimeData, DataYouWantToTest):
    ones = np.ones(len(TimeData))
    A_T =np.vstack((ones, TimeData, (TimeData)**2, (TimeData**3), TimeData**4))
    A = np.transpose(A_T)
    b_line_T = DataYouWantToTest
    b_line = np.transpose(b_line_T)
    ATA = np.dot(A_T,A)
    ATb_line = np.dot(A_T, b_line)

    solution = np.linalg.solve(ATA, ATb_line)
    y = solution[0] + solution[1]*TimeData+ solution[2]*(TimeData)**2 + solution[3]*(TimeData)**3 + solution[4]*(TimeData)**4
    return y

def fun_PlottingTheLines(SplitTimeArray, SplitValueArray, k):
    store = []
    running = True
    while running:
        Line = fun_MakeLinRegression(SplitTimeArray[k], SplitValueArray[k])
        plt.plot(SplitTimeArray[k], Line, 'r')
        store.append(Line)
        k = k + 1
        if k == len(SplitTimeArray):
            running = False
    return store

def fun_OutlierDetermination(SplitTimeArray, SplitValueArray, StoredLines, Threshold):
    j = 0
    RemovedValsLines = []
    RemovedValsTimes = []
    Cutoff = Threshold
    running = True
    while running:
        DataPoints = SplitValueArray[j]

        RegressorLine = StoredLines[j]

        TimePoints = SplitTimeArray [j]
        k = 0
        running1 = True
        while running1:
            Diff = DataPoints[k]-RegressorLine[k]
            Diff = abs(Diff)
            if Diff >= Cutoff:
                DataPoints[k] = None
                TimePoints[k] = None
            k = k + 1
            if k == len(SplitValueArray[j]):
                running1 = False
        RemovedValsLines.append(DataPoints)
        RemovedValsTimes.append(TimePoints)
        j = j + 1
        if j == len(SplitValueArray):
            running = False
    return RemovedValsTimes , RemovedValsLines




#Plotting Data
#give in the two things you want to plot
def fun_RemovedValsLinesAndProcessingForPlotting(ArraySplitT, ArraySplitV, k, Thresh, NumberOfSplits, variable1, variable2):
    StoredLines = fun_PlottingTheLines(ArraySplitT, ArraySplitV, k)
    RemovedValsTimes, RemovedValsLines = fun_OutlierDetermination(ArraySplitT, ArraySplitV, StoredLines, Thresh)


    AllRemovedValsTimes = []
    AllRemovedValsLines = []
    for i in range(NumberOfSplits):
        AllRemovedValsTimes = AllRemovedValsTimes + list(RemovedValsTimes[i])
        AllRemovedValsLines = AllRemovedValsLines + list(RemovedValsLines[i])
    AllRemovedValsLines = [i for i in AllRemovedValsLines if np.isnan(i) == False]
    AllRemovedValsTimes = [i for i in AllRemovedValsTimes if np.isnan(i) == False]

    # m = 0
    # running = True
    # while running:
    #     plt.plot(RemovedValsTimes[m], RemovedValsLines[m], color = 'g')
    #     m = m + 1
    #     if m == len(RemovedValsTimes):
    #         running = False

    plt.plot(AllRemovedValsTimes, AllRemovedValsLines, color = 'orange')
    #plt.plot(variable1, variable2, color = 'g')
    plt.show()


#Getting values and cleaning data
# StoredLines = Least_Square_Regression.fun_PlottingTheLines(ArraySplitT, ArraySplitV, k, ArraySplitT)
# RemovedValsTimes, RemovedValsLines = Least_Square_Regression.fun_OutlierDetermination(ArraySplitT, ArraySplitV, StoredLines, Thresh)
#
# AllRemovedValsTimes = []
# AllRemovedValsLines = []
# for i in range(NumberOfSplits):
#     AllRemovedValsTimes = AllRemovedValsTimes + list(RemovedValsTimes[i])
#     AllRemovedValsLines = AllRemovedValsLines + list(RemovedValsLines[i])
# AllRemovedValsLines = [i for i in AllRemovedValsLines if np.isnan(i) == False]
# AllRemovedValsTimes = [i for i in AllRemovedValsTimes if np.isnan(i) == False]
#
# plt.plot(AllRemovedValsTimes, AllRemovedValsLines, color = 'orange')
# plt.show()
