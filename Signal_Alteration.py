import numpy as np
import scipy.io as sio
"""
SIGNAL ALTERATION
"""

# Loading one of the documents
mat = sio.loadmat(f'Data files/S06_MC1_HeadMotion.mat')
data_raw = mat.pop('motiondata')
data_trans = np.transpose(data_raw)

Results = []


def fun_alteration_row(data_trans):
    # Runs over all columns of the data
    for i in range(9):
        # Puts a zero after/before the data array
        data = data_trans[i]
        data_ = np.pad(data, (0, 1), constant_values=0)
        _data = np.pad(data, (1, 0), constant_values=0)

        # Figuring out whether the slope of two succeeding data points is +/-
        Slope = data_ - _data

        # Puts a zero after/before the slope array
        _Slope = np.pad(Slope, (1, 0), constant_values=0)
        Slope_ = np.pad(Slope, (0, 1), constant_values=0)

        # Creates an array to find out whether the slope of two succeeding data points is the same
        # (+ means the same slope, - means different slope)
        Signs = np.sign(_Slope * Slope_)
        Negative_Index = np.where(Signs == -1)[0]

        Data_Index = []
        Change_Min = 0.01

        # Runs over all negative indexes to see if they are adjacent
        # If adjacent, there is signal alteration
        for j in range(len(Negative_Index) - 1):
            # Checks if the slopes are different, and the value changes with more than the minimum
            if Negative_Index[j] - Negative_Index[j + 1] == -1 and \
                    abs(data[Negative_Index[j] - 1] - data[Negative_Index[i]]) > Change_Min:
                Data_Index.append(Negative_Index[j] - 1)
                Data_Index.append(Negative_Index[j])
                # print(data[Negative_Index[j] - 2], data[Negative_Index[j] - 1],
                #       data[Negative_Index[j]], data[Negative_Index[j] + 1])

        Results.append(Data_Index)

    # Prints the amount of alterations per column
    for i in range(len(Results)):
        print(len(Results[i]))

    # Creates an array the shape of all data andputs in 1 if there is an alteration
    Alterations = np.zeros((9, len(data_trans[0])))

    for Data_Type in range(len(Results)):
        for Idx in Results[Data_Type]:
            Alterations[Data_Type][Idx] = 1
    # print(Alterations)

    # idx = int(input("Which dataset do you want to use?:\n"
    #                 "Time= 0\n"
    #                 "xdotdot = 1\n"
    #                 "FrameSignature= 3\n"
    #                 "Roll_raw = 4\n"
    #                 "Pitch_raw = 5\n"
    #                 "Yaw_raw = 6\n"
    #                 "X_raw = 7\n"
    #                 "Y_raw= 8\n"
    #                 "Z_raw = 9\n"
    #                 "Insert Number: "))

    # print(Alterations[idx])
    # print(sum(Alterations[idx]))
    # print(len(Results[idx]))
    # print((Results[idx]))


def fun_alteration_column(data_trans):
    Expected_Array = np.empty((len(data_trans), len(data_trans[0]) - 2))
    print(data_trans)
    for i in range(len(data_trans)):
        # Puts a zero after/before the data array
        data = data_trans[i]
        data__ = np.pad(data, (0, 2), constant_values=0)
        __data = np.pad(data, (2, 0), constant_values=0)

        Expected_Data = (data__ + __data) * 1/2
        Expected_Data = Expected_Data[2:-2]
        Expected_Array[i] = Expected_Data

    print(Expected_Array)

    Idx_array = []
    min_change = 0.001
    min_difference = 0.1

    for col1 in range(len(data_trans)):
        for col2 in range(col1 + 1, len(data_trans)):
                Expected1_min_Data1 = abs(Expected_Array[col1] - data_trans[col1][1:-1])
                Idx_Expected1_min_Data1 = np.where(Expected1_min_Data1 > min_change)[0]

                Expected2_min_Data2 = abs(Expected_Array[col2] - data_trans[col2][1:-1])
                Idx_Expected2_min_Data2 = np.where(Expected2_min_Data2 > min_change)[0]

                Expected1_min_Data2 = abs(Expected_Array[col1] - data_trans[col2][1:-1])
                Idx_Expected1_min_Data2 = np.where(Expected1_min_Data2 < min_difference)[0]

                Expected2_min_Data1 = abs(Expected_Array[col2] - data_trans[col1][1:-1])
                Idx_Expected2_min_Data1 = np.where(Expected2_min_Data1 < min_difference)[0]

                Idx_list = []
                for Idx11 in Idx_Expected1_min_Data1:
                    # for Idx22 in Idx_Expected2_min_Data2:
                    #     for Idx12 in Idx_Expected1_min_Data2:
                    #         for Idx21 in Idx_Expected2_min_Data1:
                    if Idx11 in Idx_Expected2_min_Data2 \
                            and Idx11 in Idx_Expected1_min_Data2 \
                            and Idx11 in Idx_Expected2_min_Data1 \
                            and abs(data_trans[col1][Idx11+1] - data_trans[col2][Idx11+1]) > 0.05:
                        Idx_list.append([Idx11 + 1, col1, col2])

                print(col1, col2)

                Idx_array.append(Idx_list)

    print(Idx_array)
    for i in range(len(Idx_array)):
        for j in range(len(Idx_array[i])):
            idx = Idx_array[i][j][0]
            col1 = Idx_array[i][j][1]
            col2 = Idx_array[i][j][2]
            print(data_trans[col1][idx - 1], data_trans[col1][idx], data_trans[col1][idx + 1])
            print(data_trans[col2][idx - 1], data_trans[col2][idx], data_trans[col2][idx + 1])
            print("")

# fun_alteration_row(data_trans)

test_array = np.array(
    [[1, 2, 3, 4, 12, 6, 7],
    [8, 9, 10, 11, 5, 13, 14]])

fun_alteration_column(data_trans)


