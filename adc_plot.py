



# import matplotlib.pyplot as plt
#
# def plot_voltage_vs_time(time, voltage, max_voltage):
#     plt.figure(figsize=(10, 6))
#     plt.plot(time, voltage)
#     plt.title("График зависимости напряжения от времени (SAR)")
#     plt.xlabel("Время, с")
#     plt.ylabel("Напряжение, В")
#     plt.ylim(0, max_voltage)
#     plt.grid(True)
#     plt.show()
#
# def plot_sampling_period_hist(time):
#     sampling_periods = [time[i+1] - time[i] for i in range(len(time)-1)]
#     sampling_periods = [p for p in sampling_periods if p > 0]
#
#     if not sampling_periods:
#         print("Гистограмма: мало точек (нужно минимум 2 измерения).")
#         return
#
#     plt.figure(figsize=(10, 6))
#     plt.hist(sampling_periods, bins=80, range=(0, 0.06))
#     plt.title("Распределение длительностей измерений (SAR)")
#     plt.xlabel("Период измерения, с")
#     plt.ylabel("Количество измерений")
#     plt.xlim(0, 0.06)
#     plt.grid(True)
#     plt.show()






import matplotlib.pyplot as plt


def plot_voltage_vs_time(time_vals, voltage_vals, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time_vals, voltage_vals, marker="o", linestyle="-", markersize=3)
    plt.title("Зависимость напряжения на входе АЦП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.ylim(0, max_voltage)
    plt.grid(True)
    plt.show()


def plot_sampling_period_hist(time_vals):
    sampling_periods = [time_vals[i + 1] - time_vals[i] for i in range(len(time_vals) - 1)]
    sampling_periods = [p for p in sampling_periods if p > 0]

    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods, bins=30, edgecolor="black")
    plt.title("Распределение длительности измерений")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")
    plt.xlim(0, 0.06)
    plt.grid(True)
    plt.show()
