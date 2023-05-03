import math
import numpy as np

m_a = 50
m_b= 135 
eta = 0.9
sprR = 4
S = math.pi * (sprR**2)
Q = 0.1

E = 0.1
P = 4
cor = [(3, 2), (3, 3), (8, 2), (8, 3)]
x_min, y_min = -1, -2
sprNetR = 4
recL, recW = 12, 6
N = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
     [0, 0, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 0, 0], 
     [0, 1, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 1, 0], 
     [0, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 0], 
     [1, 2, 2, 2, 2, 3, 4, 4, 2, 2, 2, 2, 2, 0], 
     [1, 2, 2, 2, 2, 3, 4, 4, 2, 2, 2, 2, 2, 0], 
     [0, 2, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 0], 
     [0, 1, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 1, 0], 
     [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], 
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def quota():
    if 2 * m_a < m_b: # intersect
        m = (2 * m_a + m_b) / 2
    else:
        m = (a + b) / 2

    return m * S / eta  / Q

def rec(i, j):
    return i - x_min, j - x_min

def dis(x_1, y_1, x_2, y_2):
    return math.sqrt((x_1 - x_2)**2 + (y_1 - y_2)**2)

def wetRateDetectArea():
    x, y = map(list, zip(*cor))
    measureArea = np.zeros((P, 2, 2), dtype=int)
    for i in range(P):
        flag1, flag2 = False, False
        for ii in range(math.floor(x[i] - sprNetR), math.ceil(x[i] + sprNetR)):
            for jj in range(math.floor(y[i] - sprNetR), math.ceil(y[i] + sprNetR)):
                ii_, jj_ = rec(ii, jj)
                if (dis(ii, jj, x[i], y[i]) <= sprNetR): 
                    if (flag1 == False and N[jj_][ii_] == 1): 
                        measureArea[i][0] = [ii_, jj_]
                        flag1 = True
                    if (flag2 == False and N[jj_][ii_] == 2):
                        measureArea[i][1] = [ii_, jj_]
                        flag2 = True
                if flag1 and flag2:
                    break
            if flag1 and flag2:
                break
    return measureArea

if __name__ == '__main__':
    print(wetRateDetectArea())




