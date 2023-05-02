import time
import numpy as np
import math
from itertools import product, combinations
length = 8 
width = 8
P_r = [3]
netR = 3
l_r = netR / 2
w_r = netR * width / length / 2
P = 5
r = [netR, netR, netR, netR, netR]
recL = math.ceil(length * 2 / netR)
# recW = math.ceil(width / netR)
recW = recL
x_min = 0
y_min = 0

def dis(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def rec(x, y):
    # return math.floor((x - x_min) * 2 / netR), math.floor((y - y_min) * length * 2 / netR / width) 
    return x - x_min, y - y_min

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
        for ii in range(rec(x[i] - r[i]), x[i] + r[i]):
            for jj in range(y[i] - r[i], y[i] + r[i]):
                ii_, jj_ = rec(ii, jj)
                xi_, yi_ = rec(x[i], y[i])
                if (dis(ii_, jj_, xi_, yi_) <= r[i]): N[jj_][ii_] += 1
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
            if N[jj][ii] >= 1:
                sumCover += 1
    return sumCover

if __name__ == '__main__':
    pos = enumerPos()
    w1 = 0.5; w2 = 0.5
    minLoss = 9999999
    for p in pos:
        x, y = map(list, zip(*p))
        print(list(zip(x, y)))
        P_x_min, P_x_max, P_y_min, P_y_max = sprinkler_range(x, y, r)
        x_min = min(P_x_min, 0)
        y_min = min(P_y_min, 0)
        x_max = max(P_x_max, recL)
        y_max = max(P_y_max, recW)

        netL = math.ceil((x_max - x_min) * 2 / netR)
        netW = math.ceil((y_max - y_min) * 2 * length / netR / width)
        N = N_(x, y, r, netW, netL)
        print(N)
        print("\n")
        if (coverRate(N) > recL * recW):
            loss = w1 * wasteArea(x, y, N) + w2 * minM(N)
            if (loss < minLoss):
                minLoss = loss
                print(zip(x, y))
        break
