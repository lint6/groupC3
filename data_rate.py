import data_importer
import numpy as np
import scipy.io as sio

def data_rate_checker(array_in):
    time_array = array_in[0]
    time_array_2 = np.pad(time_array, (1,0))
    time_array = np.pad(time_array, (0,1))
    time_diff = np.delete(time_array - time_array_2, [0, -1] , 0)
    delta = np.bincount(time_diff.astype("int64")).argmax()
    error_array = np.nonzero(time_diff == delta)
    if error_array[0].size > 0:
        print('Data rate error found, location printed:')
        print(error_array)
    else:
        print('No data rate error found')



index = data_importer.fun_Index_Gen("Data files")
#index_num = int(input('Which file number would you like?'))
for i in range(26):
    print(f'\nData file{i}')
    index_num = i
    array = sio.loadmat(f'Data files/{index[index_num]}')
    array = data_importer.fun_data_format(array)
    data_rate_checker(array)
