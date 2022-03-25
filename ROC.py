import numpy as np
import Signal_Alteration
import matplotlib.pyplot as plt
import scipy.io as sio

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
    print(Difference_Array)
    # DA=1   : True positive (Correctly found anomaly)
    # DA=0   : True Negative (Correctly found no anomaly)
    # DA=-1  : False positive (Incorrectly not found anomaly)
    # DA=2   : False negative (Incorrectly found anomaly)

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
    TNR = TN/N

    print(TP)
    print(TN)
    print(FP)
    print(FN)

    return TPR, FPR, FNR, TNR

# [start1, stop1, stop2]


def fun_ROC_curves(function, parameter1=None, parameter2=None, parameter3=None):
    mat = sio.loadmat(f'Data files/S09_MC1_HeadMotion.mat')
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

    TPR = []
    FPR = []
    FNR = []
    TNR = []

    Manual = []

    for Parameter1 in np.linspace(start1, stop1, steps1):
        Manual = function(data_raw, Parameter1)
        for Parameter2 in np.linspace(start2, stop2, steps2):
            for Parameter3 in np.linspace(start3, stop3, steps3):
                if parameter2 is Dummy_List:
                    Algorithm = function(data_raw, Parameter1)
                elif parameter3 is Dummy_List:
                    Algorithm = function(data_raw, Parameter1, Parameter2)
                else:
                    Algorithm = function(data_raw, Parameter1, Parameter2, Parameter3)

                rates = fun_Rates(Manual, Algorithm)

                TPR.append(rates[0])
                FPR.append(rates[1])
                FNR.append(rates[2])
                TNR.append(rates[3])

    plt.scatter(FPR, TPR)

    plt.show()


# fun_Rates(Manual_Test, Algorithm_Test)
fun_ROC_curves(Signal_Alteration.fun_alteration_row, [0, 1, 5])
