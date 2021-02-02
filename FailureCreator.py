#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Environment simulation"

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import matplotlib.pyplot as plt
import numpy as np
import random
from math import *



class CreateFailureMonitor():

    def __init__(self, age_battery, age_motor, scale_battery, shape_battery, scale_motor, shape_motor):
        
        self.connection_string = '127.0.0.1:14551'
        self.age_battery = age_battery*60
        self.age_motor = age_motor*60

        self.alpha_battery = scale_battery#100
        self.beta_battery = shape_battery#12

        self.alpha_motor = scale_motor#120
        self.beta_motor = shape_motor#15


        self.res_battery = int(random.weibullvariate(self.alpha_battery, self.beta_battery)*60)
        self.res_motor = int(random.weibullvariate(self.alpha_motor, self.beta_motor)*60)

    def connect(self):
        print('Process2: Environment connecting to vehicle on: %s' %self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)

    def wait_arm(self):
        while not self.vehicle.armed:
            print("Process2: Waiting for arming...")
            time.sleep(0.2)

    def run(self):
        t1 =  self.age_battery
        t2 =  self.age_motor
        self.wait_arm()
        print(self.res_battery)
        
        print(self.res_motor)

        while t1 != self.res_battery and t2 != self.res_motor and int(self.vehicle.battery.level) != 0:
            time.sleep(0.2)
            t1 = t1 + 1
            t2 = t2 + 1
            print(t2)

        if t1 == self.res_battery:
            #self.vehicle.parameters['SIM_BATT_VOLTAGE'] = 0
            self.vehicle.mode = VehicleMode("RTL")
            time.sleep(2)
            print("Process2: Battery failure")

        if t2 == self.res_motor:
            self.vehicle.mode = VehicleMode("RTL")
            time.sleep(2)
            print("Process2: Motor failure")

        if int(self.vehicle.battery.level) == 0:

            #self.vehicle.mode = VehicleMode("RTL")
            self.vehicle.mode = VehicleMode("RTL")
            time.sleep(2)
            print("Process2: Out of Power")
            #print(self.vehicle.mode)




if __name__ == "__main__":
    #Connected
    # 通过本地端口，使用UDP连接到SITL模拟器
    #connection_string = '127.0.0.1:14550'
    connection_string = raw_input("Please enter connection port:\n")
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)


    age_battery = int(input("Please enter current using age(hours) of battery:"))*60
    age_motor = int(input("Please enter current using age(hours) of motor:"))*60

    monitor = CreateFailureMonitor(connection_string, age_battery, age_motor)
    monitor.connect()
    monitor.run()
