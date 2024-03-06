import RPi.GPIO as GPIO
import time
from matplotlib import pyplot as plt

dac = [8, 11, 7, 1, 0, 5, 12, 6]
number = [0, 0, 0, 0, 0, 1, 0, 0]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

GPIO.output(dac, number)
time.sleep(20)

GPIO.output(dac, 0)
GPIO.cleanup()

x = [0, 5, 32, 64, 127, 255]
y = [0.05, 0.114, 0.457, 0.865, 1.671, 3.243]

plt.plot(x, y)
plt.show(   )