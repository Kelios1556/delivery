import time
import numpy as np
import math
from itertools import product, combinations
length = 12 
width = 6
netRatio = 3
# l_r = sprR / netRatio
# w_r = sprR * width / length / netRatio
netR = 1
sprR = 4
rr = math.ceil(sprR / netR)
P = 4
r = [rr, rr, rr, rr]
recL = math.ceil(length / netR)
recW = math.ceil(width / netR)
x_min = 0
y_min = 0

def dis(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def rec(x, y):
    # return math.floor((x - x_min) * netRatio / sprR), math.floor((y - y_min) * length * netRatio / sprR / width) 
    return x - x_min, y - y_min

def recFromPos(x, y):
    return math.floor((x - x_min) / netR), math.floor((y - y_min) / netR) 

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

def N_(x, y, r, netW, netL): # N[y][x]
    N = np.zeros((netW + 1, netL + 1), dtype=int)
    for i in range(P):
        iirb, jjrb = rec(x[i] - r[i], y[i] - r[i])
        iiru, jjru = rec(x[i] + r[i], y[i] + r[i])
        xi_, yi_ = rec(x[i], y[i])
        for ii in range(iirb, iiru):
            for jj in range(jjrb, jjru):
                if (dis(ii, jj, xi_, yi_) <= rr): N[jj][ii] += 1
    return N.tolist()

def enumerPos():
    pos = list(product(range(recL), range(recW)))
    return list(combinations(pos, P))

def wasteArea(x, y, N):
    result = 0
    for i in range(P_x_min, 0):
        for j in range(P_y_min, P_y_max):
            ii, jj = rec(i, j)
            result += N[jj][ii]
    for i in range(recL, P_x_max + 1):
        for j in range(P_y_min, P_y_max):
            ii, jj = rec(i, j)
            result += N[jj][ii]
    for i in range(0, recL):
        for j in range(P_y_min, 0):
            ii, jj = rec(i, j)
            result += N[jj][ii]
    for i in range(0, recL):
        for j in range(recW, P_y_max):
            ii, jj = rec(i, j)
            result += N[jj][ii]
    return result

def minM(N):
    sumN = 0
    for i in range(recL):
        for j in range(recW):
            ii, jj = rec(i, j)
            sumN += N[jj][ii]
    meanN = sumN / (recL * recW)
    sumV = 0
    for i in range(recL):
        for j in range(recW):
            ii, jj = rec(i, j)
            sumV += (N[jj][ii] - meanN)**2
    return math.sqrt(sumV)

def coverRate(N):
    sumCover = 0
    for i in range(recL):
        for j in range(recW):
            ii, jj = rec(i, j)
            # print(ii, jj)
            # print("\n")
            if N[jj][ii] >= 1:
                sumCover += 1
    return sumCover

if __name__ == '__main__':
    pos = enumerPos()
    w1 = 0.5; w2 = 0.5
    minLoss = 999999999999
    for p in pos:
        x, y = map(list, zip(*p))
        P_x_min, P_x_max, P_y_min, P_y_max = sprinkler_range(x, y, r)
        x_min = min(P_x_min, 0)
        y_min = min(P_y_min, 0)
        x_max = max(P_x_max, recL)
        y_max = max(P_y_max, recW)

        netL = x_max - x_min
        netW = y_max - y_min
        N = N_(x, y, r, netW, netL)
        if (coverRate(N) >= recL * recW):
            loss = w1 * wasteArea(x, y, N) + w2 * minM(N)
            if (loss < minLoss):
                minLoss = loss
                print(list(zip(x, y)))
