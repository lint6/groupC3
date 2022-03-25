import data_importer
import numpy as np
import scipy.io as sio

def rewriter(array_in, index_num):
    global index
    #print(array_in)
    #print(np.shape(array_in))
    if index_num < 2:
        with open (f'csv_data/{index[index_num]}.csv',"w") as f:
            f.write("")
        with open (f'csv_data/{index[index_num]}.csv', 'a') as f:
            for i in range(len(array_in[0])):
                if i % 4 == 0:
                    f.write(f'{array_in[1][i]},{array_in[2][i]},{array_in[3][i]},{array_in[4][i]},{array_in[5][i]},{array_in[6][i]}')
                    #x, y, z, roll, pitch, yaw
                    f.write("\n")
    else:
        with open (f'csv_data/{index[index_num]}.csv',"w") as f:
            f.write("")
        with open (f'csv_data/{index[index_num]}.csv', 'a') as f:
            for i in range(len(array_in[0])):
                f.write(f'{array_in[6][i]},{array_in[7][i]},{array_in[8][i]},{array_in[3][i]},{array_in[4][i]},{array_in[5][i]}')
                #x, y, z, roll, pitch, yaw
                f.write("\n")
    print('done')

index = data_importer.fun_Index_Gen("Data files")
#index_num = int(input('Which file number would you like?'))
for i in range(26):
    print(f'\nData file{i}')
    array = sio.loadmat(f'Data files/{index[index_num]}')
    array = data_importer.fun_DataFormat(array)
    rewriter(array, i)
