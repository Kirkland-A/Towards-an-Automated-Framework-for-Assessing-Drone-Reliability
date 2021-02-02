#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division 
import numpy as np
import matplotlib.pyplot as plt
from reliability.Fitters import Fit_Weibull_Mixture, Fit_Weibull_2P, Fit_Weibull_CR, Fit_Everything, Fit_Weibull_3P
from reliability.Other_functions import histogram, make_right_censored_data
from reliability.Distributions import Lognormal_Distribution, Gamma_Distribution, Weibull_Distribution, Mixture_Model
import time
import math
from math import *
import pandas as pd
from collections import Counter
import scipy.stats as s
import random



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


    def weibc(self, x, sc, sh):

        return 1-exp(-(x / sc) ** sh)

    def weib(self, x, sc, sh):

        return (sh / sc) * (x / sc) ** (sh- 1) * np.exp(-(x / sc) ** sh)

    def weibp(self, x, sc, sh):

        return (sh / sc) * (x / sc) ** (sh- 1)


    def excel_one_line_to_list(self):
        df = pd.read_excel(self.filename, usecols=[1], names=None)  # 读取项目名称列,不要列名
        timelist = df.values.tolist()
        result = []
        for t in timelist:
            result.append(t[0])
        return result

    def delate(self, list1):
        x = max(list1)
        list2 = []
        for i in range(len(list1)):
            if list1[i] != 0 and list1[i] < 9.5:
                list2.append(list1[i])
        return list2

    def plot(self):
        probability = []
        result = []
        battery = []
        motor = []

        timelist = self.excel_one_line_to_list()
        #timelist = [4.5, 7.7, 4.2, 2.2, 9.4, 6.5, 5.4, 6.0, 2.9, 2.9, 1.4, 5.5, 6.3, 0.6, 7.9, 4.8, 2.5, 8.9, 4.5, 0.8, 8.9, 4.9, 7.5, 2.5, 1.6, 6.6, 3.0, 6.8, 3.1, 8.6, 3.1, 4.0, 6.6, 6.2, 0.1, 6.1, 3.7, 4.3, 6.8, 2.8, 4.7, 1.3, 5.6, 3.7, 0.9, 0.8, 1.9, 7.5, 5.7, 7.2, 6.2, 3.3, 0.2, 6.1, 5.8, 4.2, 3.2, 0.4, 1.3, 1.7, 3.5, 1.9, 5.5, 2.8, 7.9, 0.5, 7.9, 5.4, 5.2, 5.4, 8.0, 1.8, 3.7, 3.3, 2.9, 2.3, 2.7, 1.7, 3.5, 5.1, 2.1, 0.3, 6.0, 1.0, 3.4, 1.8, 7.1, 4.1, 6.0, 0.3, 5.2, 4.7, 2.1, 1.7, 2.3, 2.1, 2.0, 7.2, 3.4, 0.6, 7.5, 9.6, 0.7, 2.4, 3.4, 7.0, 6.1, 1.5, 0.7, 5.8, 1.9, 4.3, 2.7, 8.6, 0.0, 1.8, 1.4, 8.0, 8.6, 5.3, 6.8, 2.6, 4.3, 5.2, 4.0, 4.1, 4.0, 4.1, 0.9, 3.2, 4.9, 3.9, 1.8, 3.7, 1.1, 0.5, 8.5, 6.2, 0.6, 5.6, 5.7, 6.0, 1.4, 3.1, 0.0, 2.5, 7.0, 1.1, 0.3, 6.8, 9.6, 1.4, 2.0, 6.6, 3.8, 7.0, 3.1, 3.4, 2.7, 4.0, 2.3, 0.4, 1.4, 8.0, 4.3, 0.6, 9.6, 6.5, 9.3, 1.9, 1.9, 0.7, 3.2, 6.8, 9.6, 7.0, 3.2, 2.4, 7.9, 4.8, 5.5, 1.6, 8.4, 1.6, 8.4, 5.2, 3.5, 0.3, 3.1, 9.0, 3.0, 4.6, 5.1, 2.4, 3.8, 1.1, 2.3, 1.3, 2.9, 3.4, 2.7, 0.7, 0.7, 3.8, 6.1, 8.3, 7.5, 1.3, 3.1, 9.6, 5.0, 4.4, 7.0, 5.0, 3.0, 4.5, 5.6, 7.1, 6.4, 1.1, 5.0, 2.6, 2.3, 4.4, 1.5, 4.4, 2.5, 6.5, 5.9, 1.5, 4.8, 4.3, 0.9, 4.3, 4.5, 5.1, 2.4, 2.4, 0.3, 9.6, 1.9, 3.4, 1.2, 0.8, 9.6, 4.8, 0.9, 0.7, 4.2, 1.5, -0.0, 0.9, 4.8, 0.8, 0.6, 2.5, 2.1, 0.3, 0.7, 0.9, 2.3, 5.8, 3.8, 0.1, 0.9, 2.0, 1.8, 8.4, 1.1, 2.4, 2.2, 7.9, 9.6, 3.1, 0.0, 5.7, 2.6, 1.3, 1.5, 4.5, 5.8, 3.0, 4.7, 8.5, 6.4, 5.0, 9.6, 0.5, 3.8, 4.0, 1.2, 6.7, 0.9, 1.9, 2.6, 3.9, 8.4, 2.2, 0.2, 4.7, 5.7, 7.5, 8.6, 7.3, 9.4, 7.3, 5.1, 7.2, 1.6, 1.6, 1.0, 8.8, 0.1, 5.1, 1.1, 1.4, 6.9, 3.9, 4.6, 6.2, 0.6, 2.2, 1.3, 8.4, 1.3, 0.6, 4.9, 3.7, 1.6, 1.3, 4.0, 4.9, 9.2, 2.0, 2.6, 5.8, 3.9, 4.8, 4.2, 5.5, 4.8, 6.5, 3.3, 0.4, 5.1, 3.3, 1.6, 1.4, 2.8, 0.1, 6.8, 5.7, 1.3, 2.4, 0.8, 3.1, 3.8, 4.0, 3.8, 5.0, 7.0, 7.8, 3.3, 7.9, 5.9, 2.2, 0.0, 4.7, 2.4, 2.8, 4.3, 1.9, 3.2, 2.2, 4.9, 0.1, 0.7, 2.6, 3.6, 4.1, 0.5, 3.0, 3.7, 4.3, 6.0, 8.5, 5.4, 6.0, 0.0, 3.8, 4.9, 2.2, 3.3, 0.1, 7.0, 2.5, 1.5, 6.6, 0.2, 8.8, 5.5, 1.2, 6.7, 5.2, 0.9, 1.8, 1.5, 9.4, 4.8, 0.6, 3.7, 2.5, 1.2, 2.4, 5.2, 0.9, 1.0, 1.7, 0.5, 0.0, 1.8, 1.9, 2.5, 0.3, 4.5, 4.2, 2.2, 0.3, 6.5, 0.1, 2.7, 4.4, 1.9, 0.8, 2.1, 8.5, 5.8, 0.8, 7.5, 0.4, 0.1, 3.2, 2.2, 6.4, 4.9, 2.9, 8.0, 3.5, 0.3, 5.9, 6.3, 5.6, 5.3, 0.4, 8.4, 1.4, 1.2, 0.2, 4.7, 0.9, 4.8, 2.3, 0.3, 7.7, 6.1, 1.7, 7.9, 9.3, 4.0, 1.5, 2.0, 0.4, 7.0, 1.9, 4.6, 2.3, 3.7, 3.8, 2.5, 5.8, 2.1, 6.0, 4.2, 4.4, 2.1, 3.9, 0.1, 3.2, 1.5, 1.3, 3.3, 3.2, 6.1, 3.3, 3.5, 5.8, 5.8, 5.3, 0.7, 3.9, 4.5, 9.2, 0.8, 4.6, 5.8, 0.5, 3.6, 3.8, 0.3, 6.5, 3.4, 7.3, 5.0, 4.9, 5.4, 2.9, 4.0, 0.9, 0.7, 7.6, 2.8, 2.8, 1.4, 3.9, 0.1, 3.5, 6.3, 2.6, 6.7, 0.9, 1.5, 6.2, 0.9, 4.7, 3.5, 3.4, 3.7, 8.7, 3.7, 3.4, 4.3, 6.8, 6.9, 3.2, 6.3, 0.3, 2.4, 1.4, 1.3, 3.0, 3.8, 3.5, 4.5, 1.8, 0.5, 3.0, 1.6, 4.7, 5.0, 2.1, 1.2, 0.3, 5.0, 4.4, 3.0, 1.4, 8.6, 0.8, 1.6, 1.9, 5.9, 4.5, 3.6, 9.6, 5.9, 2.3, 2.5, 5.9, 6.8, 2.0, 6.3, 3.2, 4.3, 2.6, 3.4, 1.1, 8.8, 1.1, 0.8, 0.3, 2.5, 0.8, 5.0, 3.3, 4.2, 4.2, 4.8, 7.6, 1.8, 5.3, 0.8, 3.6, 6.5, 0.1, 7.3, 5.8, 6.0, 0.9, 4.5, 9.6, 2.0, 6.4, 0.4, 2.2, 2.9, 1.8, 2.4, 0.4, 1.8, 3.1, 3.0, 2.1, 6.3, 2.3, 2.3, 0.2, 1.3, 5.9, 6.2, 2.5, 4.5, 6.8, 2.0, 3.4, 8.6, 3.2, 4.8, 2.5, 8.1, 1.5, 5.0, 3.3, 3.3, 0.8, 6.0, 3.2, 7.4, 6.1, 2.3, 5.8, 5.5, 0.3, 3.4, 1.4, 2.5, 6.5, 2.1, 1.2, 3.8, 4.9, 1.2, 1.8, 4.2, 1.7, 7.6, 1.5, 1.3, 3.5, 1.5, 1.5, 1.4, 9.1, 6.7, 2.3, 8.8, 9.6, 0.3, 0.8, 3.9, 2.5, 0.6, 2.7, 5.0, 0.6, 5.6, 7.9, 1.6, 1.8, 3.7, 1.4, 5.0, 3.6, 0.9, 5.8, 5.1, 2.4, 7.0, 3.6, 6.0, 0.8, 0.5, 4.5, 3.0, 5.3, 6.8, 4.9, 3.1, 3.1, 3.4, 6.0, 1.1, 2.4, 3.0, 6.8, 2.0, 0.8, 7.5, 3.0, 0.3, 3.1, 1.6, 5.5, 0.9, 4.3, 0.7, 2.9, 2.8, 4.9, 2.2, 1.7, 4.0, 3.4, 5.7, 9.0, 3.4, 2.4, 0.2, 1.7, 6.2, 8.0, 8.3, 9.6, 0.6, 3.3, 0.7, 3.3, 1.9, 6.5, 5.8, 3.0, 1.1, 3.5, 0.8, 2.8, 3.0, 4.0, 1.3, 8.4, 3.2, 5.3, 1.8, 6.9, 1.3, 0.8, 4.1, 3.5, 2.2, 3.7, 3.9, 0.4, 5.2, 1.3, 0.6, 3.1, 8.2, 0.4, 7.0, 1.9, 2.2, 2.9, 4.5, 2.6, 3.9, 3.9, 5.3, 0.2, 3.0, 5.3, 0.3, 2.2, 4.1, 3.0, 1.3, 2.4, 5.7, 5.0, 0.7, 2.8, 0.8, 5.6, 5.6, 1.4, 1.7, 1.6, 6.8, 4.0, 5.6, 2.3, 1.4, 4.4, 6.4, 3.6, 8.4, 0.5, 0.3, 3.3, 0.2, 3.2, 8.9, 1.9, 0.1, 0.8, 4.3, 7.3, 1.8, 2.8, 4.1, 0.3, 3.2, 2.4, 2.3, 2.4, 1.8, 5.4, 1.3, 5.8, 2.0, 2.6, 6.4, 1.9, 5.8, 3.0, 1.0, 4.6, 2.0, 4.0, 3.5, 8.8, 0.8, 2.9, 5.3, 5.0, 2.0, 1.4, 2.6, 0.3, 0.9, 1.6, 6.6, 0.8, 6.7, 0.6, 1.2, 6.1, 0.8, 7.1, 6.8, 4.5, 3.6, 2.5, 1.5, 1.9, 6.5, 2.2, 0.1, 2.0, 6.0, 0.1, 1.4, 6.0, 3.2, 6.0, 3.9, 1.4, 5.3, 5.5, 6.0, 0.8, 6.5, 3.1, 3.3, 4.8, 0.2, 1.4, 1.9, 2.0, 2.5, 2.3, 3.7, 1.9, 9.1, 1.3, 0.4, 3.3, 4.5, 7.5, 2.8, 4.4, 7.4, 4.5, 2.7, 6.6, 1.0, 1.8, 4.1, 3.4, 1.6, 1.5, 9.6, 0.1, 3.5, 1.4, 1.7, 2.8, 5.8, 1.5, 4.2, 3.0, 8.1, 2.7, 6.5, 4.9, 6.1, 3.5, 5.8, 0.0, 5.8, 3.9, 1.1, 5.6, 8.8, 0.0, 3.8, 0.3, 2.6, 4.8, 5.3, 4.0, 3.2, 2.0, 2.9, 3.6, 2.8, 3.0, 9.0, 2.7, 4.7, 0.7, 4.3, 1.2, 1.0, 0.6, 1.2, 1.9, 5.4, 7.0, 1.9, 5.4, 8.2, 1.9, 0.1, 0.1, 7.0, 1.8, 5.4, 2.0, 4.2, 7.2, 0.8, 8.9, 9.6, 2.7, 0.5, 6.5, 1.7, 5.7, 1.0, 9.6, 4.4, 0.2, 1.4, 1.1, 8.6, 2.9, 2.4, 6.8, 3.0, 3.3, 1.8, 9.6]



        for t in timelist:
            n = self.round5(t)
            result.append(n)
        print(max(result))
        result_new = self.delate(result)
        data = make_right_censored_data(result, threshold=9.499)
        print(data.right_censored)
        #cc = Counter(result_new)
        #print(cc)
        result_new.sort()

        results1 = Fit_Weibull_Mixture(failures=result_new,right_censored=data.right_censored, show_probability_plot=False)
        #results1 = Fit_Weibull_Mixture(failures=result_new, show_probability_plot=False)
        results2 = Fit_Weibull_2P(failures=result_new, right_censored=data.right_censored, show_probability_plot=False)
        #print(results1.loglik)
        #histogram(result_new, white_above=30)

        xvals = np.linspace(0, 10, 1000)
        #results1.distribution.CDF(label='Weibull Mixture (RMSE = 2.24e-03)',xvals=xvals)
        #results2.distribution.CDF(label='Weibull Single (RMSE = 5.93e-03)',xvals=xvals)
        #plt.title('Single Weibull Distribution Fitting(1000 iterations)')
        #plt.legend()

        """
        d1 = Weibull_Distribution(alpha=2.613, beta=1.297)
        d2 = Weibull_Distribution(alpha=6.014, beta=2.618)
        mix1 = Mixture_Model(distributions=[d1, d2], proportions=[0.553, 0.447])
        plot_components = False 
        mix1.PDF(plot_components=plot_components, color='blue', linestyle='--')
        d3 = Weibull_Distribution(alpha=4.2, beta=1.7)
        d4 = Weibull_Distribution(alpha=8.3, beta=3.2)
        mix2 = Mixture_Model(distributions=[d3, d4], proportions=[0.92, 0.08])
        plot_components = False 
        mix2.PDF(plot_components=plot_components, color='red', linestyle='--')
        """

        #result = self.excel_one_line_to_list()
        count = Counter(result_new)
        print(count)
        time = list(count.keys())
        time.sort()
        print(Counter(result))
        number = list(count.values())
        print(number)
        totaliteration = self.returnSum(count)
        #data0 = np.loadtxt(self.filename)
        #print(data0)
        
        p = 0.0
        for i in number:
            p1 = round(float(i/len(timelist)), 3)
            p = p+p1
            #print(p)
            probability.append(p1)
        print(probability)
        
        square=0
        sum1=0
        sum1=0
        www1=list()
        www2=list()
        print(len(time))
        for i in range(0,len(time)):
            #ex = self.weibc(time[i],4.111,1.429)
            ey = self.weibp(time[i],4.111,1.429)
            ex = 0.553*self.weib(time[i],2.613,1.297)+0.447*self.weib(time[i],6.041,2.618)
            ac = probability[i]
            sum1 = sum1+ac
            sum2 = sum2+ex
            sub = abs(ac-ex)
            xx = ey/(1-ex)
            www1.append(sum1)
            www2.append(ex)
            sq = float((ac-ex)**2)
            square = square+sq/ex
        RSE = square
        print(RSE)
        print(max(www1))
   
        plt.title('K-S test')

        plt.xlabel('Experiment Time(Minutes)')
        plt.ylabel('CDF')
        colors = '#000000'
        plt.plot(time, www2, label = "D(x)")
        plt.plot(time, www1, label = "S(x)")

        """
        a = [1.74, 1.65, 1.61, 1.59]
        b = [0.52, 0.43, 0.40, 0.39]
        c = [2.44, 2.23, 2.14, 2.06]
        d = [0.66, 0.54, 0.47, 0.42]
        x = [250, 500, 750, 1000]
        plt.xlabel('iterations')
        plt.ylabel('Error between estimation and input parameters')
        plt.plot(x, a, label = 'Error alpha1')
        plt.plot(x, b, label = 'Error beta1')
        plt.plot(x, c, label = 'Error alpha2')
        plt.plot(x, d, label = 'Error beta2')
        """

        plt.legend()
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

    df = pd.read_excel("test.xlsx", usecols=[1], names=None)  # 读取项目名称列,不要列名
    timelist1 = df.values.tolist()
    timelist2 = [6.2, 0.0, 1.3, 2.9, 1.2, 1.7, 6.8, 1.1, 2.7, 9.5, 6.3, 2.0, 9.6, 4.0, 4.5, 3.2, 4.6, 7.9, 9.6, 9.6, 9.5, 9.6, 5.2, 9.6, 7.6, 6.4, 3.0, 3.1, 1.4, 2.3, 2.1, 6.2, 4.5, 0.4, 3.6, 9.6, 4.6, 9.6, 9.6, 2.4, 0.0, 9.6, 8.8, 5.5, 0.9, 7.5, 9.6, 9.6, 8.7, 9.6, 9.6, 9.6, 6.2, 8.1, 8.6, 9.6, 4.7, 1.4, 9.6, 9.6, 7.4, 2.0, 7.3, 7.7, 2.6, 8.5, 2.4, 4.3, 7.2, 7.9, 0.7, 4.8, 5.2, 8.2, 8.4, 9.6, 1.2, 7.6, 0.9, 2.8, 9.4, 9.1, 7.2, 9.5, 9.6, 4.7, 3.2, 5.3, 5.3, 8.5, 8.0, 9.6, 5.5, 1.9, 9.6, 0.4, 7.7, 9.2, 8.1, 9.6, 0.3, 9.6, 9.6, 9.6, 6.1, 7.9, 7.0, 1.5, 9.5, 2.8, 9.6, 3.3, 7.2, 6.7, 9.6, 9.5, 8.4, 3.2, 9.6, 9.6, 3.9, 2.6, 2.2, 3.9, 9.5, 4.5, 0.8, 9.6, 9.6, 9.4, 9.6, 9.5, 8.6, 7.2, 7.4, 6.2, 4.1, 9.6, 4.4, 5.6, 9.6, 8.7, 5.3, 9.6, 6.3, 5.6, 9.6, 6.2, 9.6, 2.6, 8.7, 7.3, 5.6, 9.6, 6.8, 9.6, 1.0, 8.3, 9.6, 7.0, 1.6, 4.3, 6.2, 4.4, 4.0, 0.9, 2.1, 7.2, 9.6, 7.6, 7.5, 9.6, 5.6, 6.3, 9.6, 9.6, 6.8, 0.9, 5.3, 7.0, 3.9, 1.8, 9.6, 4.8, 8.2, 9.6, 1.6, 5.0, 8.0, 8.6, 8.8, 5.0, 3.4, 7.4, 9.6, 4.6, 9.0, 9.6, 0.1, 9.6, 9.6, 9.6, 9.6, 1.8, 9.6, 5.1, 3.1, 6.8, 9.6, 8.5, 8.8, 0.5, 9.6, 7.3, 5.3, 4.1, 9.6, 7.9, 6.4, 6.3, 9.6, 7.2, 7.8, 9.6, 3.7, 9.6, 9.6, 2.2, 8.8, 9.6, 6.6, 8.6, 3.5, 4.5, 5.3, 6.8, 8.0, 4.0, 0.3, 6.9, 9.6, 8.6, 9.2, 7.1, 9.6, 3.7, 0.2, 0.8, 9.6, 3.4, 9.6, 8.7, 5.9, 7.7, 3.6, 9.0, 6.3, 9.6, 6.4, 9.6, 5.0, 0.5, 4.5, 1.9, 9.6, 9.6, 4.1, 0.8, 5.8, 8.4, 7.3, 9.6, 7.0, 9.5, 9.6, 0.1, 9.0, 6.4, 8.2, 7.3,4.7, 0.3, 3.3, 9.6, 6.7, 7.9, 8.8, 9.6, 9.6, 4.0, 8.8, 3.0, 4.7, 9.6, 9.2, 8.4, 9.4, 9.6, 5.9, 4.3, 5.7, 3.8, 0.8, 3.2, 0.0, 5.4, 7.8, 9.6, 2.5, 9.1, 9.0, 9.5, 9.5, 8.7, 7.8, 9.5, 5.5, 4.6, 0.9, 6.3, 6.5, 9.6, 9.3, 7.9, 9.5, 9.5, 7.5, 0.3, 8.7, 6.6, 9.5, 4.5, 8.7, 2.8, 1.7, 8.9, 2.8, 9.5, 9.5, 7.3, 5.3, 8.2, 9.6, 5.1, 9.6, 2.1, 6.5, 9.6, 5.0, 9.5, 8.4, 3.5, 9.5, 9.3, 4.5, 9.6, 4.8, 9.6, 0.9, 3.6, 9.6, 5.9, 4.2, 5.0, 9.6, 1.0, 3.4, 9.6, 0.3, 6.4, 9.6, 6.2, 6.0, 6.3, 2.2, 6.9, 6.5, 4.8, 9.2, 3.7, 2.0, 3.1, 9.6, 9.1, 9.3, 6.2, 9.5, 0.6, 9.7, 9.6, 9.6, 5.6, 4.5, 3.1, 9.3, 9.5, 6.0, 9.6, 1.2, 7.3, 2.6, 9.6, 6.0, 2.3, 0.3, 3.6, 9.2, 6.2, 8.8, 9.6, 2.4, 9.6, 7.6, 1.8, 4.9, 9.6, 8.2, 2.9, 6.7, 6.7, 3.9, 4.8, 3.4, 6.9, 6.0, 9.6, 9.1, 3.9, 3.4, 2.9, 5.3, 5.3, 4.7, 3.5, 5.3, 9.6, 2.9, 3.4, 3.5, 9.6, 1.3, 9.6, 3.4, 9.6, 4.9, 0.7, 4.7, 5.5, 7.6, 7.1, 7.4, 8.5, 1.9, 4.9, 8.4, 8.7, 2.4, 8.2, 7.3, 9.6, 4.4, 9.1, 9.6, 8.8, 9.0, 3.6, 3.8, 7.7, 9.6, 2.4, 6.3, 1.3, 3.6, 4.0, 9.6, 2.6, 0.9, 7.7, 3.9, 6.5, 7.8, 0.1, 9.6, 8.6, 0.6, 9.6, 4.5, 7.6, 9.6, 9.6, 7.4, 6.0, 6.1, 7.2, 0.0, 6.8, 9.6, 5.1, 3.2, 6.9]
    timelist = timelist1+timelist2
     

    result = []
    probability = []
    for t in timelist:
        n = round5(t)
        result.append(n)
    print(result)
    count = Counter(result)
    print(count)
    time1 = list(count.keys())
    time = list.sort(time1)
    print(time)
    number = list(count.values())
    totaliteration = returnSum(count)

    for i in number:
        p = round(float(i/totaliteration), 3)

        probability.append(p)

    plt.xlabel('Failure time')
    plt.ylabel('Probability')
    plt.scatter(time, probability)
    plt.show()
