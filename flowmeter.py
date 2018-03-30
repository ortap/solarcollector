# -*- coding: utf-8 -*-
"""
Flow Sensor Equipment Details
Pulse frequency (Hz) / 7.5 = flow rate in L/min.

Features:

Model: YF-S201
Sensor Type: Hall effect
Working Voltage: 5 to 18V DC (min tested working voltage 4.5V)
Max current draw: 15mA @ 5V
Output Type: 5V TTL
Working Flow Rate: 1 to 30 Liters/Minute
Working Temperature range: -25 to +80℃
Working Humidity Range: 35%-80% RH
Accuracy: ±10%
Maximum water pressure: 2.0 MPa
Output duty cycle: 50% +-10%
Output rise time: 0.04us
Output fall time: 0.18us
Flow rate pulse characteristics: Frequency (Hz) = 7.5 * Flow rate (L/min)
Pulses per Liter: 450
Durability: minimum 300,000 cycles
Cable length: 15cm
1/2" nominal pipe connections, 0.78" outer diameter, 1/2" of thread
Size: 2.5" x 1.4" x 1.4"
Connection details:

Red wire : +5V
Black wire : GND
Yellow wire : PWM output.


@author: shail
Python 3.6.3 program for flow meter
"""
import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)

inpt = 11

GPIO.setup(inpt,GPIO.IN)

rate_cnt = 0
tot_cnt = 0
minutes = 0
constant = 0.10
time_new = 0.0

# User instruction
print('Water Flow - Approximate')
print('Control c to exit')

while True:
    time_new = time.time() + 60
    rate_cnt = 0
    while time.time() <= time_new:
        if GPIO.input(inpt)!= 0:
            rate_cnt += 1
            tot_cnt += 1
        try:
           print(GPIO.input(inpt), end='')
        except KeyboardInterrupt:
           print('\nCTRL C - Exiting nicely')
           GPIO.cleanup()
           sys.exit()
    minutes += 1
    print('\nLiters / min',round(rate_cnt * constant,4))
    print('Total liters', round(tot_cnt * constant,4))
    print('Time (min & clock) ', minutes, '\t', time.asctime(time.localtime()))

GPIO.cleanup()
print('Done')]import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BOARD)

          
