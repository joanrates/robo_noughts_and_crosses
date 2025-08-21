from pymycobot.mycobot import MyCobot


mc = MyCobot('/dev/ttyAMA0',1000000)
mc.power_on()
print(mc.get_angles()) 
mc.set_color(0,0,0)
Posicio = [5.71, 50.62, -126.47, 14.94, -81.12, -72.42]
mc.send_angles(Posicio,10)
mc.power_off()
