from pymycobot.mycobot import MyCobot

mc = MyCobot('/dev/ttyAMA0',1000000)
primeraPos = [139.8, -19.1, 126.6, 92.39, 86.41, 27.44]

mc.power_on()
mc.send_coords(primeraPos,10,0)
print(mc.get_coords())
while True:
    valorx, valory, valorz = primeraPos[0], primeraPos[1], primeraPos[2]
    valor = raw_input('nou valor x: ')
    if valor != '':
        valorx = int(valor)
    valor = raw_input('nou valor y: ')
    if valor != '':
        valory = int(valor)
    valor = raw_input('nou valor z: ')
    if valor != '':
        valorz = int(valor)

    if(valorx != primeraPos[0]):
        mc.send_coord(1, valorx, 10)
        primeraPos[0]= valorx
    if(valory != primeraPos[1]):
        mc.send_coord(2, valory, 10)
        primeraPos[1] = valory
    if(valorz != primeraPos[2]):
        mc.send_coord(3, valorz, 10)
        primeraPos[2] = valorz
    print(mc.get_coords())