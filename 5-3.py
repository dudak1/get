import RPi.GPIO as GPIO
import time
dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)
leds = [2,3,4,17,27,22,10,9]
GPIO.setup(leds,GPIO.OUT)

def dec2bin(a):
    return [int(bit) for bit in bin(int(a))[2:].zfill(8)]


def adc(troyka):
    d = 0
    for i in range (7,-1,-1):
        d+=2**i
        GPIO.output(dac,dec2bin(d))
        time.sleep(0.001)
        jokerge = GPIO.input(comp)
        if(jokerge==1):
            d-=2**i 
    return d


try:
    while(True):
        k=0
        t=0
        c=0
        while(c<adc(troyka)):
            k+=2**t
            t+=1
            c+=32
        GPIO.output(leds,dec2bin(k))
        print(3.3*adc(troyka)/255)
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()