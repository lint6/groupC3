import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio
import data_importer
import os

# This code checks whether certain data points are almost equal to previous data points!
# (Almost -> within a certain margin)

# START OF DATA EXTRACTION INTERMEZZO

"""contain function for importing data"""
# Functions


def fun_Index_Gen(foldername):
    presetlist = os.listdir(foldername)
    n = 0
    file_index = []
    # print(f'Total file found: {len(presetlist)}')
    for i in presetlist:
        # print(f'{n} -- {i}')
        file_index.append(i)
        n += 1
    # print(f'Index Finished')
    return file_index


index = fun_Index_Gen("Data files")

# index_num = int(input('Which file number would you like?'))
index_num = 5

# Extracting Data from Matlab
mat = sio.loadmat(f'Data files/{index[index_num]}')


def fun_data_format(mate):
    data_raw = mate.pop('motiondata')
    data_trans = np.transpose(data_raw)
    # Scaling the values
    # Time column
    data_trans[0] = data_trans[0] - data_trans[0][0]
    data_trans[0] = data_trans[0] / 10000

    # Roll raw #Pitch_raw and Yaw Raw
    running = True
    k = 3
    while running:
        data_trans[k] = (data_trans[k]*180)/16383
        if k == 5:
            running = False
        k = k + 1

    # X_raw, Y_raw and Z_raw
    running = True
    k = 6
    while running:
        data_trans[k] = (data_trans[k]*180)/16383
        if k == 8:
            running = False
        k = k + 1
    return data_trans

# Class setup


class Data:
    def __init__(self, Time, xdotdot, FrameSignature, Roll_raw, Pitch_raw, Yaw_raw, X_raw, Y_raw, Z_raw):
        self.Time = Time
        self.xdotdot = xdotdot
        self.FrameSignature = FrameSignature
        self.Roll_raw = Roll_raw
        self.Pitch_raw = Pitch_raw
        self.Yaw_raw = Yaw_raw
        self.X_raw = X_raw
        self.Y_raw = Y_raw
        self.Z_raw = Z_raw


# Defining Class
FormattedData = fun_data_format(mat)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5],
            FormattedData[6], FormattedData[7], FormattedData[8])

# Plotting Data
# give in the two things you want to plot
# variable1 = data.Time
# variable2 = data.Pitch_raw

# plt.plot(variable1, variable2)
# plt.show()

# END OF DATA EXTRACTION INTERMEZZO

# Select data column to analyze and
# vectorize this column of data


# Input which data to take here!!
# Original_Array = data.X_raw
# =======================================================================================


