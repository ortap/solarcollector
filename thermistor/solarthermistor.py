
# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time
from  math import pow, log
import Adafruit_ADS1x15


class thermo_datacollector:
#--------------------ADC SETUP-----------------------
# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.


#Raspberry Pi Providing a +5V to the ADC and 5V for the thermocouple voltage divider.
GAIN = 1
bit_to_volt = 4.096/(pow(2,15))  #Conversion factor from bits to voltage - We are only using 15 of the 16 bits of the ADC  because the first bit is a sign bit (two's complement)

#-------------------THERMISTOR SETUP------------------
# NTC Thermistor: 3kOhm, Tolerance 1%. Vishay Part Number: 01C3001FP
#Temp Range: -40 - 150 oC
therm_res = 3*pow(10,3) #Ohms - 3kOhm Thermistor resistance

#Steinhart & hart Coefficients
A = 1.4028*pow(10,-3)
B = 2.3734*pow(10,-4)
C = 9.9257*pow(10,-8)

#Reference Resistor
therm_supplyvoltage = 5 #5V supply voltage accross the thermistor and reference resistor applied
ref_res = 1*pow(10,3)  #Ohms - 1kOhm Reference Resistance used in voltage divider calc

def res_to_temp(R):
	global A,B,C
	T = pow( A + B*log(R) + C*pow(log(R),3), -1) - 273  #Steinhart Equation and conversion from K to degrees C
	if T > 125 or T < -40:
		print('Warning: Thermistor Temperature Reading Out of Bounds!')
	return T


def vol_to_res(ADCvolt):
	global therm_res, ref_res, therm_supplyvoltage
	therm_res = ref_res*(therm_supplyvoltage/ADCvolt -1) #Voltage divider calculation
	#print("Therm_Res: " + str(therm_res))
	return therm_res

def bits_to_temp(rawbit):
	#convert from bits to voltage
	ADCvolt = rawbit*bit_to_volt
	#print("Ref_volt " + str(ADCvolt))
	return res_to_temp(vol_to_res(ADCvolt))

temps = [0]*4
values = [0]*4
# Main loop.
while True:
    for i in range(4):
    	values[i] = adc.read_adc(i, gain=GAIN)
	temps[i]= round(bits_to_temp(values[i]),2)

    print("A0: " + str(temps[0]) + " A1: " + str(temps[1]) + " A2: " + str(temps[2]) + " oC")

    time.sleep(0.5)
