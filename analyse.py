#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division 
import numpy as np
import matplotlib.pyplot as plt
#from reliability.Fitters import Fit_Weibull_Mixture
import time
import math
from math import *
import pandas as pd
from collections import Counter



class Analyse():

    def __init__(self):
        
        self.filename = "test.xlsx"


    def returnSum(self,myDict): 
      
        sum = 0
        for i in myDict: 
            sum = sum + myDict[i] 
      
        return sum

    def round5(self, x):
        if x == 0:
            return 0
        x1 = math.ceil(x)
        x2 = math.floor(x)
        x3 = round((x1+x2)/2,1)
        if x > x3:
            if abs(x3-x)<=abs(x1-x):
                return x3
            if abs(x3-x)>abs(x1-x):
                return x1
        if x <= x3:
            if abs(x3-x)<=abs(x2-x):
                return x3
            if abs(x3-x)>abs(x2-x):
                return x2


    def weib(self, x, sc, sh):

        return (sh / sc) * (x / sc) ** (sh- 1) * np.exp(-(x / sc) ** sh)


    def excel_one_line_to_list(self):
        df = pd.read_excel(self.filename, usecols=[1], names=None)  # 读取项目名称列,不要列名
        timelist = df.values.tolist()
        result = []
        for t in timelist:
            result.append(t[0])
        return result

    def plot(self):
        probability = []

        timelist5 = self.excel_one_line_to_list()
        result = []
        probability = []
        for t in timelist5:
            n = self.round5(t)
            result.append(n)


        #result = self.excel_one_line_to_list()
        count = Counter(result)
        print(count)
        time = list(count.keys())
        number = list(count.values())
        totaliteration = self.returnSum(count)
        #data0 = np.loadtxt(self.filename)
        #print(data0)

        for i in number:
            p = round(float(i/totaliteration), 3)
            probability.append(p)

        plt.xlabel('Failure time')
        plt.ylabel('Probability')
        plt.scatter(time, probability)
        plt.show()
        