def fun_check_not_updated(Input_Original_Array,
                          Threshold_Margin_Between_Measurements=1000000,
                          Threshold_Consecutive_Not_Updated_Measurements=8):
    # =======================================================================================
    # ADJUST PARAMETERS HERE (2)
    # =======================================================================================
    # Input margin and cons
    # Threshold_Margin_Between_Measurements = 1000000
    # Threshold_Consecutive_Not_Updated_Measurements = 8  # 8 is still okay, more is identified as an outlier
    # =======================================================================================

    # Create a difference array
    Difference_Array = np.diff(Input_Original_Array)
    Difference_Array2 = np.absolute(Difference_Array)

    # Create an array that represents the minimum difference
    # that should be present between two measurements.
    # Every difference below this this margin array
    # will be counted as not-updated measurement
    First_Element_Removed_Array = Input_Original_Array[:-1].copy()
    Nonaccepted_Margin_Array = First_Element_Removed_Array/Threshold_Margin_Between_Measurements
    Nonaccepted_Margin_Array2 = np.absolute(Nonaccepted_Margin_Array)

    # Pinpoint outliers, if the difference is less
    # than a (certain amount) * the first column, reject
    # Compared_Array = Difference_Array - Nonaccepted_Margin_Array
    Is_Not_Updated_Array1 = Difference_Array2 < Nonaccepted_Margin_Array2
    Is_Not_Updated_Array2 = np.append(np.array([False]), Is_Not_Updated_Array1)

    # Converts True-False array to 1-0 array
    # OVERRIDE FOR TESTING
    # Is_Not_Updated_Array2 = np.array([False,True,True,True,False,True,True,False,True,True])

    # Converts True-False array to 1-0 array
    Is_Not_Updated_One_Zero_Array = Is_Not_Updated_Array2 * 1

    # Splits array into sub arrays which are eiter all one or all zero
    # Example: [1,1,0,0,1,1,1] --> [ [1,1], [0,0], [1,1,1] ]
    Splitted_Array_list = np.split(Is_Not_Updated_One_Zero_Array,
                                   np.where(np.diff(Is_Not_Updated_One_Zero_Array) != 0)[0]+1)
    Splitted_Array = np.array(Splitted_Array_list)  # This seems to have fixed one of the issues but not all lol

    # Makes an array that will help to pinpoint starting positions of '1' sequences
    Pinpoint_First_Of_Sequence_Array = 2*(np.append(np.array([1]), np.diff(Is_Not_Updated_One_Zero_Array)))-1

    # Make a sort of function that checks the length of sub-arrays
    function_length_checker = np.vectorize(len)
    Sub_Array_Length_Array = function_length_checker(Splitted_Array)

    # Converts splitted Array back into one big array
    Non_Splitted_Array = np.concatenate(Sub_Array_Length_Array * Splitted_Array)

    # Final step that pinpoints starting positions of '1' sequences, and negative values for repeating ones
    Final_Array = Non_Splitted_Array * Pinpoint_First_Of_Sequence_Array

    # Converting values in Final Array to either '0' if the measurement is properly updated
    # Or '1' is the measurement is probably not updated
    # Lower or equal to this is will be seen as non-updated measurement
    Final_Array[Final_Array >= -Threshold_Consecutive_Not_Updated_Measurements] = 0

    # Returns detected outliers to ones
    Final_Array[Final_Array < 0] = 1
    # Real_Final_Array = np.repeat(Final_Array, 9)
    return Final_Array


Original_Array1 = data.xdotdot
Original_Array2 = data.Roll_raw
Final_Array1 = fun_check_not_updated(Original_Array1)
Final_Array2 = fun_check_not_updated(Original_Array2)


# Counts how many ones are in the Final Array
Ones_Count_1 = np.sum(Final_Array1)
Ones_Count_2 = np.sum(Final_Array2)
Final_Array_Length = len(Final_Array1)
Outlier_Fraction_Array1 = 100 * Ones_Count_1 / Final_Array_Length
Outlier_Fraction_Array2 = 100 * Ones_Count_2 / Final_Array_Length
# Functions for indices


# Yay some useful prints
# print("Type of SubLenArr: ", type(Sub_Array_Length_Array))
# print("Type of SplitArr: ", type(Splitted_Array))
# print("True False Array: ", Is_Not_Updated_Array2)
# print("One Zero Array: ", Is_Not_Updated_One_Zero_Array)
# print("Pinpoint Array: ", Pinpoint_First_Of_Sequence_Array)
# print("Splitted_array: ", Splitted_Array)    # This ones doesn't seem to work yet
print("Final faulty data array for xdotdot: ", Final_Array1)
print("Final_Array2 is: ", Final_Array2)
print("Amount of identified Non-Updated in xdotdot: ", Ones_Count_1)
print("Amount of identified Non-Updated in other data: ", Ones_Count_2)
print('Non-Updated fraction for xdotdot is then: ', Outlier_Fraction_Array1, '%')
print('Non-Updated fraction for other data is then: ', Outlier_Fraction_Array2, '%')
print()
print("Yay looks more accurate than before!")
# print('Not Updated Boolian Array: ', Is_Not_Updated_Array2)
# print("Length of Boolean Array: ", len(Is_Not_Updated_Array2))

Plotted_Final_Array = Final_Array2

# Plot helping variables
xvalues = data.Time    # indices of the data
# plt.plot(xvalues, Plotted_Final_Array, color="red", label='Non-updated values', linewidth=0.3)
# plt.plot(xvalues, Original_Array2, color="blue", label='Original values', linewidth=0.25)
# plt.xlim([12, 12.5])
# plt.ylim([-0.75, 0])
# plt.show()    # Plot here!
