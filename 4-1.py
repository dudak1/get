import RPi.GPIO as GPIO
import time

dac = [8,11,7,1,0,5,12,6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)


def per(a):
    res = ""
    while a != 1 and a != 0:
        res += str(a % 2)
        a //= 2
    res += '1'
    res += (8-len(res))*'0'
    return list(reversed(res))

f = 1
t = 0
x = 0

try:
    period = float(input("Period: "))
    while True:
        GPIO.output(dac, list(map(int, per(x))))
        print(f"voltage: {x/256*3.3:.4}")
        if x == 0:
            f = 1
        if x == 255:
            f = 0
        if f == 1:
            x += 1
        else:
            x-=1
        time.sleep(period/512)
        t+= 1
except Exception:
    print("Uncorrect enter")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
