# What does this program do?
from math import pow, log

class thermistorDataCollector:
    def __init__(self, reftothermocoupleADC):
        self.adc = reftothermocoupleADC

    # -------------------- ADC SETUP ----------------------

    # Raspberry Pi Providing +5V to the ADC and 5V for the thermocouple voltage divider.
    GAIN = 1  # If you change the internal gain, then you must change the voltage on the next line. Refer to adafruit documentation
    bit_to_volt = 4.096 / (pow(2, 15))  # Conversion factor from bits to voltage - We are only using 15 of the 16 bits of the ADC  because the first bit is a sign bit (two's complement)

    # ------------------ THERMISTOR SETUP -----------------
    # NTC Thermistor: 3kOhm, Tolerance 1%. Vishay Part Number: 01C3001FP
    # Temp Range: -40 - 150 oC
    therm_res = 3 * pow(10, 3)  # Ohms - 3kOhm Thermistor resistance
    # Steinhart & hart Coefficients
    A = 1.4028 * pow(10, -3)
    B = 2.3734 * pow(10, -4)
    C = 9.9257 * pow(10, -8)

    # Reference Resistor
    therm_supplyvoltage = 5  # 5V supply voltage accross the thermistor and reference resistor applied
    ref_res = 1 * pow(10, 3)  # Ohms - 1kOhm Reference Resistance used in voltage divider calc

    # --------------------- CONVERSION FUNCTIONS -------------------------
    @staticmethod
    def res_to_temp(r):
        global A, B, C
        T = pow(A + B * log(r) + C * pow(log(r), 3), -1) - 273  # Steinhart Equation and conversion from K to degrees C
        if T > 125 or T < -40:
            print('Warning: Thermistor Temperature Reading Out of Bounds!')
        return T

    @staticmethod
    def volt_to_res(ADCvolt):
        global therm_res, ref_res, therm_supplyvoltage
        therm_res = ref_res * (therm_supplyvoltage / ADCvolt - 1)  # Voltage divider calculation
        # print("Therm_Res: " + str(therm_res))
        return therm_res

    def bits_to_temp(rawbit):
        # Convert from bits to voltage using res_to_temp and vol_to_res
        global bit_to_volt
        ADCvolt = rawbit * bit_to_volt
        # print("Ref_volt " + str(ADCvolt))
        return thermistorDataCollector.res_to_temp(thermistorDataCollector.volt_to_res(ADCvolt))

    # Main loop.
    def get_data(self):
        global GAIN
        temps = [0] * 4
        values = [0] * 4
        for i in range(4):
            values[i] = self.adc.read_adc(i, gain=GAIN)
        temps[i] = round(self.bits_to_temp(values[i]), 2)  # Rounds the temperature to the hundreths place
        return temps
