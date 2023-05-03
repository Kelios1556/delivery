import numpy as np
import math

rad = 80 # real radius(m) * 10
sprR = 30
P = 4
x_min = -rad
x_max = rad
y_min = -rad
y_max = rad

def proj(i, j):
    return i - x_min, j - y_min

def dist(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def area():
    net = 0
    for i in range(-rad, rad):
        for j in range(-rad, rad):
            if (dist(i, j, 0, 0) <= rad): net += 1
    return net

def sprPos(dis):
    x, y = [0] * P, [0] * P
    theta = 2 * math.pi / P
    for i in range(P):
        x[i] = round(dis * math.cos(theta * i), 5)
        y[i] = round(dis * math.sin(theta * i), 5)
    return x, y
        
def sprinkler_range(x, y):
    P_x_min = math.floor(x[0] - sprR)
    P_x_max = math.ceil(x[0] + sprR)
    P_y_min = math.floor(y[0] - sprR)
    P_y_max = math.ceil(y[0] + sprR)
    for i in range(1, P):
        if P_x_min > math.floor(x[i] - sprR): P_x_min = math.floor(x[i] - sprR) 
        if P_x_max < math.ceil(x[i] + sprR): P_x_max = math.ceil(x[i] + sprR)
        if P_y_min > math.floor(y[i] - sprR): P_y_min = math.floor(y[i] - sprR)
        if P_y_max < math.ceil(y[i] + sprR): P_y_max = math.ceil(y[i] + sprR)
    return P_x_min, P_x_max, P_y_min, P_y_max

def N_(x, y): # N[y][x]
    l = x_max - x_min; w = y_max - y_min
    N = np.zeros((w + 1, l + 1), dtype=int)
    for p in range(P):
        for i in range(math.floor(x[p] - sprR), math.ceil(x[p] + sprR)):
            for j in range(math.floor(y[p] - sprR), math.ceil(y[p] + sprR)):
                ii, jj = proj(i, j)
                if dist(i, j, x[p], y[p]) <= sprR: N[jj][ii] += 1
    return N.tolist()

def wasteArea(N):
    result = 0
    for i in range(x_min, x_max):
        for j in range(y_min, y_max):
            ii, jj = proj(i, j)
            if (dist(i, j, 0, 0) > rad) and (N[jj][ii] >= 1):
                result += N[jj][ii]
    return result

def repeatRate(N):
    repeat = 0
    for i in range(-rad, rad):
        for j in range(-rad, rad):
            ii, jj = proj(i, j)
            if (dist(i, j, 0, 0) <= rad) and (N[jj][ii] > 1):
                repeat += N[jj][ii] - 1
    return repeat

def coverRate(N):
    cover = 0
    for i in range(-rad, rad):
        for j in range(-rad, rad):
            ii, jj = proj(i, j)
            if N[jj][ii] >= 1: cover += 1
    return cover

def optPos(w1, w2, w3):
    global x_min, y_min, x_max, y_max
    minLoss = 9999999999
    cordinate = []
    for dis in range(sprR, rad - sprR):
        x, y = sprPos(dis)
        P_x_min, P_x_max, P_y_min, P_y_max = sprinkler_range(x, y)
        x_min = min(x_min, P_x_min)
        x_max = max(x_max, P_x_max)
        y_min = min(y_min, P_y_min)
        y_max = max(y_max, P_y_max)
        N = N_(x, y)

        loss = w1 * wasteArea(N) + w2 * repeatRate(N) + w3 * (area() - coverRate(N))
        if loss < minLoss:
            minLoss = loss
            cordinate = list(zip(x, y))
    return minLoss, cordinate

if __name__ == '__main__':
    w1 = 0.3; w2 = 0.3; w3 = 0.4
    for w1 in np.arange(0.3, 0.55, 0.05):
        for w2 in np.arange(0.3, 0.05, -0.05):
            w3 = 1 - round(w1, 2) - round(w2, 2)
            minLoss, cor = optPos(round(w1, 2), round(w2, 2), round(w3, 2))
            print("w1, w2, w3 = ", round(w1, 2), round(w2, 2), round(w3, 2))
            print(minLoss, cor)
            print("\n")

