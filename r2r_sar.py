



# import time
# import r2r_adc as adc
# import adc_plot as plot
#
# DYNAMIC_RANGE = 3.3
# DURATION = 5.0
# COMPARE_TIME = 0.0001  # чтобы гистограмма попадала в 0..0.06
#
# r2r = adc.R2R_ADC(DYNAMIC_RANGE, compare_time=COMPARE_TIME)
#
# vols = []
# ts = []
#
# try:
#     t0 = time.perf_counter()
#     while (time.perf_counter() - t0) < DURATION:
#         vols.append(r2r.get_sar_voltage())
#         ts.append(time.perf_counter() - t0)
#
#     plot.plot_voltage_vs_time(ts, vols, DYNAMIC_RANGE * 1.1)
#     plot.plot_sampling_period_hist(ts)
#
# finally:
#     r2r.deinit()





import time
import r2r_adc as adc
import adc_plot as plot

DYNAMIC_RANGE = 3.3
DURATION = 5.0
COMPARE_TIME = 0.0001  # чтобы гистограмма попадала в 0..0.06

if __name__ == "__main__":
    r2r = adc.R2R_ADC(DYNAMIC_RANGE, compare_time=COMPARE_TIME)

    vols = []
    ts = []

    try:
        t0 = time.perf_counter()
        while (time.perf_counter() - t0) < DURATION:
            vols.append(r2r.get_sar_voltage())
            ts.append(time.perf_counter() - t0)

        plot.plot_voltage_vs_time(ts, vols, DYNAMIC_RANGE * 1.1)
        plot.plot_sampling_period_hist(ts)

    finally:
        r2r.deinit()
