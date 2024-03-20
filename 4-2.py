import RPi.GPIO as GPIO

dac = [8,11,7,1,0,5,12,6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)


def per(x):
    res = ""
    while x != 1:
        res += str(x % 2)
        x //= 2
    res += '1'
    res += (8-len(res))*'0'
    return list(reversed(res))

try:
    while True:
        try:
            x = float(input("Enter number from 0 to 255: "))
        except Exception:
            print("Введена буква")
            continue
        if (0 <= int(x) <= 255):
            x = int(x)
            GPIO.output(dac, list(map(int, per(x))))
            v = x / 256 * 3.3
            print(f"voltage: {v:.4}")
        else:
            print("try again")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
