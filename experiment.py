#!/usr/bin/env python
# -*- coding: utf-8 -*-

"Experiments of drones"

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
import matplotlib.pyplot as plt
import numpy as np
from math import *



#Setting

class Experiment(object):

    def __init__(self, desired_voltage, import_mission_filename):

        self.connection_string = '127.0.0.1:14552'
        self.desired_voltage = desired_voltage
        self.import_mission_filename = import_mission_filename

    def connect(self):
        print('Process1: Connecting to vehicle on: %s' %self.connection_string)
        self.vehicle = connect(self.connection_string, wait_ready=True)

    def check(self):
        # check before flight
        print("Process1: Basic pre-arm checks")
        # vehicle.is_armable: SITL start? GPS fix? 卡曼滤波器?
        # 是否初始化完毕。若以上检查通过，则会返回True
        while not self.vehicle.is_armable:
            print("Process1: Waiting for vehicle to initialise...")
            time.sleep(0.2)

    def checkarming(self):
        while not self.vehicle.armed:
            print("Process1: Waiting for arming...")
            time.sleep(0.2)


    def readmission(self):
        """
        Load a mission from a file into a list. The mission definition is in the Waypoint file
        format (http://qgroundcontrol.org/mavlink/waypoint_protocol#waypoint_file_format).

        This function is used by upload_mission().
        """
        print("\nProcess1: Reading mission from file: %s" %self.import_mission_filename)
        cmds = self.vehicle.commands
        missionlist=[]
        with open(self.import_mission_filename) as f:
            for i, line in enumerate(f):
                if i==0:
                    if not line.startswith('QGC WPL 110'):
                        raise Exception('Process1: File is not supported WP version')
                else:
                    linearray=line.split('\t')
                    ln_index=int(linearray[0])
                    ln_currentwp=int(linearray[1])
                    ln_frame=int(linearray[2])
                    ln_command=int(linearray[3])
                    ln_param1=float(linearray[4])
                    ln_param2=float(linearray[5])
                    ln_param3=float(linearray[6])
                    ln_param4=float(linearray[7])
                    ln_param5=float(linearray[8])
                    ln_param6=float(linearray[9])
                    ln_param7=float(linearray[10])
                    ln_autocontinue=int(linearray[11].strip())
                    cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                    missionlist.append(cmd)
        return missionlist

    def upload_mission(self):
        """
        Upload a mission from a file. 
        """
        #Read mission from file
        missionlist = self.readmission()
    
        print("\nProcess1: Upload mission from a file: %s" %self.import_mission_filename)
        #Clear existing mission from vehicle
        print('Process1: Clear mission')
        cmds = self.vehicle.commands
        cmds.clear()
        #Add new mission to vehicle
        for command in missionlist:
            cmds.add(command)
        print('Process1: Upload mission')
        self.vehicle.commands.upload()

    def run(self):

        self.vehicle.parameters['SIM_SPEEDUP'] = 5
        self.vehicle.parameters['SIM_ENGINE_MUL']  = 1 
        print('Process1: Reset failure')
        self.vehicle.parameters['SIM_BATT_VOLTAGE']  = self.desired_voltage #change the initial voltage
        aTargetAltitude = 60
        self.check()
        
        
        print("Process1: Arming motors")
        # 将无人机的飞行模式切换成"GUIDED"（一般建议在GUIDED模式下控制无人机）
        self.vehicle.mode = VehicleMode("GUIDED")
        # 通过设置vehicle.armed状态变量为True，解锁无人机
        self.vehicle.armed = True

        # 在无人机起飞之前，确认电机已经解锁
        self.checkarming()
        print("Process1: Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude)

        # 在无人机上升到目标高度之前，阻塞程序
        while True:

            print("Process1: Altitude: ", self.vehicle.location.global_relative_frame.alt)
            # 当高度上升到目标高度的0.95倍时，即认为达到了目标高度，退出循环
            # vehicle.location.global_relative_frame.alt为相对于home点的高度
            if str(self.vehicle.mode) == 'VehicleMode:RTL':
                print("Process1: End experiment")
                break 
            if self.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Process1: Reached target altitude")
                break
                # 等待1s
            time.sleep(0.2)

        self.upload_mission()
        print("Process1: Uploaded")
        self.vehicle.mode = VehicleMode("AUTO")

        while True:
            print("Process1: Running ")
            #self.vehicle.groundspeed = 10
            if str(self.vehicle.mode) == 'VehicleMode:RTL':
                print("Process1: End experiment")
                break 
            time.sleep(0.2)

        







