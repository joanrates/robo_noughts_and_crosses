from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/ttyAMA0',1000000)
mc.power_on()
estat = 0
while True:
    if estat == 0:
        mc.send_angles([0,0,0,0,0,0],10)
        estat = 1
    elif estat == 1:
        if mc.is_in_position([0,0,0,0,0,0]):
            estat = 2
    elif estat == 2:
        print('jasta')
        estat = 3
    