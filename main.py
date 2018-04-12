

import Adafruit_ADS1x15
from thermistor import solarthermistor

#Start Connection to Thermocouple ADC
adc1_conn = Adafruit_ADS1x15.ADS1115()

while True:
    adc1 = solarthermistor.thermistorDataCollector(adc_conn)
    print(adc1.get_data())