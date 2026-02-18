import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial=0)
        # if self.verbose:
        #     print(f"R2R_DAC инициализирован: пины {self.gpio_bits}, диапазон {self.dynamic_range} В")

    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
        # if self.verbose:
        #     print("R2R_DAC деинициализирован")

    def set_number(self, number):
        if number < 0 or number > 255:
            print(f"Ошибка: число {number} вне диапазона 0-255. Устанавливается 0.")
            number = 0

        for i, pin in enumerate(self.gpio_bits):
            state = (number >> i) & 1
            GPIO.output(pin, state)

        # if self.verbose:
        #     print(f"Установлено число {number} (0x{number:02X}) на ЦАП")

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение {voltage:.3f} В выходит за диапазон 0.00 - {self.dynamic_range:.2f} В. Устанавливается 0 В.")
            number = 0
        else:
            number = int(voltage / self.dynamic_range * 255)

        self.set_number(number)

        # if self.verbose:
        #     actual_voltage = number * self.dynamic_range / 255
        #     print(f"Запрошено {voltage:.3f} В -> число {number} -> фактическое напряжение ~{actual_voltage:.3f} В")


if name == "__main__":
    try:
        # Создаём объект ЦАП с пинами из задания (BCM нумерация)
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, verbose=True)

        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()
