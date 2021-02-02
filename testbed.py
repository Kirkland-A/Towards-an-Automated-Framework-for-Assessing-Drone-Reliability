import os
import subprocess
import signal
import multiprocessing as mp
import time

import argparse

from FailureCreator import CreateFailureMonitor
from monitor import Monitor
from experiment import Experiment
from analyse import Analyse

def parseCommandLineArguments():
    parser = argparse.ArgumentParser(description='Process some integers.')

    #parser.add_argument('--failureConnectionString', type=str, help='ip connection to failure monitor')
    #parser.add_argument('--monitorConnectionString', type=str, help='ip connection to montior')
    #parser.add_argument('--experimentConnectionString', type=str, help='ip connection to experiment')

    parser.add_argument('--scale_battery', type=float, help='Scale parameter of battery Weibull distribution')
    parser.add_argument('--shape_battery', type=float, help='Shape parameter of battery Weibull distribution')
    parser.add_argument('--scale_motor', type=float, help='Scale parameter of Motor Weibull distribution')
    parser.add_argument('--shape_motor', type=float, help='Shape parameter of Motor Weibull distribution')

    parser.add_argument('--batteryage', type=float, help='Minutes that the battery been used')
    parser.add_argument('--motorage', type=float, help='Minutes that the motor been used')

    parser.add_argument('--desiredvoltage', type=int, help='Current voltage of battery')
    parser.add_argument('--missionfilename', type=str)

    parser.add_argument('--iterations', '-i', type = int)

    args = parser.parse_args()
    return args

def runOneFailureMonitor(args):
    ageb, agem, scb, shb, scm, shm = args
    monitor = CreateFailureMonitor(ageb, agem, scb, shb, scm, shm)
    monitor.connect()
    monitor.run()

def runOneDroneMonitor(args):
    iterations = args
    monitor = Monitor(iterations)
    monitor.run()

def runOneExperiment(args):
    desiredvol, filename = args
    experiment = Experiment(desiredvol, filename)
    experiment.connect()
    experiment.run()

def runOnce(ageb, agem, scb, shb, scm, shm, desiredvol, filename):
    

    commandlist = ['sim_vehicle.py', '--console', '-vArduCopter', '--out=127.0.0.1:14552']
    p = subprocess.Popen(commandlist)
    processpid = p.pid
    #time.sleep(2)

    myargs2 = (ageb, agem, scb, shb, scm, shm)
    failureMonitorProcess = mp.Process(target=runOneFailureMonitor, args=(myargs2,))
    failureMonitorProcess.start()
    #processpid = failureMonitorProcess.pid

    myargs3 = (desiredvol, filename)
    experimentProcess = mp.Process(target=runOneExperiment, args=(myargs3,))
    experimentProcess.start()

    failureMonitorProcess.join()
    experimentProcess.join()
    # on finish
    
    os.kill(processpid, signal.SIGINT)
    time.sleep(2)



def run(ageb, agem, scb, shb, scm, shm, desiredvol, filename, iterations):

    myargs1 = (iterations)
    droneMonitorProcess  = mp.Process(target=runOneDroneMonitor, args=(myargs1,))
    droneMonitorProcess.start()

    for i in range(iterations):
        runOnce(ageb, agem, scb, shb, scm, shm, desiredvol, filename)




if __name__=='__main__':
    args = parseCommandLineArguments()
    run(args.batteryage, args.motorage, args.scale_battery, args.shape_battery, args.scale_motor, args.shape_motor, args.desiredvoltage, args.missionfilename,iterations=args.iterations)
    time.sleep(5)
    analysis = Analyse()
    analysis.plot()
    #python testbed.py --batteryage 90 --motorage 100 --scale_battery 93 --shape_battery 7 --scale_motor 105 --shape_motor 25 --desiredvoltage 15 --missionfilename 'mymission3.txt' -i 500
