import time
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import itertools as it
from PLR_Final import OutlierMatrix, PerRemoved

# import Signal_Alteration
import data_not_updated

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
    PP = TP + FP
    PN = FN + TN

    TPR = TP/P  # True Positive Rate or Sensitivity
    FPR = FP/N  # False Positive Rate or Fall-out
    FNR = FN/P  # False Negative Rate or Miss rate
    TNR = TN/N  # True Negative Rate
    Jaccard = TP / (TP+FP+FN)

    return TPR, FPR, FNR, TNR, Jaccard


def fun_ROC_curves2(function, parameter1=None, parameter2=None, parameter3=None):  # the optimized function for the ROC curve

    mat = sio.loadmat(f'Data files/S10_MC2_HeadMotion.mat')
    data_raw = mat.pop('motiondata')
    data_raw = np.transpose(data_raw)

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

    options1 = np.arange(start1, stop1, steps1)
    options2 = np.arange(start2, stop2, steps2)
    options3 = np.linspace(start3, stop3, steps3)

    options = np.array([options1, options2, options3], dtype="object")

    combinations = it.product(*options)

    length = 100 * (stop2-start2)

    TPR = np.empty(length)
    FPR = np.empty(length)
    FNR = np.empty(length)
    TNR = np.empty(length)
    Jaccard = np.empty(length)
    Combination_list = np.empty(length, dtype="object")
    TPR2 = np.empty(length)
    FPR2 = np.empty(length)
    FNR2 = np.empty(length)
    TNR2 = np.empty(length)
    Jaccard2 = np.empty(length)
    Combination_list2 = np.empty(length, dtype="object")

    Manual = np.transpose(np.genfromtxt("Manual_Value_Spikes_S10MC2.csv", delimiter=";"))[9]

    i = 0

    for comb1, comb2, comb3 in combinations:
        if parameter2 is Dummy_List:
            Algorithm = function(data_raw, comb1)
        elif parameter3 is Dummy_List:
            Algorithm = function(data_raw[2], comb1, comb2)
        else:
            Algorithm = function(data_raw, comb1, comb2, comb3)

        rates = fun_Rates(Manual, Algorithm)
        rates2 = fun_Rates(Manual, OutlierMatrix[1,0:44998]) #compare outlier matrix to Algorithm

        TPR[i] = rates[0]
        FPR[i] = rates[1]
        FNR[i] = rates[2]
        TNR[i] = rates[3]
        Jaccard[i] = rates[4]
        Combination_list[i] = [comb1, comb2, comb3]
        TPR2[i] = rates2[0]
        FPR2[i] = rates2[1]
        FNR2[i] = rates2[2]
        TNR2[i] = rates2[3]
        Jaccard2[i] = rates2[4]
        Combination_list2[i] = [comb1, comb2, comb3]

        # print(comb2, Jaccard[i], len(np.where(Algorithm == 1)[0]))

        i += 1

    # print(np.max(Jaccard))
    # print(np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)[0])
    # print(Combination_list[np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)[0][0]])
    X = [0, 1]
    Y = [0, 1]

    # plt.scatter(FPR, TPR)
    plt.plot(FPR[np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)], TPR[np.where(abs(Jaccard - np.max(Jaccard)) < 1e-15)], marker="o", markerfacecolor="red")
    plt.plot(FPR2[np.where(abs(Jaccard2 - np.max(Jaccard2)) < 1e-15)],
             TPR2[np.where(abs(Jaccard2 - np.max(Jaccard2)) < 1e-15)], marker="o", markerfacecolor="blue")
    plt.plot(X, Y)
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC-curve")
    plt.show()



# fun_Rates(Manual_Test, Algorithm_Test)
# fun_ROC_curves2(Signal_Alteration.fun_alteration_row, [0, 1, 500])

fun_ROC_curves2(data_not_updated.fun_check_not_updated, [10000, 1000001, 10000], [8, 9, 1])
