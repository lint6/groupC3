#This file will extract the code from the MAT files and put in python. It also has functions to fully format the code.

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os
import math

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


def fun_GetDataRaw(index_num, index):
    # index = fun_Index_Gen("Data files")
    mat = sio.loadmat(f'Data files/{index[index_num]}')
    data_raw = mat.pop('motiondata')
    data_trans = np.transpose(data_raw)
    return data_trans

def fun_data_format(data_trans):
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

def fun_FillInFinalProd(FinalProd, TimesToZero, n):
    m = 0
    running = True
    while running:
        point = int(TimesToZero[m])
        FinalProd[n][point] = int(0)
        m = m + 1
        if m >= len(TimesToZero):
            running = False
    return FinalProd

def fun_BuildFinalProd(Time):
    finalbuild1 = np.ones((6, len(Time)))
    FinalProd = np.vstack((Time, finalbuild1))
    PerRemoved = np.zeros((1,6))
    return FinalProd, PerRemoved

def fun_MakeLinRegression(TimeData, DataYouWantToTest, DegreeOfPoly):
    ones = np.ones(len(TimeData))
    A_T = ones
    for i in range(DegreeOfPoly):
        A_T =np.vstack((A_T, TimeData**(i+1)))
    A = np.transpose(A_T)
    b_line_T = DataYouWantToTest
    b_line = np.transpose(b_line_T)
    ATA = np.dot(A_T,A)
    ATb_line = np.dot(A_T, b_line)

    solution = np.linalg.solve(ATA, ATb_line)
    y = 0
    for j in range(DegreeOfPoly+1):
        y = y + (solution[j] * TimeData**j)

    return y

def fun_PlottingTheLines(SplitTimeArray, SplitValueArray, k, DegreeOfPoly):
    store = []
    ThreshStore = []
    running = True
    while running:
        Line = fun_MakeLinRegression(SplitTimeArray[k], SplitValueArray[k], DegreeOfPoly)
        ##########################     Thresh    ###################################
        ArrayLine = np.array(Line)
        DiffArray = np.sort(abs(SplitValueArray[k] - ArrayLine))
        UQ = DiffArray[round(len(DiffArray)*0.75)]
        LQ = DiffArray[round(len(DiffArray)*0.25)]
        IQR = UQ-LQ
        # print(UQ, IQR)
        Thresh = UQ + 1.5*(IQR)
        ThreshStore.append(Thresh)
        #plt.plot(SplitTimeArray[k], Line, 'r', linewidth = 5)
        store.append(list(Line))
        k = k + 1
        if k == len(SplitTimeArray):
            running = False
    AvThresh = sum(ThreshStore)/len(ThreshStore)

    # np.savetxt('filePLR.txt', np.array(Store2))
    return store, AvThresh

def fun_NoPlottingTheLines(SplitTimeArray, SplitValueArray, k, DegreeOfPoly):
    store = []
    running = True
    while running:
        Line = fun_MakeLinRegression(SplitTimeArray[k], SplitValueArray[k], DegreeOfPoly)
        plt.plot(SplitTimeArray[k], Line, 'r', linewidth = 3)
        store.append(Line)
        k = k + 1
        if k == len(SplitTimeArray):
            running = False
    return store

def fun_OutlierDetermination(SplitTimeArray, SplitValueArray, StoredLines, Threshold):
    j = 0
    COUNTER = 0
    RemovedValsLines = []
    RemovedValsTimes = []
    Cutoff = Threshold
    running = True
    while running:
        DataPoints = SplitValueArray[j].copy()

        RegressorLine = StoredLines[j].copy()

        TimePoints = SplitTimeArray [j].copy()
        k = 0
        running1 = True
        while running1:
            Diff = DataPoints[k]-RegressorLine[k]
            Diff = abs(Diff)
            if Diff >= Cutoff:
                DataPoints[k] = None
                TimePoints[k] = None
                COUNTER += 1
            k = k + 1
            if k == len(SplitValueArray[j]):
                running1 = False
        RemovedValsLines.append(DataPoints)
        RemovedValsTimes.append(TimePoints)
        j = j + 1
        if j == len(SplitValueArray):
            running = False
    return RemovedValsTimes , RemovedValsLines, COUNTER




#Plotting Data
#give in the two things you want to plot
def fun_LinearRegressionAlgorithm(ArraySplitT, ArraySplitV, k, Thresh, NumberOfSplits, variable1, variable2, DegreeOfPoly):
    StoredLines, AvThresh = fun_PlottingTheLines(ArraySplitT, ArraySplitV, k, DegreeOfPoly)
    RemovedValsTimes, RemovedValsLines, COUNTER = fun_OutlierDetermination(ArraySplitT, ArraySplitV, StoredLines, AvThresh)


    AllRemovedValsTimes = []
    AllRemovedValsLines = []
    for i in range(NumberOfSplits):
        AllRemovedValsTimes = AllRemovedValsTimes + list(RemovedValsTimes[i])
        AllRemovedValsLines = AllRemovedValsLines + list(RemovedValsLines[i])
    AllRemovedValsLines = [i for i in AllRemovedValsLines if np.isnan(i) == False]
    AllRemovedValsTimes = [i for i in AllRemovedValsTimes if np.isnan(i) == False]
    TimesToZero = np.array(AllRemovedValsTimes)/0.04
    plt.plot(AllRemovedValsTimes, AllRemovedValsLines, color = 'orange')
    plt.xlabel('Time [s]')
    plt.ylabel('Pitch [deg]')
    plt.show()
    return COUNTER, TimesToZero

def fun_NoPlotLinearRegressionAlgorithm(ArraySplitT, ArraySplitV, k, Thresh, NumberOfSplits, variable1, variable2, DegreeOfPoly):
    StoredLines, AvThresh = fun_PlottingTheLines(ArraySplitT, ArraySplitV, k, DegreeOfPoly)
    RemovedValsTimes, RemovedValsLines, COUNTER = fun_OutlierDetermination(ArraySplitT, ArraySplitV, StoredLines, AvThresh)


    AllRemovedValsTimes = []
    AllRemovedValsLines = []
    for i in range(NumberOfSplits):
        AllRemovedValsTimes = AllRemovedValsTimes + list(RemovedValsTimes[i])
        AllRemovedValsLines = AllRemovedValsLines + list(RemovedValsLines[i])
    AllRemovedValsLines = [i for i in AllRemovedValsLines if np.isnan(i) == False]
    AllRemovedValsTimes = [i for i in AllRemovedValsTimes if np.isnan(i) == False]
    TimesToZero = np.array(AllRemovedValsTimes) / 0.04

    #plt.plot(AllRemovedValsTimes, AllRemovedValsLines, color = 'orange')
    #plt.show()
    return COUNTER, TimesToZero

def fun_FindThresh(variable2):
    Abso = variable2
    Sorted = np.sort(Abso)
    Limit = math.ceil(0.9*len(Sorted))
    Sort = Sorted[0:Limit]
    Uplim = Sort[-1]
    LowLim = Sort[0]
    Thresh = (Uplim-LowLim)/3
    return Thresh

def fun_SplittingArrays(NumberOfSplits, variable1, variable2):
    ArraySplitT = np.array_split(variable1, NumberOfSplits)
    ArraySplitV = np.array_split(variable2, NumberOfSplits)
    return ArraySplitT, ArraySplitV
