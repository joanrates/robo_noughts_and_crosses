from pymycobot.mycobot import MyCobot
from time import sleep

mc = MyCobot('/dev/ttyAMA0',1000000)
mc.power_on()
mc.set_color(0,0,0)
while True:
    try:
        valor = int(input('degrees: '))
        mc.set_pwm_output(23,50,valor)
        sleep(2)
    except:
        mc.power_off()
        print('error')
        break



