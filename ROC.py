import numpy as np

Manual_Test = np.array([[1, 0, 0, 1, 1, 0],
                        [0, 0, 1, 0, 0, 0],
                        [1, 1, 0, 0, 0, 0],
                        [0, 1, 0, 1, 0, 0]])

Algorithm_Test = np.array([[0, 1, 0, 0, 1, 1],
                           [1, 1, 0, 0, 1, 1],
                           [1, 1, 1, 1, 1, 1],
                           [0, 1, 1, 0, 0, 1]])


def fun_ROC(Manual, Algorithm):
    Difference_Array = Manual - Algorithm
    print(Difference_Array)
    # DA=0 & Algorithm=1: True positive (Correctly found anomaly)
    # DA=0 & Algorithm=0: True Negative (Correctly found no anomaly)
    # DA=1              : False positive (Incorrectly not found anomaly)
    # DA=-1             : False negative (Incorrectly found anomaly)
    # TP = np.where(Difference_Array == 0 and Algorithm == 1)
    # TN = np.where(Difference_Array == 0 and Algorithm == 0)
    TP = [[]] * len(Algorithm)
    TN = [[]] * len(Algorithm)

    DA_0_coord = np.where(Difference_Array == 0)
    A_1_coord = np.where(Algorithm == 1)
    A_0_coord = np.where(Algorithm == 0)

    DA_0 = np.zeros((len(Algorithm), len(Algorithm[0])))
    A_1 = np.zeros((len(Algorithm), len(Algorithm[0])))
    A_0 = np.zeros((len(Algorithm), len(Algorithm[0])))

    for idx in range(len(DA_0_coord[0])):
        DA_0[DA_0_coord[0][idx]][DA_0_coord[1][idx]] = 1

    FP = len(np.where(Difference_Array == 1)[0])
    FN = len(np.where(Difference_Array == -1)[0])

    print(DA_0_coord)
    print(DA_0)
    print(TP)
    print(TN)
    print(FP)
    print(FN)


fun_ROC(Manual_Test, Algorithm_Test)
