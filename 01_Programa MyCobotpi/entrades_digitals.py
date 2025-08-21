from pymycobot.mycobot import MyCobot
import RPi.GPIO as GPIO
from time import sleep
mc = MyCobot('/dev/ttyAMA0',1000000)
valor = False
GPIO.setmode(GPIO.BCM)

PIN = 1
GPIO.setup(PIN,GPIO.IN)

valor = GPIO.input(PIN)



while True:
     
    sleep(0.1)
    print(GPIO.input(PIN))
    if GPIO.input(PIN):
        print('Pin Activat.')
        