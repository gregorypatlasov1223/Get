import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Инициализация АЦП на основе R-2R лестницы.
        dynamic_range: максимальное напряжение (В), соответствующее числу 255
        compare_time: время ожидания после установки числа на ЦАП (с)
        verbose: если True, выводить отладочную информацию
        """
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose

        # Пины для 8 бит (GPIO в режиме BCM)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21  # пин компаратора

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        """Освобождение ресурсов GPIO."""
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        """Устанавливает на выходах двоичное представление числа (0-255)."""
        bits = [int(b) for b in bin(number)[2:].zfill(8)]
        if self.verbose:
            print(f"Число на ЦАП: {number}, биты: {bits}")
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        """Последовательный перебор (метод последовательного счёта)."""
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"Найдено значение: {value}")
                return value
        # Если ничего не нашли (напряжение выше предела) – возвращаем 255
        return 255

    def get_sc_voltage(self):
        """Возвращает напряжение, измеренное методом последовательного счёта."""
        value = self.sequential_counting_adc()
        voltage = (value / 255.0) * self.dynamic_range
        if self.verbose:
            print(f"Напряжение: {voltage:.3f} В")
        return voltage

    def successive_approximation_adc(self):
        """Более быстрый метод – последовательное приближение."""
        left, right = 0, 256
        while right - left > 1:
            mid = (left + right) // 2
            self.number_to_dac(mid)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                right = mid
            else:
                left = mid
        return left

    def get_sar_voltage(self):
        """Возвращает напряжение, измеренное методом последовательного приближения."""
        value = self.successive_approximation_adc()
        return (value / 255.0) * self.dynamic_range


if __name__ == "__main__":
    # Пример использования (если файл запущен напрямую)
    try:
        adc = R2R_ADC(dynamic_range=3.3, compare_time=0.001, verbose=True)
        while True:
            v = adc.get_sar_voltage()
            print(f"Текущее напряжение: {v:.3f} В")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Программа остановлена пользователем")
    finally:
        adc.deinit()
