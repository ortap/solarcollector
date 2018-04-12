import sys

# Edit directory path to point to Adafruit_ADS1x15 directory
sys.path.insert(0, '/home/pi/Documents/solarcollector/Adafruit_Python_ADS1x15/Adafruit_ADS1x15')


import Adafruit_ADS1x15
from thermistor import solarthermistor



#Start Connection to Thermocouple ADC
adc1_conn = Adafruit_ADS1x15.ADS1115()

adc1 = solarthermistor.thermistorDataCollector(adc1_conn)
while True:
    #adc1 = solarthermistor.thermistorDataCollector(adc1_conn)
    print(adc1.get_data())
    