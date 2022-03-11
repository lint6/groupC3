#This file will check whether all the data points are to the same significant digits.

import data_importer
import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import os

index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?'))

mat = sio.loadmat(f'Data files/{index[index_num]}')

#Class defining
FormattedData = data_importer.fun_data_format(mat)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])

print (data.Time)










