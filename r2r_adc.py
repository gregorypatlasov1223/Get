# import RPi.GPIO as GPIO
# import time
#
# class R2R_ADC:
#     def __init__(self, drange, comp_time = 0.01, verbose = False):
#         self.comp_time = comp_time
#         self.range = drange
#         self.verbose = verbose
#
#         self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
#         self.comp_gpio = 21
#
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
#         GPIO.setup(self.comp_gpio, GPIO.IN)
#
#     def deinit(self):
#         GPIO.output(self.bits_gpio, 0)
#         GPIO.cleanup()
#
#     def num_2_dac(self, number):
#         GPIO.output(self.bits_gpio, [int(element) for element in bin(number)[2:].zfill(8)])
#
#     def sequential_counting_adc(self):
#         for i in range(256):
#             self.num_2_dac(i)
#             time.sleep(self.comp_time)
#             if GPIO.input(self.comp_gpio) or i == 255:
#                 return i * self.range / 255
#
#     def get_sc_vol(self):
#         res = self.sequential_counting_adc()
#         print(f"Voltage is: {res}\n")
#         return res
#
#     def successive_approximation_adc(self):
#         upper = 256
#         lower = 0
#         while lower < upper - 1:
#             current = (lower + upper) // 2
#             self.num_2_dac(current)
#             time.sleep(self.comp_time)
#             if GPIO.input(self.comp_gpio):
#                 upper = current
#             else:
#                 lower = current
#         return lower
#
#     def indian_bise(self):
#         cmp = 128
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp = 192
#         else:
#             cmp = 64
#
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp += 32
#         else:
#             cmp -= 32
#
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp += 16
#         else:
#             cmp -= 16
#
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp += 8
#         else:
#             cmp -= 8
#
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp += 4
#         else:
#             cmp -= 4
#
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp += 2
#         else:
#             cmp -= 2
#
#         self.num_2_dac(cmp)
#         time.sleep(self.comp_time)
#         if GPIO.input(self.comp_gpio):
#             cmp += 1
#         else:
#             cmp -= 1
#
#         return cmp
#
#     def get_sar_vol(self):
#         res = (self.successive_approximation_adc() / 255.0) * self.range
#         print(f"Voltage is: {res}\n")
#         return res
#
#     def get_indian_vol(self):
#         res = (self.successive_approximation_adc() / 255.0) * self.range
#         print(f"Voltage is: {res}\n")
#         return res
#
#
# if __name__ == "__main__":
#     try:
#         adc = R2R_ADC(3.183)
#
#         while True:
#             #adc.get_sc_vol()
#             #adc.get_sar_vol()
#             adc.get_indian_vol()
#     finally:
#         adc.deinit()



# import RPi.GPIO as GPIO
# import time
# GPIO.setmode(GPIO.BCM)
#
# class R2R_ADC:
#     def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
#         self.dynamic_range = dynamic_range
#         self.verbose = verbose
#         self.compare_time = compare_time
#
#         self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
#         self.comp_gpio = 21
#
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
#         GPIO.setup(self.comp_gpio, GPIO.IN)
#
#     def deinit(self):
#         GPIO.output(self.bits_gpio, 0)
#         GPIO.cleanup()
#
#     def number_to_dac(self, number):
#         bits = [int(element) for element in bin(number)[2:].zfill(8)]
#         #print(f"Число на вход АЦП: {number}, биты: {bits}")
#         GPIO.output(self.bits_gpio, bits)
#
#     def sequential_counting_acd(self):
#         for value in range(256):
#             R2R_ADC.number_to_dac(self, value)
#             time.sleep(self.compare_time)
#             if (GPIO.input(self.comp_gpio)==1):
#                 #print(f"Число на вход АЦП: {value}, напряжение - {voltage}В")
#                 return value
#         #print("Число на выходе АЦП: 256, напряжение - 3.2В")
#         return 255
#
#     def get_sc_voltage(self):
#         value = R2R_ADC.sequential_counting_acd(self)
#         return (value/255)*self.dynamic_range
#
#     def successive_approximation_adc(self):
#         right = 256
#         left = 0
#         value = 0
#         while (right-left>1):
#             value = (right+left)//2
#             R2R_ADC.number_to_dac(self, value)
#             time.sleep(self.compare_time)
#             if (GPIO.input(self.comp_gpio)==1):
#                 right=value
#             else:
#                 left=value
#         return value
#
#     def get_sar_voltage(self):
#         value = R2R_ADC.successive_approximation_adc(self)
#         return (value/255)*self.dynamic_range
#
#
# if __name__ == "__main__":
#     try:
#         adc = R2R_ADC(3.2, 0.1)
#         while True:
#             voltage = adc.get_sar_voltage()
#             print(f"Напряжение: {voltage}")
#     finally:
#         adc.deinit()


import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False,
                 comp_high_when_dac_greater=True):
        self.dynamic_range = float(dynamic_range)
        self.compare_time = float(compare_time)
        self.verbose = bool(verbose)
        self.comp_high_when_dac_greater = bool(comp_high_when_dac_greater)

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.comp_gpio, GPIO.IN)

        # LUT: ускоряем number_to_dac — заранее готовим 256 наборов бит
        self._lut = [[int(b) for b in f"{n:08b}"] for n in range(256)]

    def deinit(self):
        GPIO.output(self.bits_gpio, GPIO.LOW)
        GPIO.cleanup()

    def number_to_dac(self, number: int):
        GPIO.output(self.bits_gpio, self._lut[number & 0xFF])

    def _dac_greater_than_input(self) -> bool:
        comp = GPIO.input(self.comp_gpio)
        return (comp == 1) if self.comp_high_when_dac_greater else (comp == 0)

    # --- SAR "быстрый индусский": только value, 8 явных шагов ---
    def successive_approximation_adc(self) -> int:
        # локальные ссылки — микроприбавка к скорости
        out = self.number_to_dac
        sleep = time.sleep
        gt = self._dac_greater_than_input
        dt = self.compare_time

        # 1) пробуем 128
        value = 128
        out(value)
        sleep(dt)
        if gt():
            value = 0  # откат (без лишнего out)

        # 2) явно: либо 192, либо 64
        #    (если 128 принят -> пробуем 192; иначе пробуем 64)
        if value == 128:
            value = 192
        else:
            value = 64

        out(value)
        sleep(dt)
        if gt():
            value -= 64  # откат к базе (128 или 0), без лишнего out

        # дальше обычные явные шаги: +32, +16, ..., +1
        value += 32
        out(value)
        sleep(dt)
        if gt():
            value -= 32

        value += 16
        out(value)
        sleep(dt)
        if gt():
            value -= 16

        value += 8
        out(value)
        sleep(dt)
        if gt():
            value -= 8

        value += 4
        out(value)
        sleep(dt)
        if gt():
            value -= 4

        value += 2
        out(value)
        sleep(dt)
        if gt():
            value -= 2

        value += 1
        out(value)
        sleep(dt)
        if gt():
            value -= 1

        return value

    def get_sar_voltage(self) -> float:
        return (self.successive_approximation_adc() / 255.0) * self.dynamic_range


if __name__ == "__main__":
    adc = None
    try:
        adc = R2R_ADC(dynamic_range=3.3, compare_time=0.001, verbose=False)
        while True:
            print(f"{adc.get_sar_voltage():.3f} V")
            time.sleep(0.5)
    finally:
        if adc is not None:
            adc.deinit()
