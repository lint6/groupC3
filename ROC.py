import numpy as np
import matplotlib.pyplot as plt

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

def fun_ROC


fun_ROC(Manual_Test, Algorithm_Test)
