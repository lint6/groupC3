import data_importer
import numpy as np
import scipy.io as sio

def fun_hole_checker(array_in, length):
    # Function to check for holes in data, this assumes missing data are either zero or missing
    # 'array_in' should be an narray of the data
    # 'length' should be the expacted length of the data

    hole_array = np.where(array_in != 0, 0, 1)
    if len(hole_array) != length:
        raise ValueError('Length of the array is shorter than expacted, missing data detected')
    hole_array = np.nonzero(hole_array) # find location of all zero value within array_in
    
    return hole_array



index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?'))
mat = sio.loadmat(f'Data files/{index[index_num]}')

array = data_importer.fun_data_format(mat)

print(fun_hole_checker(array, len(array)))
