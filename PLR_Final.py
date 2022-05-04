import data_importer
import matplotlib.pyplot as plt

index = data_importer.fun_Index_Gen("Data files")
index_num = int(input('Which file number would you like?\n'))
DataArray = data_importer.fun_GetDataRaw(index_num, index)

FormattedData = data_importer.fun_data_format(DataArray)
OutlierMatrixOnes, PerRemoved = data_importer.fun_BuildFinalProd(FormattedData[0])
plot = int(input("Do you want the algorithm to plot the individual graphs? \n Yes (type: 1) \n No (type: 0) \n"))

for z in range(6):
    Test = z + 3
    ############################ VARIABLE DEFINING ##############################
    variable1 = FormattedData[0]                                   # USUALLY TIME
    variable2 = FormattedData[Test]
    NumberOfSplits = 10
    DegreeOfPoly = 6
    Thresh = data_importer.fun_FindThresh(variable2)
    plt.plot(variable1, variable2, color = 'g')
    k=0

    ArraySplitT, ArraySplitV = data_importer.fun_SplittingArrays(NumberOfSplits, variable1, variable2)
    if plot == 1:
        plt.plot(variable1, variable2, color='g')
        NumberOfRemovedValues, TimesAreNotOutlier = data_importer.fun_LinearRegressionAlgorithm(ArraySplitT,ArraySplitV,k ,Thresh,NumberOfSplits,variable1,variable2,DegreeOfPoly)
    elif plot == 0:
        NumberOfRemovedValues, TimesAreNotOutlier = data_importer.fun_NoPlotLinearRegressionAlgorithm(ArraySplitT,ArraySplitV, k, Thresh, NumberOfSplits,variable1, variable2,DegreeOfPoly)
    else:
        print('You did not type 0 or 1, please rerun the program and type it correctly.')
        dummy = input("")
    OutlierMatrix = data_importer.fun_FillInFinalProd(OutlierMatrixOnes, TimesAreNotOutlier, (z+1))
    PerRemoved[0][z]= (NumberOfRemovedValues/len(FormattedData[0]))*100

print(OutlierMatrix)
print(PerRemoved)
