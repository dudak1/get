import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
tro = 13
rang = range(255, 0, -1)

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(tro, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN) 

def dec2bin(val):
    return[int(elem) for elem in bin(val)[2:].zfill(8)]

def adc():
    i = 255
    val = 0
    while i > 1:
        GPIO.output(dac, dec2bin(val+i)[0:8])
        time.sleep(0.01)
        if GPIO.input(comp) == GPIO.LOW:
            val += i
        i//=2
    return(val)

try:
    while True:
        vall = adc()
        ll = [1]*((vall//32))+[0]*((8-vall//32))
        if vall/256*3.3 > 6:
            vall /=2
        GPIO.output(leds, ll[0:8])
        time.sleep(1)
        ## print(ll)
        print(round(vall/256*3.3, 1))

finally:
    GPIO.output(dac, 0)
    GPIO.output(tro, 0)
    
    GPIO.cleanup()