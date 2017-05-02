import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

def mean(x):
    return sum(x)/len(x)

def variance(x, mean):
    return sum(map(lambda x_i: (x_i - mean)**2,x))/len(x)

DATA_DIR = 'data/'
spws = np.genfromtxt(DATA_DIR + 'a_spw_interval.dat', delimiter=' ')

spws_m = mean(spws)
spws_v = variance(spws, spws_m)

x = np.linspace(-3, 3, 100)
#print(spws)
plt.plot(x,mlab.normpdf(x,spws_m, math.sqrt(spws_v)))
plt.show()
