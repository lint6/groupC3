import scipy.io
import numpy as np

#Extracting Data from Matlab
mat = scipy.io.loadmat('S01_MC1_HeadMotion')
data_raw = mat.pop('motiondata')
data_trans = np.transpose(data_raw)

#Scaling the values
#Time column
data_trans[0] = data_trans[0] - data_trans[0][0]
data_trans[0] = data_trans[0] / 1000


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


print(data.Time)



