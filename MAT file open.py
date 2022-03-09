import scipy.io
import numpy as np

#Extracting Data from Matlab
mat = scipy.io.loadmat('S01_MC1_HeadMotion')
data_raw = mat.pop('motiondata')
data_trans = np.transpose(data_raw)

#Scaling the values
#Time column
data_trans[0] = data_trans[0] - data_trans[0][0]
data_trans[0] = data_trans[0] / 10000

#xdotdot
#Framesignature

#Roll raw #Pitch_raw and Yaw Raw
running = True
k = 3
while running:
    data_trans[k] = (data_trans[k]*180)/16383
    if k == 5:
        running = False
    k = k + 1

#X_raw, Y_raw and Z_raw
running = True
k = 6
while running:
    data_trans[k] = (data_trans[k]*180)/16383
    if k == 8:
        running = False
    k = k + 1




#test = -458.286
#test = (test*180)/16383
#print(test)


#Class setup
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

#Defining Class
data = Data(data_trans[0], data_trans[1], data_trans[2], data_trans[3], data_trans[4], data_trans[5], data_trans[6], data_trans[7], data_trans[8])


print(data.Z_raw)




