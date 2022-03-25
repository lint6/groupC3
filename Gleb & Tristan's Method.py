import random
import math
import matplotlib.pyplot as plt
import numpy as np
import data_importer

index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?'))
DataArray = data_importer.fun_GetDataRaw(index_num)

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

FormattedData = data_importer.fun_data_format(DataArray)
data = Data(FormattedData[0], FormattedData[1], FormattedData[2], FormattedData[3], FormattedData[4], FormattedData[5], FormattedData[6], FormattedData[7], FormattedData[8])

Time = np.array(data.Time)
Y_raw = np.array(data.Y_raw)
Z = np.array(data.Z_raw)
print(len(Time))
k = 100  # neighborhood window width
tau = 1  # a specified threshold
x_step = 0.01  # Increments of x

def method(data, clean, threshold, width):
    for i in range(len(data) - (2 * width)):
        #print(i + 2 * width + 1)
        #print(data[i:(i + 2 * width + 1)])
        avg = np.average(data[i:(i + 2 * width + 1)])
        if abs(data[i + width] - avg) > threshold:
            clean[i + width] = None
    return clean


def method_vectorized(data, clean, threshold, width):
    y_hat = data
    index = 2 * width + 1
    y_median = y_hat
    for i in range(index - 1):
        y_hat = np.insert(y_hat, 0, 0)
        y_hat = np.delete(y_hat, -1)
        y_median += y_hat
    y_median = y_median / index
    check = abs(data - y_median) > threshold
    print(check)
    clean[check] = None
    print(clean)
    return


def dummy_data(x):
    decide = random.randint(0, 10)  # One in 10 change of an outlier
    range = 2
    a = 2  # Scaling value
    outlier_range = 20
    if decide == 1:
        y = random.uniform(-outlier_range, outlier_range)
    else:
        offset = random.uniform(-range, range)
        y = a * math.sin(x) + offset
    return y

plt.scatter(Time, Y_raw, s=1)
# x_array = np.arange(0, 2 * np.pi, x_step)
# y_array = np.array([dummy_data(x) for x in x_array])
Y_raw_copy = Y_raw.copy()
# y_array_3 = y_array.copy()
# # y_array_4 = y_array.copy()
y_array_filtered = method(Y_raw, Y_raw_copy, tau, k)
plt.scatter(Time, y_array_filtered, s=1)

# plt.subplot(2, 2, 1)
# plt.plot(x_array, y_array)
# plt.plot(x_array, y_array_filtered)
# y_array_filtered_vectorized = method_vectorized(y_array, y_array_3, tau, k)
# plt.subplot(2, 2, 2)
# plt.plot(x_array, y_array_4)
# plt.plot(x_array, y_array_filtered_vectorized)
plt.show()
