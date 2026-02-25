import mcp4725_driver as mcp4725
import signal_generator as sg
import time

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    mcp = mcp4725.MCP4725(5.11)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        signal = amplitude * sg.get_sin_wave_amplitude(signal_frequency, current_time)
        mcp.set_voltage(signal)
        sg.wait_for_sampling_period(sampling_frequency)
finally:
    mcp.deinit()
