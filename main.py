#!/usr/bin/env python3
import random
import pandas
import numpy as np
from collections import deque
import matplotlib.pyplot as plt

def normalize (array, dimension):
    size = len(array[0])
    full = []
    # create suitable array
    for i in range(dimension):
        part = [[0] * size]
        full.append(part)
    # do normalization with sampling range
    for j in range(dimension):
        lSide = min(array[j])
        rSide = max(array[j])
        samplRange = rSide - lSide
        # create new array
        array_normalized = [0] * size
        for i in range(size):
            array_normalized[i] = (array[j][i] - lSide) / samplRange
        print("\nDimension №", j + 1, "\nMin = ", lSide)
        print("Max = ", rSide)
        print("Sampling range = ", samplRange)
        full[j] = array_normalized
    return full

def euclidean (p1,p2,dimension):
    euclid = 0
    for i in range (dimension):
        dif = pow((p1[i] - p2[i]),2)
        euclid += dif
    euclid = pow(euclid,0.5)
    return euclid

def longInWidth (longForm, dimension):
    # this function change [x1,x2,..],[y1,y2,..] into [x1,y1],[x2,y2],..
    widthForm = []
    size = len(longForm[0])
    for i in range(size):
        part = [0] * dimension
        widthForm.append(part)
        for j in range (dimension):
            widthForm[i][j] = longForm[j][i]
    return widthForm

def getNumber (objNumber,default=1):
    if  (default):
        return 2
    else:
        print('\nEnter the number of clusters (between 1 and number of objects):')
        n = int(input())
        while (( n <= 1 ) or ( n > objNumber )):
            print('The value does not fit. Enter the number of clusters one more time, please:')
            n = int(input())
        return n

def getFuzzifier(default=1):
    if  (default):
        return 2
    else:
        print('\nEnter the fuzzifier (more than 1):')
        n = float(input())
        while ( n <= 1 ):
            print('The value does not fit. Enter the fuzzifier one more time, please:')
            n = float(input())
        return n

def show2DClusters(center,data):
    size = len(data)
    centerAmount = len(center)
    colors = deque(['#00FF00', '#0000FF', '#FF00FF', '#FF0000', '#FF4500', '#808080', '#FFFF00'])
    common = '#000000'
    circles = []
    for i in range (centerAmount):
        curColor = colors.popleft()
        newCircle = plt.Circle((center[i][0], center[i][1]), .3, color = curColor, alpha = 0.5,)
        circles.append(newCircle)
    for k in range(centerAmount):
        plt.gcf().gca().add_artist(circles[k])
    x1 = np.zeros((1, size))
    y1 = np.zeros((1, size))
    for j in range(size):
        x1[0][j] = data[j][0]
        y1[0][j] = data[j][1]
    plt.scatter(x1, y1, marker='o', c = common)
    plt.show()

#---------------Data preparation---------------

df = pandas.read_excel ("dataFile1.xls", sep=';')
data = [df['f1'], df['f2']]
dimension = len(data)
data = longInWidth (normalize (data, dimension),2)
dataSize = len(data)
dimension = len(data[0])

#---------------Setting of initial values---------------

print('\nInitialization of the C-mean clustering method...')
# 1) number of clusters
J = getNumber(dataSize,0)
# 2) initial membership function
mf = []
for a in range (dataSize):
    part = [0]*J
    mf.append(part)
for b in range (dataSize):
    for c in range (J):
        mf[b][c] = random.random()
# 3) fuzzifier (level of fuzziness)
m = getFuzzifier(0)
# 4) initial centres
initialCentres = random.sample(range(0, dataSize), J)
print("Numbers of random objects:", initialCentres,'\n')
centres = []
for d in range (J):
    part = [0]*dimension
    centres.append(part)
for e in range (J):
    for f in range (dimension):
        cur = initialCentres[e]
        centres[e][f] = data [cur][f]
for g in range (J):
   print('Initial centre №',g+1)
   for h in range (dimension):
       print ('Dimension №',h+1,':',centres[g][h])
   print('\n')
iteration = 1
maxIteration = 20
EPSILON = 4
fuzError = 100

#---------------Main loop of computation ---------------

print('Starting C-mean main loop...\n')
while( (fuzError > EPSILON  ) and (iteration <= maxIteration) ):
    print('ITERATION №',iteration,'\n')
    # 1) calculate new centres of clusters
    for a in range (J):
        for b in range (dimension):
            part1 = 0
            part2 = 0
            for c in range(dataSize):
                fuzzyWeight = pow (mf[c][a],m)
                part1 += fuzzyWeight * data [c][b]
                part2 += fuzzyWeight
            centres[a][b] = part1/part2
    for g in range (J):
       print('New centre №',g+1)
       for h in range (dimension):
           print ('Dimension №',h+1,':',centres[g][h])
       print('\n')
    # 2) calculate new membership function values
    for a in range (J):
        for b in range (dataSize):
            part1 = 1 / pow( (euclidean (data[b],centres[a],dimension)), 2/(m-1) )
            part2 = 0
            for c in range (J):
                part2 += 1 / pow( (euclidean (data[b],centres[c],dimension)), 2/(m-1) )
            mf[b][a] = part1/part2
    # 3) compute the value of the fuzzy error criterion
    fuzError = 0
    for a in range (J):
        for b in range (dataSize):
            fuzzyWeight = pow(mf[b][a], m)
            part = euclidean(data[b], centres[a],dimension)
            fuzError += fuzzyWeight * part
    print('Criterion value:',fuzError)
    iteration += 1
if (dimension == 2):
    show2DClusters(centres,data)
