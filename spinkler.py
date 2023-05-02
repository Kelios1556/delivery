import time
import numpy as np
import math
from itertools import product, combinations
length = 8 
width = 8
P_r = [1, 2, 3]
netR = min(P_r)
P = 5
x = [0, 0, 0, 0, 0]
y = [0, 0, 0, 0, 0]
r = [netR, netR, netR, netR, netR]
netL = (int)(length / netR)
netW = (int)(width / netR)

def dis(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def sprinkler_range(x, y, r):
    P_x_min = x[0] - r[0]
    P_x_max = x[0] + r[0]
    P_y_min = y[0] - r[0]
    P_y_max = y[0] + r[0]
    for i in range(1, P):
        if P_x_min > x[i] - r[i]: P_x_min = x[i] - r[i]
        if P_x_max < x[i] + r[i]: P_x_max = x[i] + r[i]
        if P_y_min > y[i] - r[i]: P_y_min = y[i] - r[i]
        if P_y_max < y[i] + r[i]: P_y_max = y[i] + r[i]
    return P_x_min, P_x_max, P_y_min, P_y_max

def N(x, y, r):
    N = np.zeros(netW, netL)
    for i in range(P):
        for ii in range(x[i] - r[i], x[i] + r[i]):
            for jj in range(y[i] - r[i], y[i] + r[i]):
                if (dis(ii, jj, x[i], y[i]) < r[i]): N[jj][ii] += 1

def enumerPos():
    pos = list(product(range(netL), range(netW)))
    return list(combinations(pos, 5))

if __name__ == '__main__':
    pos = enumerPos()
    for p in pos:
        print(p)
        x, y = map(list, zip(*p))
        


