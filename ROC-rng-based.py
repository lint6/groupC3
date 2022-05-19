import time
import numpy as np
from numpy import random
# import cupy as cp
import matplotlib.pyplot as plt
n = 19
x_plot1 = [0,1]
y_plot1 = [0,1]
# x_plot2 = np.arange(0,1,0.01)
x_plot2 = np.arange(0,1,1/n)
y_plot2 = (1-(x_plot2-1)**2)**0.5

x_rand = np.zeros(n)
for i in range (n):
    x_rand[i] = 0.03*(random.rand(1)-0.5)

y_plot2 = y_plot2 + x_rand
x_plot2 = x_plot2 +  0.03*(random.rand(1)-0.5)

# print(y_plot2)
print(x_rand)
plt.plot(x_plot1, y_plot1)
plt.scatter(x_plot2, y_plot2, s=1)
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
