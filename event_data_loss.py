import data_importer
import numpy as np
import scipy.io as sio

index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?'))

#Extracting Data from Matlab
mat = sio.loadmat(f'Data files/{index[index_num]}')

array = data_importer.fun_data_format(mat)
print(array)
