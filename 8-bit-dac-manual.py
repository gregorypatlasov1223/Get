import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO-пины, подключённые к входам R2R-ЦАП (D7..D0 или D0..D7 — зависит от стенда)
dac_bits = [16, 20, 21, 25, 26, 17, 27, 22]

GPIO.setup(dac_bits, GPIO.OUT, initial=GPIO.LOW)

dynamic_range = 3.17  # В (если в задании сказано ~3.3, можно поставить 3.3)

def voltage_to_number(voltage: float) -> int:
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(number: int):
    number = max(0, min(255, int(number)))  # защита от мусора
    bits = [int(b) for b in bin(number)[2:].zfill(8)]
    GPIO.output(dac_bits, bits)
    return bits

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в вольтах: "))
            number = voltage_to_number(voltage)
            bits = number_to_dac(number)
            print("Число на вход ЦАП:", number, "биты:", bits)
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")

finally:
    GPIO.output(dac_bits, GPIO.LOW)
    GPIO.cleanup()
