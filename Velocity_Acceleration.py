import numpy as np
import data_importer
import scipy.io as sio

def rewriter_1(array_in, index_num):
    global index
    #print(array_in)
    #print(np.shape(array_in))
    if index_num < 2:
        with open (f'csv_derive_data/{index[index_num]}_derive.csv',"w") as f:
            f.write("")
        with open (f'csv_derive_data/{index[index_num]}_derive.csv', 'a') as f:
            for i in range(len(array_in[0])):
                if i % 4 == 0:
                    f.write(f'{array_in[1][i]},{array_in[2][i]},{array_in[3][i]},{array_in[4][i]},{array_in[5][i]},{array_in[6][i]}')
                    #x, y, z, roll, pitch, yaw
                    f.write("\n")
    else:
        with open (f'csv_derive_data/{index[index_num]}_derive.csv',"w") as f:
            f.write("")
        with open (f'csv_derive_data/{index[index_num]}_derive.csv', 'a') as f:
            for i in range(len(array_in[0])):
                f.write(f'{array_in[6][i]},{array_in[7][i]},{array_in[8][i]},{array_in[3][i]},{array_in[4][i]},{array_in[5][i]}')
                #x, y, z, roll, pitch, yaw
                f.write("\n")
    print('done')

def rewriter_2(array_in, index_num):
    global index
    #print(array_in)
    #print(np.shape(array_in))
    if index_num < 2:
        with open (f'csv_derive_data/{index[index_num]}_derive_2.csv',"w") as f:
            f.write("")
        with open (f'csv_derive_data/{index[index_num]}_derive_2.csv', 'a') as f:
            for i in range(len(array_in[0])):
                if i % 4 == 0:
                    f.write(f'{array_in[1][i]},{array_in[2][i]},{array_in[3][i]},{array_in[4][i]},{array_in[5][i]},{array_in[6][i]}')
                    #x, y, z, roll, pitch, yaw
                    f.write("\n")
    else:
        with open (f'csv_derive_data/{index[index_num]}_derive_2.csv',"w") as f:
            f.write("")
        with open (f'csv_derive_data/{index[index_num]}_derive_2.csv', 'a') as f:
            for i in range(len(array_in[0])):
                f.write(f'{array_in[6][i]},{array_in[7][i]},{array_in[8][i]},{array_in[3][i]},{array_in[4][i]},{array_in[5][i]}')
                #x, y, z, roll, pitch, yaw
                f.write("\n")
    print('done')

dt = 0.04

index = data_importer.fun_Index_Gen("Data files")

write = str(input("write csv? (Y/N)\n"))

if write.upper() == 'Y':
    for i in range (26):
        print(f'\nData file{i}')
        array = sio.loadmat(f'Data files/{index[i]}')
        array = data_importer.fun_DataFormat(array)

        array_pad_f = np.pad(array, ((0,0),(1,0)))
        array_pad_b = np.pad(array, ((0,0),(0,1)))
        array_derive = (array_pad_f - array_pad_b)/dt
        array_derive = np.delete(np.delete(array_derive, -1, 1), 0, 1)

        array_derive_f = np.pad(array_derive, ((0,0),(1,0)))
        array_derive_b = np.pad(array_derive, ((0,0),(0,1)))
        array_derive_2 = array_derive_f - array_derive_b
        array_derive_2 = np.delete(np.delete(array_derive_2, -1, 1), 0, 1)

        print (np.shape(array_derive))
        rewriter_1(array_derive, i)
        rewriter_2(array_derive, i)

graph = str(input('Graph data? (Y/N)')).upper()

while graph == 'Y':
