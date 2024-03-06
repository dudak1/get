import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
while True:
    print(GPIO.input(16))