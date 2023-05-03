import numpy as np
import math
from itertools import product, combinations

length = 12 
width = 6
netR = 1
sprR = 4
P = 4

sprNetR = sprR / netR
recL = math.ceil(length / netR)
recW = math.ceil(width / netR)
x_min = 0; y_min = 0
pos = []

def dis(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def rec(x, y):
    return x - x_min, y - y_min

def recFromPos(x, y):
    return math.floor((x - x_min) / netR), math.floor((y - y_min) / netR) 

def sprinkler_range(x, y):
    P_x_min = math.floor(x[0] - sprNetR)
    P_x_max = math.ceil(x[0] + sprNetR)
    P_y_min = math.floor(y[0] - sprNetR)
    P_y_max = math.ceil(y[0] + sprNetR)
    for i in range(1, P):
        if P_x_min > math.floor(x[i] - sprNetR): P_x_min = math.floor(x[i] - sprNetR) 
        if P_x_max < math.ceil(x[i] + sprNetR): P_x_max = math.ceil(x[i] + sprNetR)
        if P_y_min > math.floor(y[i] - sprNetR): P_y_min = math.floor(y[i] - sprNetR)
        if P_y_max < math.ceil(y[i] + sprNetR): P_y_max = math.ceil(y[i] + sprNetR)
    return P_x_min, P_x_max, P_y_min, P_y_max

def N_(x, y, netW, netL): # N[y][x]
    N = np.zeros((netW + 1, netL + 1), dtype=int)
    for i in range(P):
        iirb, jjrb = rec(math.floor(x[i] - sprNetR), math.floor(y[i] - sprNetR))
        iiru, jjru = rec(math.ceil(x[i] + sprNetR), math.ceil(y[i] + sprNetR))
        xi_, yi_ = rec(x[i], y[i])
        for ii in range(iirb, iiru):
            for jj in range(jjrb, jjru):
                if (dis(ii, jj, xi_, yi_) <= sprNetR): N[jj][ii] += 1
    return N.tolist()

def enumerPos():
    pos = list(product(range(recL), range(recW)))
    return list(combinations(pos, P))

def wasteArea(N, P_x_min, P_x_max, P_y_min, P_y_max):
    result = 0
    for i in range(P_x_min, 0):
        for j in range(P_y_min, P_y_max):
            ii, jj = rec(i, j)
            result += N[jj][ii]
    for i in range(recL, P_x_max):
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

def repeatRate(N):
    repeat = 0
    for i in range(recL):
        for j in range(recW):
            ii, jj = rec(i, j)
            if N[jj][ii] > 1:
                repeat += N[jj][ii] - 1
    return repeat

def coverRate(N):
    sumCover = 0
    for i in range(recL):
        for j in range(recW):
            ii, jj = rec(i, j)
            if N[jj][ii] >= 1:
                sumCover += 1
    return sumCover

def sprPos(w1, w2, w3):
    global x_min, y_min
    minLoss = 999999999999
    cordinate = []
    for p in pos:
        x, y = map(list, zip(*p))
        P_x_min, P_x_max, P_y_min, P_y_max = sprinkler_range(x, y)
        x_min = min(P_x_min, 0)
        y_min = min(P_y_min, 0)
        x_max = max(P_x_max, recL)
        y_max = max(P_y_max, recW)

        netL = x_max - x_min
        netW = y_max - y_min
        N = N_(x, y, netW, netL)

        loss = w1 * wasteArea(N, P_x_min, P_x_max, P_y_min, P_y_max) \
                + w2 * repeatRate(N) \
                + w3 * (recL * recW - coverRate(N))

        if (loss < minLoss):
            minLoss = loss
            cordinate = list(zip(x, y))
    return minLoss, cordinate

if __name__ == '__main__':
    pos = enumerPos()
    w1 = 0.3; w2 = 0.3; w3 = 0.4

    for w1 in np.arange(0.3, 0.55, 0.05):
        for w2 in np.arange(0.3, 0.05, -0.05):
            w3 = 1 - round(w1, 2) - round(w2, 2)
            minLoss, cor = sprPos(round(w1, 2), round(w2, 2), round(w3, 2))
            print("w1, w2, w3 = ", round(w1, 2), round(w2, 2), round(w3, 2))
            print(minLoss, cor)
            print("\n")


