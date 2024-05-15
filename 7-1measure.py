import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

#function to_bin
def to_bin(n):
    s = bin(n)[2:].zfill(8)
    return list(map(int, s))

#put  signal
def adc():
    k = 0
    for i in range(7, -1, -1):
        k += 2 ** i
        dac_val = to_bin(k)
        GPIO.output(dac, dac_val)
        time.sleep(0.01)
        cmp = GPIO.input(comp)
        if cmp == GPIO.HIGH:
            k -= 2 ** i
    return k

def num2_dac_leds(value):
    signal = to_bin(value)
    GPIO.output(dac, signal)
    return signal


#settings
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13
bits = len(dac)
levels = 2 ** bits
maxV = 3.3

GPIO.setmode(GPIO.BCM)

GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 0)

data_volts = []
data_times = []
data_val   = []

try:
    val = 0
    GPIO.output(troyka, 1)
    start_time = time.time()

    #getting data
    while(val < 207):
        val = adc()
        voltage = val / levels * maxV
        print(f"Charging: {val}, voltage = {voltage:.3f}")
        num2_dac_leds(val)
        data_times.append(time.time() - start_time)
        data_volts.append(voltage)
        data_val.append(val)

    discharge_start = len(data_volts)

    GPIO.output(troyka, 0)

    while(val > 64):
        val = adc()
        voltage = val / levels * maxV
        print(f"Discharging: {val}, voltage = {voltage:.3f}")
        num2_dac_leds(val)
        data_times.append(time.time() - start_time)
        data_volts.append(voltage)
        data_val.append(val)

    end_time = time.time()

    #write time and maxV to settings.txt
    with open("./settings.txt", "w") as file:
        file.write(str((end_time - start_time) / len(data_volts)))
        file.write(("\n"))
        file.write(str(maxV / 256))

    print(end_time - start_time, " secs\n", len(data_volts) / (end_time - start_time), "\n", maxV / 256)

finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

#writing data to fil "data.txt"
with open("data.txt", "w") as file:
    for i in range(discharge_start):
        print(f"{data_val[i]}", file=file)
    for i in range(discharge_start, len(data_volts)):
        print(f"{data_val[i]}", file=file)

#draw schedule
plt.plot(data_times, data_volts)
plt.show()