if __name__ == '__main__':

    def returnSum(myDict): 
      
        sum = 0
        for i in myDict: 
            sum = sum + myDict[i] 
      
        return sum

    def round5(x):
        if x == 0:
            return 0
        x1 = math.ceil(x)
        x2 = math.floor(x)
        x3 = round((x1+x2)/2,1)
        if x > x3:
            if abs(x3-x)<=abs(x1-x):
                return x3
            if abs(x3-x)>abs(x1-x):
                return x1
        if x <= x3:
            if abs(x3-x)<=abs(x2-x):
                return x3
            if abs(x3-x)>abs(x2-x):
                return x2

    #df = pd.read_excel("test.xlsx", usecols=[1], names=None)  # 读取项目名称列,不要列名
    #timelist = df.values.tolist()
    timelist = [6.2, 0.0, 1.3, 2.9, 1.2, 1.7, 6.8, 1.1, 2.7, 9.5, 6.3, 2.0, 9.6, 4.0, 4.5, 3.2, 4.6, 7.9, 9.6, 9.6, 9.5, 9.6, 5.2, 9.6, 7.6, 6.4, 3.0, 3.1, 1.4, 2.3, 2.1, 6.2, 4.5, 0.4, 3.6, 9.6, 4.6, 9.6, 9.6, 2.4, 0.0, 9.6, 8.8, 5.5, 0.9, 7.5, 9.6, 9.6, 8.7, 9.6, 9.6, 9.6, 6.2, 8.1, 8.6, 9.6, 4.7, 1.4, 9.6, 9.6, 7.4, 2.0, 7.3, 7.7, 2.6, 8.5, 2.4, 4.3, 7.2, 7.9, 0.7, 4.8, 5.2, 8.2, 8.4, 9.6, 1.2, 7.6, 0.9, 2.8, 9.4, 9.1, 7.2, 9.5, 9.6, 4.7, 3.2, 5.3, 5.3, 8.5, 8.0, 9.6, 5.5, 1.9, 9.6, 0.4, 7.7, 9.2, 8.1, 9.6, 0.3, 9.6, 9.6, 9.6, 6.1, 7.9, 7.0, 1.5, 9.5, 2.8, 9.6, 3.3, 7.2, 6.7, 9.6, 9.5, 8.4, 3.2, 9.6, 9.6, 3.9, 2.6, 2.2, 3.9, 9.5, 4.5, 0.8, 9.6, 9.6, 9.4, 9.6, 9.5, 8.6, 7.2, 7.4, 6.2, 4.1, 9.6, 4.4, 5.6, 9.6, 8.7, 5.3, 9.6, 6.3, 5.6, 9.6, 6.2, 9.6, 2.6, 8.7, 7.3, 5.6, 9.6, 6.8, 9.6, 1.0, 8.3, 9.6, 7.0, 1.6, 4.3, 6.2, 4.4, 4.0, 0.9, 2.1, 7.2, 9.6, 7.6, 7.5, 9.6, 5.6, 6.3, 9.6, 9.6, 6.8, 0.9, 5.3, 7.0, 3.9, 1.8, 9.6, 4.8, 8.2, 9.6, 1.6, 5.0, 8.0, 8.6, 8.8, 5.0, 3.4, 7.4, 9.6, 4.6, 9.0, 9.6, 0.1, 9.6, 9.6, 9.6, 9.6, 1.8, 9.6, 5.1, 3.1, 6.8, 9.6, 8.5, 8.8, 0.5, 9.6, 7.3, 5.3, 4.1, 9.6, 7.9, 6.4, 6.3, 9.6, 7.2, 7.8, 9.6, 3.7, 9.6, 9.6, 2.2, 8.8, 9.6, 6.6, 8.6, 3.5, 4.5, 5.3, 6.8, 8.0, 4.0, 0.3, 6.9, 9.6, 8.6, 9.2, 7.1, 9.6, 3.7, 0.2, 0.8, 9.6, 3.4, 9.6, 8.7, 5.9, 7.7, 3.6, 9.0, 6.3, 9.6, 6.4, 9.6, 5.0, 0.5, 4.5, 1.9, 9.6, 9.6, 4.1, 0.8, 5.8, 8.4, 7.3, 9.6, 7.0, 9.5, 9.6, 0.1, 9.0, 6.4, 8.2, 7.3,4.7, 0.3, 3.3, 9.6, 6.7, 7.9, 8.8, 9.6, 9.6, 4.0, 8.8, 3.0, 4.7, 9.6, 9.2, 8.4, 9.4, 9.6, 5.9, 4.3, 5.7, 3.8, 0.8, 3.2, 0.0, 5.4, 7.8, 9.6, 2.5, 9.1, 9.0, 9.5, 9.5, 8.7, 7.8, 9.5, 5.5, 4.6, 0.9, 6.3, 6.5, 9.6, 9.3, 7.9, 9.5, 9.5, 7.5, 0.3, 8.7, 6.6, 9.5, 4.5, 8.7, 2.8, 1.7, 8.9, 2.8, 9.5, 9.5, 7.3, 5.3, 8.2, 9.6, 5.1, 9.6, 2.1, 6.5, 9.6, 5.0, 9.5, 8.4, 3.5, 9.5, 9.3, 4.5, 9.6, 4.8, 9.6, 0.9, 3.6, 9.6, 5.9, 4.2, 5.0, 9.6, 1.0, 3.4, 9.6, 0.3, 6.4, 9.6, 6.2, 6.0, 6.3, 2.2, 6.9, 6.5, 4.8, 9.2, 3.7, 2.0, 3.1, 9.6, 9.1, 9.3, 6.2, 9.5, 0.6, 9.7, 9.6, 9.6, 5.6, 4.5, 3.1, 9.3, 9.5, 6.0, 9.6, 1.2, 7.3, 2.6, 9.6, 6.0, 2.3, 0.3, 3.6, 9.2, 6.2, 8.8, 9.6, 2.4, 9.6, 7.6, 1.8, 4.9, 9.6, 8.2, 2.9, 6.7, 6.7, 3.9, 4.8, 3.4, 6.9, 6.0, 9.6, 9.1, 3.9, 3.4, 2.9, 5.3, 5.3, 4.7, 3.5, 5.3, 9.6, 2.9, 3.4, 3.5, 9.6, 1.3, 9.6, 3.4, 9.6, 4.9, 0.7, 4.7, 5.5, 7.6, 7.1, 7.4, 8.5, 1.9, 4.9, 8.4, 8.7, 2.4, 8.2, 7.3, 9.6, 4.4, 9.1, 9.6, 8.8, 9.0, 3.6, 3.8, 7.7, 9.6, 2.4, 6.3, 1.3, 3.6, 4.0, 9.6, 2.6, 0.9, 7.7, 3.9, 6.5, 7.8, 0.1, 9.6, 8.6, 0.6, 9.6, 4.5, 7.6, 9.6, 9.6, 7.4, 6.0, 6.1, 7.2, 0.0, 6.8, 9.6, 5.1, 3.2, 6.9]
     

    result = []
    probability = []
    for t in timelist:
        n = round5(t)
        result.append(n)
    print(result)
    count = Counter(result)
    print(count)
    time = list(count.keys())
    number = list(count.values())
    totaliteration = returnSum(count)

    for i in number:
        p = round(float(i/totaliteration), 3)

        probability.append(p)

    plt.xlabel('Failure time')
    plt.ylabel('Probability')
    plt.scatter(time, probability)
    plt.show()
