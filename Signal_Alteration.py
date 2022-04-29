import numpy as np
import scipy.io as sio
#has to run after spike removal?????!!!
"""
SIGNAL ALTERATION
Input files are the raw data
"""

# Loading one of the documents
mat = sio.loadmat(f'Data files/S10_MC1_HeadMotion.mat')
data_raw = mat.pop('motiondata')

# data_raw = [[0, 1, 0, 0, 1, 1],[1, 1, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1],[0, 1, 1, 0, 0, 1]]

def fun_alteration_row(data_raw, Change_Min=1000): #treshold
    data_trans = np.transpose(data_raw)
    Results = []

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

    ### Prints the amount of alterations per column
    for i in range(len(Results)):
        print(len(Results[i]))

    # Creates an array the shape of all data and puts in 1 if there is an alteration
    Alterations_Row = np.zeros((9, len(data_trans[0])))

    for Data_Type in range(len(Results)):
        for Idx in Results[Data_Type]:
            Alterations_Row[Data_Type][Idx] = 1
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

    return Alterations_Row


def fun_alteration_column(data_raw, min_change=0.05, min_difference=0.1, min_overlap=0.02):
    data_trans = np.transpose(data_raw) #9rows 45005 columns
    Expected_Array = np.empty((len(data_trans), len(data_trans[0]) - 2))

    for i in range(len(data_trans)):
        # Puts a zero after/before the data array
        data = data_trans[i]
        data__ = np.pad(data, (0, 2), constant_values=0)
        __data = np.pad(data, (2, 0), constant_values=0)

        # Creates array of expected data at all points, based on previous and next point
        Expected_Data = (data__ + __data) * 1/2
        Expected_Data = Expected_Data[2:-2]
        Expected_Array[i] = Expected_Data

    Idx_array = []

    # Runs over all combinations of column to cross-check all of them
    # Column 1 (time) is skipped, since it is most likely perfect, and it messed things up
    for col1 in range(1, len(data_trans)):
        for col2 in range(col1 + 1, len(data_trans)):
            # Looks at the difference between the expected data of column 1
            # And compares it to the real data of column 1
            Expected1_min_Data1 = abs(Expected_Array[col1] - data_trans[col1][1:-1])
            Idx_Expected1_min_Data1 = np.where(Expected1_min_Data1 > min_change)[0]

            # Looks at the difference between the expected data of column 2
            # And compares it to the real data of column 2
            Expected2_min_Data2 = abs(Expected_Array[col2] - data_trans[col2][1:-1])
            Idx_Expected2_min_Data2 = np.where(Expected2_min_Data2 > min_change)[0]

            # Looks at the difference between the expected data of column 1
            # And compares it to the real data of column 2
            Expected1_min_Data2 = abs(Expected_Array[col1] - data_trans[col2][1:-1])
            Idx_Expected1_min_Data2 = np.where(Expected1_min_Data2 < min_difference)[0]

            # Looks at the difference between the expected data of column 2
            # And compares it to the real data of column 1
            Expected2_min_Data1 = abs(Expected_Array[col2] - data_trans[col1][1:-1])
            Idx_Expected2_min_Data1 = np.where(Expected2_min_Data1 < min_difference)[0]

            # Looks at whether the two real data point not just closely overlap at timestamp by coincidence
            Data1_min_Data2 = abs(data_trans[col1][1:-1] - data_trans[col2][1:-1])
            Idx_Data1_min_Data2 = np.where(Data1_min_Data2 > min_overlap)[0]

            # Add arrays together and sorts them
            Sorted_Array = np.sort(np.concatenate((Idx_Expected1_min_Data1, Idx_Expected2_min_Data2,
                                                   Idx_Expected2_min_Data1, Idx_Expected1_min_Data2,
                                                   Idx_Data1_min_Data2)))

            # Splits array in sub arrays where each element has the same value
            # Example: [1,1,2,5,5,5,7,7] --> [ [1,1] , [2] , [5,5,5] , [7,7] ]
            Splitted_Array = np.array(np.split(Sorted_Array, np.where(np.diff(Sorted_Array) != 0)[0] + 1),
                                      dtype="object")

            # Creates output array (Four_Times_Present_Array)
            # that is '1' when a sub array has length four.
            # Or '0' when it is not four in length.
            fun_length_checker = np.vectorize(len)
            Length_Array = fun_length_checker(Splitted_Array)
            Four_Times_Present_Array = np.where(Length_Array == 5, 1, 0)

            # Array that is '1' whenever a new value compared to previous appears
            # Example: [1,3,3,3,5,5]
            #     '--> [1,1,0,0,1,0]
            Pinpoint_Array = np.where(np.concatenate((np.array([1]), np.diff(Sorted_Array))) > 0, 1, 0)

            # Smushes everything together
            # Result: An array where every value that appears in all four
            # input arrays is once in this array. Also, a bunch of zeroes
            Zeroed_Array = np.concatenate(Four_Times_Present_Array * Splitted_Array) * Pinpoint_Array

            Zero_Eliminated_Array = Zeroed_Array[Zeroed_Array != 0]

            Idx_list = []
            for idx in Zero_Eliminated_Array:
                Idx_list.append([idx + 1, col1, col2])

            # print(f"col{col1}, col{col2}")
            # print("Zero_Eliminated_Array:\n", Idx_list)

            Idx_array.append(Idx_list)

    # Creates an array the shape of all data and puts in 1 if there is an alteration
    Alterations_Column = np.zeros((len(data_trans), len(data_trans[0])))

    for Data_Type_idx in range(len(Idx_array)):
        for Alteration_Idx in range(len(Idx_array[Data_Type_idx])):
            row = Idx_array[Data_Type_idx][Alteration_Idx][0]
            column1 = Idx_array[Data_Type_idx][Alteration_Idx][1]
            column2 = Idx_array[Data_Type_idx][Alteration_Idx][2]

            Alterations_Column[column1][row] = 1
            Alterations_Column[column2][row] = 1

    # for i in range(len(Idx_array)):
    #     for j in range(len(Idx_array[i])):
    #         idx = Idx_array[i][j][0]
    #         col1 = Idx_array[i][j][1]
    #         col2 = Idx_array[i][j][2]
    #         print(data_trans[col1][idx - 1], data_trans[col1][idx], data_trans[col1][idx + 1])
    #         print(data_trans[col2][idx - 1], data_trans[col2][idx], data_trans[col2][idx + 1])
    #         print("Difference: ", round(abs(data_trans[col1][idx] - data_trans[col2][idx]), 4))
    #         print("")

    return Alterations_Column

# test_array = np.array([[1, 2, 3, 4, 12, 6, 7],
#                         [8, 9, 10, 11, 5, 13, 14]])
Alterations_Row = fun_alteration_row(data_raw)
# Alterations_Row = fun_alteration_row(test_array)


print(np.count_nonzero(Alterations_Row), "Are the amount of signal alterations in the rows")

#
# Alterations_Column = fun_alteration_column(test_array)
Alterations_Column = fun_alteration_column(data_raw)

print(np.count_nonzero(Alterations_Column), "Are the amount of signal alterations in the columns")
