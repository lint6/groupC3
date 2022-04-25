import time
import numpy as np
import Signal_Alteration
import matplotlib.pyplot as plt
import scipy.io as sio
import itertools as it

Manual_Test = np.array([[1, 0, 0, 1, 1, 0],
                        [0, 0, 1, 0, 0, 0],
                        [1, 1, 0, 0, 0, 0],
                        [0, 1, 0, 1, 0, 0]])

Algorithm_Test = np.array([[0, 1, 0, 0, 1, 1],
                           [1, 1, 0, 0, 1, 1],
                           [1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 0, 0, 1]])


def fun_Rates(Manual, Algorithm):
    Difference_Array = Manual * 2 - Algorithm
    # print(Difference_Array)
    # DA = 1   : True positive (Correctly found anomaly)
    # DA = 0   : True Negative (Correctly found no anomaly)
    # DA = -1  : False positive (Incorrectly not found anomaly)
    # DA = 2   : False negative (Incorrectly found anomaly)

    TP = len(np.where(Difference_Array == 1)[0])
    TN = len(np.where(Difference_Array == 0)[0])
    FP = len(np.where(Difference_Array == -1)[0])
    FN = len(np.where(Difference_Array == 2)[0])

    P = TP + FN
    N = FP + TN
    # PP = TP + FP
    # PN = FN + TN

    TPR = TP/P  # True Positive Rate or Sensitivity
    FPR = FP/N  # False Positive Rate or Fall-out
    FNR = FN/P  # False Negative Rate or Miss rate
    TNR = TN/N  # True Negative Rate
    Jaccard = TP / (TP+FP+FN)

    return TPR, FPR, FNR, TNR, Jaccard


# def fun_ROC_curves(function, parameter1=None, parameter2=None, parameter3=None): #the first iteration of the function we implemented
#     start_time = time.time()
#     mat = sio.loadmat(f'Data files/S11_MC1_HeadMotion.mat')
#     data_raw = mat.pop('motiondata')
#
#     Dummy_List = [0, 1, 1]
#     if parameter3 is None:
#         parameter3 = Dummy_List
#     if parameter2 is None:
#         parameter2 = Dummy_List
#     if parameter1 is None:
#         parameter1 = Dummy_List
#
#     start1 = parameter1[0]
#     stop1 = parameter1[1]
#     steps1 = parameter1[2]
#
#     start2 = parameter2[0]
#     stop2 = parameter2[1]
#     steps2 = parameter2[2]
#
#     start3 = parameter3[0]
#     stop3 = parameter3[1]
#     steps3 = parameter3[2]
#
#     TPR = []
#     FPR = []
#     FNR = []
#     TNR = []
#     Jaccard = []
#     Parameter1_list = []
#     Parameter2_list = []
#     Parameter3_list = []
#
#     Manual = function(data_raw, 0.07)
#
#     for Parameter1 in np.linspace(start1, stop1, steps1):
#         for Parameter2 in np.linspace(start2, stop2, steps2):
#             for Parameter3 in np.linspace(start3, stop3, steps3):
#                 if parameter2 is Dummy_List:
#                     Algorithm = function(data_raw, Parameter1)
#                 elif parameter3 is Dummy_List:
#                     Algorithm = function(data_raw, Parameter1, Parameter2)
#                 else:
#                     Algorithm = function(data_raw, Parameter1, Parameter2, Parameter3)
#
#                 rates = fun_Rates(Manual, Algorithm)
#
#                 TPR.append(rates[0])
#                 FPR.append(rates[1])
#                 FNR.append(rates[2])
#                 TNR.append(rates[3])
#                 Jaccard.append(rates[4])
#                 Parameter1_list.append(Parameter1)
#                 Parameter2_list.append(Parameter2)
#                 Parameter3_list.append(Parameter3)
#
#     plt.scatter(FPR, TPR)
#     print(max(Jaccard))
#     print(np.where(abs(np.array(Jaccard) - max(Jaccard)) < 1e-15)[0])
#     print(Parameter1_list[np.where(abs(np.array(Jaccard) - max(Jaccard)) < 1e-15)[0][0]])
#     plt.xlim(0, 1)
#     plt.ylim(0, 1)
#     plt.xlabel("FPR")
#     plt.ylabel("TPR")
#     plt.title("ROC-curve")
#     plt.show()
#
#     print("--- %s seconds ---" % (time.time() - start_time))


def fun_ROC_curves2(function, parameter1=None, parameter2=None, parameter3=None): #the optimized function for the ROC curve
    start_time = time.time()

    mat = sio.loadmat(f'Data files/S11_MC1_HeadMotion.mat')
    data_raw = mat.pop('motiondata')

    Dummy_List = [0, 1, 1]
    if parameter3 is None:
        parameter3 = Dummy_List
    if parameter2 is None:
        parameter2 = Dummy_List
    if parameter1 is None:
        parameter1 = Dummy_List

    start1 = parameter1[0]
    stop1 = parameter1[1]
    steps1 = parameter1[2]

    start2 = parameter2[0]
    stop2 = parameter2[1]
    steps2 = parameter2[2]

    start3 = parameter3[0]
    stop3 = parameter3[1]
    steps3 = parameter3[2]

    options1 = np.linspace(start1, stop1, steps1)
    options2 = np.linspace(start2, stop2, steps2)
    options3 = np.linspace(start3, stop3, steps3)

    options = np.array([options1, options2, options3], dtype="object")

    combinations = it.product(*options)

    length = steps1 * steps2 * steps3

    TPR = np.empty(length)
    FPR = np.empty(length)
    FNR = np.empty(length)
    TNR = np.empty(length)
    Jaccard = np.empty(length)
    Combination_list = np.empty(length, dtype="object")

    Manual = function(data_raw, 0.07)

    i = 0

    # print("--- %s seconds ---" % (time.time() - start_time))
    for comb1, comb2, comb3 in combinations:
        if parameter2 is Dummy_List:
            Algorithm = function(data_raw, comb1)
        elif parameter3 is Dummy_List:
            Algorithm = function(data_raw, comb1, comb2)
        else:
            Algorithm = function(data_raw, comb1, comb2, comb3)

        rates = fun_Rates(Manual, Algorithm)

        TPR[i] = rates[0]
        FPR[i] = rates[1]
        FNR[i] = rates[2]
        TNR[i] = rates[3]
        Jaccard[i] = rates[4]
        Combination_list[i] = [comb1, comb2, comb3]

        i += 1

    print(np.max(Jaccard))
    print(np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)[0])
    print(Combination_list[np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)[0][0]])
    # X = [0, 0.2, 0.4, 0.6, 0.8, 1]
    # Y = [0, 0.2, 0.4, 0.6, 0.8, 1]

    plt.scatter(FPR, TPR)
    plt.plot(FPR[np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)], TPR[np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)], marker="o", markerfacecolor="red")
    # plt.plot(X,Y)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC-curve")
    plt.show()

    print("--- %s seconds ---" % (time.time() - start_time))


# fun_Rates(Manual_Test, Algorithm_Test)
# fun_ROC_curves(Signal_Alteration.fun_alteration_row, [0, 1, 500])

fun_ROC_curves2(Signal_Alteration.fun_alteration_row, [0, 1, 200])
