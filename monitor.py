#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division 
import numpy as np
import matplotlib.pyplot as plt
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from math import *
import os
import subprocess
import signal
import pandas as pd

# connection_string = '127.0.0.1:14550'
# print('Connecting to vehicle on: %s' % connection_string)
# connect函数将会返回一个Vehicle类型的对象，即此处的vehicle
# 即可认为是无人机的主体，通过vehicle对象，我们可以直接控制无人机


class Monitor(object):

    def __init__(self, iterations):
        self.connection_string = '127.0.0.1:14550'
        self.iterations = iterations
        self.data = []

    def connect(self):
        print('Process3: Monitor connecting to vehicle on: %s' %self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)

        #Checking arm state
    def checkarming(self):
        print('Process3: checking state...')
        while not self.vehicle.armed:
            print("Process3: Waiting for arming...")
            time.sleep(0.2)

    def savetofile(self, filename):
        #saves self.data to filename using python pickle or csv or whatever
        pass

    def run(self):
        #Start Arudiplot

        for i in range(self.iterations):
            self.connect()
            self.checkarming()
            start_time = time.time()
            print("Process3: Right")
            
            while str(self.vehicle.mode) != 'VehicleMode:RTL':
                print("Process3: Monitoring...")
                time.sleep(0.2)
            if str(self.vehicle.mode) == 'VehicleMode:RTL':
                print("Process3: Failure occurred")
                timetaken = time.time() - start_time
                t = round((timetaken)*5-2)
                t_minutes = round(t/60, 1)
                self.data.append(t_minutes)
                df = pd.DataFrame(self.data)
                df.to_excel('test.xlsx')
            time.sleep(4)


        print(self.data)
        df = pd.DataFrame(self.data)
        df.to_excel('test.xlsx')
        print("Save to excel")

