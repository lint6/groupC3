#This file will check if there is any redundancy in the data (two data sets exactly the same)
import data_importer
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os

def fun_CheckBigArrays(DataArray, DataArray2):
    if np.array_equal(DataArray, DataArray2, equal_nan=False) == True:
        response = 1
    else:
        response = 0
    return response

def fun_DataRedundancyCheck(i, j):
    running = True
    while running:
        sames = []
        index_num = i
        DataArray = data_importer.fun_GetDataRaw(index_num)

        index_num2 = j
        DataArray2 = data_importer.fun_GetDataRaw(index_num2)

        BigCheck = fun_CheckBigArrays(DataArray, DataArray2)

        if BigCheck == 1:
            if i != j:
                sames.append((i, j))
        return sames

def fun_FullBigArrayCheck(i=3 , j=3):
    sameArrays = []
    running = True
    while running:
        sametuple = fun_DataRedundancyCheck(i, j)
        if len(sametuple) > 0:
            sameArrays.append(sametuple)
        j = j + 1
        if j > 25:
            i = i + 1
            j = i
            if i > 25:
                running = False
    return sameArrays

TOTAL_ARRAY_CHECK = fun_FullBigArrayCheck()
print (TOTAL_ARRAY_CHECK)

#def fun_CheckWithinArrays(i = 0, j = 0):
