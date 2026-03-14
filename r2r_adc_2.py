import RPi.GPIO as GPIO
import time

class R2R_ADC:
    """
    Класс для работы с 8-битным АЦП последовательного счёта на базе ЦАП R-2R и компаратора.
    """
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Конструктор класса.
        :param dynamic_range: динамический диапазон ЦАП в вольтах (измеряется мультиметром)
        :param compare_time: время ожидания после подачи числа на ЦАП для стабилизации компаратора (сек)
        :param verbose: флаг отладочного вывода
        """
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose

        # Пины для 8 бит ЦАП (от старшего к младшему)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # Пин, подключённый к выходу компаратора
        self.comp_gpio = 21

        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        """Сброс ЦАП в 0 и очистка настроек GPIO."""
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        """
        Подаёт 8-битное число (0–255) на параллельный вход ЦАП.
        """
        # Преобразование числа в список битов (старший бит — первый в списке)
        bits = [int(b) for b in bin(number)[2:].zfill(8)]
        if self.verbose:
            print(f"Устанавливаем биты: {bits}")
        GPIO.output(self.bits_gpio, bits)

    def sequential_counting_adc(self):
        """
        Метод последовательного счёта.
        Перебирает значения от 0 до 255, пока напряжение ЦАП не превысит входное.
        Возвращает число, при котором компаратор сработал (выход = 1),
        или 255, если превышение не достигнуто.
        """
        for value in range(256):
            self.number_to_dac(value)
            time.sleep(self.compare_time)  # Ждём, пока компаратор установит выход
            if GPIO.input(self.comp_gpio) == 1:
                if self.verbose:
                    print(f"Компаратор сработал при value = {value}")
                return value
        # Если входное напряжение больше максимального (обычно не происходит)
        return 255

    def get_sc_voltage(self):
        """
        Измеряет входное напряжение с помощью АЦП последовательного счёта.
        Возвращает напряжение в вольтах.
        """
        code = self.sequential_counting_adc()
        voltage = (code / 255) * self.dynamic_range
        if self.verbose:
            print(f"Код АЦП: {code}, напряжение: {voltage:.3f} В")
        return voltage


# Основной охранник
if __name__ == "__main__":
    try:
        # Замените dynamic_range на значение, измеренное вашим мультиметром!
        # В примере используется 3.2 В, но у вас может быть другое.
        adc = R2R_ADC(dynamic_range=3.2, compare_time=0.01, verbose=False)

        while True:
            # Бесконечно измеряем и выводим напряжение
            voltage = adc.get_sc_voltage()
            print(f"Напряжение на потенциометре: {voltage:.3f} В")
            # Небольшая задержка для удобства чтения (необязательно)
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Позволяет выйти из цикла по Ctrl+C
        print("\nИзмерение прервано пользователем")
    finally:
        # Гарантированно освобождаем GPIO
        adc.deinit()
