import data_importer
import numpy as np
import scipy.io as sio

def data_accuracy_checker(array_in):
    array_in = np.delete(array_in, [0,], 0)
    print(type(array_in[0][0]))
    print(array_in)



index = data_importer.fun_Index_Gen("Data files")
#index_num = int(input('Which file number would you like?'))
for i in range(26):
    print(f'\nData file {i}')
    index_num = i
    array = sio.loadmat(f'Data files/{index[index_num]}')
    array = data_importer.fun_data_format(array)
    data_accuracy_checker(array)
