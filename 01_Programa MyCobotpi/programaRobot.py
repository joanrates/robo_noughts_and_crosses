#importem la funció sleep de la llibreria time
from time import sleep
#Importem la llibreria MyCobot que ens permet comunicar amb el robot
from pymycobot.mycobot import MyCobot
#Importem la llibreria d'entrades i sortides de la raspberry
import RPi.GPIO as GPIO
#Importem la llibreria de comunicació serie per a poder-nos comunicar amb l'ordinador
import serial

#iniciem l'objecte per el qual ens comunicarrem amb l'ordinador
ser = serial.Serial('/dev/ttyUSB0', 9600)
#iniciem l'objecte per al qual ens comunicarem amb el robot
mc = MyCobot('/dev/ttyAMA0',1000000)
#Establim que les entrades i sortides estaran codificades amb el nombre del processador en lloc
#del nombre pintat a la placa de la raspberry ja que no coincideixen
GPIO.setmode(GPIO.BCM)

#Definim una constant per referir-nos al pin que farem servir per la entrada del botó start
PINSTART = 23
#Definim una constant per referir-nos al pin que farem servir per la entrada del botó stop
PINSTOP = 1
#Definim una constant per referir-nos al pin que farem serfir per a enviar la senyal de sortida al relé
PINSORTIDA = 19

#Iniciem les entrades i sortides com a tals
GPIO.setup(PINSTART, GPIO.IN)
GPIO.setup(PINSTOP,GPIO.IN)
GPIO.setup(PINSORTIDA, GPIO.OUT)

#Establim una variable que farem servir en cada moment per saber si el robot s'està movent o no
movent = False
#Definim una variable que ens farà de buffer per a guardar l'ultim valor llegit en la entrada sèrie
info = b'b'
#Creem dues variables per guardar les dades que arribin des de l'ordinador
fila = 0
columna = 0
#creem una llista amb totes les posicions en que es pot deixar una peça
posicions = [[39.46, -58.53, -80.06, -54.84, -43.85, 53.08],[47.28, -64.68, -67.41, -50.53, -30.41, 41.83],[58.71, -53.87, -80.06, -43.15, -37.0, 35.24],[27.86, -67.41, -55.19, -52.82, -51.59, 35.24],[38.05, -67.14, -55.01, -51.85, -45.26, 34.98],[51.32, -67.5, -55.28, -53.61, -51.06, 35.06],[27.33, -67.5, -55.01, -45.87, -73.3, 34.89],[34.18, -67.5, -55.01, -44.03, -72.94, 34.89],[45.08, -67.58, -55.19, -45.7, -76.28, 34.89]]
#Creem una llista amb totes les posicions en les que es pot recollir una peça de forma de creu
recollircreu = [[-17.49, -39.02, -142.11, 10.45, -98.08, 22.58],[-11.42, -36.47, -127.35, -12.12, -96.32, 43.15],[-11.86, -51.41, -94.48, -33.75, -94.74, 42.97],[-9.49, -61.69, -66.44, -50.18, -94.48, 42.97]]
#Creem una llista més amb totes les posicions que es pot recollir les peçes amb forma de cercle
recollircercle = [[123.39, -56.68, -86.39, -42.97, -52.91, 49.57], [110.39, -54.93, -86.48, -42.01, -62.92, 43.85], [95.44, -50.53, -86.83, -36.21, -78.92, 35.06], [81.38, -60.38, -79.62, -19.33, -88.41, 15.73]]
#Definim una posició inicial amb el robot completament estirat
INICI = [0,0,0,0,0,0]
#Fem una posició intermitja des de la qual es pugui arribar a totes les posicions de la graella
INTERSORITR = [38.49, -26.8, -55.28, -94.13, -83.05, 33.13]
#Definim una constant per a la velocitat
VELOCITAT = 15
#Definim una posició des de la que es pugui arribar a totes les posicions utilitzades per a agafar les peces en forma de creu
CREUINTER = [5.71, 50.62, -126.47, 14.94, -81.12, -72.42]
#Definim una posició des de la que es pugui arribar a totes les posicions utilitzades per a agafar les peces en forma de cercle
CERCLEINTER = [99.22, -44.73, -33.66, -106.78, -68.64, 38.4]
#Tenim una variable estat en el que es guardarà el procés actual del robot
estat = 0
#Finalment s'engega el robot en cas que estigués parat
mc.power_on()
#s'engega un bucle amb la màquina d'estats corresponent
while True:
    #En cas que el robot s'estigui movent s'activa la sortida, si ho ho fa es desactiva
    if movent:
        GPIO.output(PINSORTIDA, 1)
    else:
        GPIO.output(PINSORTIDA, 0)
    #Es mostra l'estat per pantalla, ja que permet un major control del que passa en tot moment
    print(estat)
    #En cas que es premi el pulsador d'estop es torna a iniciar el robot
    if not GPIO.input(PINSTOP)and estat != 0:
        #Es para allà on sigui
        mc.pause()
        #Es passa a l'estat inicial
        estat = 0
        #Es deiaxa de moure
        movent = False
        #En cas que es pugui escriure a través del canal serie
        if ser.writable:
            #S'escriu el byte a, d'atur
            ser.write(b'a')
    #Estat inicial
    if estat ==0:
        #Posem el display de color vermell
        mc.set_color(255,0,0)
        #En el cas que es premi el pin de stert
        if GPIO.input(PINSTART):
            #Saltem a l'estat 1
            estat = 1
            #Enviem la posició inicial al robot
            mc.send_angles(INICI, VELOCITAT)
            #Indiquem que el robot s'està movent
            movent = True
            #Esperem un petit moment per evitar errors de lectura en la posició del robot.
            #Procés que es repeteix més endavant amb la mateixa finalitat
            sleep(0.1)
    #Estat 1
    elif estat == 1:
        #Obrim la pinça del robot
        mc.set_pwm_output(23,50,15)
        #Esperem un moment
        sleep(0.1)
        #Comporovem si el robot ha arribat a la posició desitjada
        if mc.is_in_position(INICI):
            #En cas que hi hagi arribat indiquem que ja no es mou
            movent = False
            #Passem al següent estat
            estat = 2
            #Enviem el byte m a través del canal serie per indicar a l'ordinador que pot començar la transmissió
            ser.write(b'm')
    elif estat == 2:
        #Canviem el color del display a verd
        mc.set_color(0,255,0)
        #En el cas que hi hagi alguna cosa per llegir en el canal serie
        if ser.inWaiting():
            #Es llegeix el primer byte que arribés i es guarda a la variable info
            info = ser.read()
            #comprova la informació per si coincideix amb s
            if info == 's':
                #en tal cas torna a enviar la senyal de marxa, de tal manera que s'engegui el programa que s'engegui primer
                #el programa funciona de manera adequada
                ser.write(b'm')
            #En el cas que la informació sigui f, el seguent nombre serà la fila de destí i es llegeix en l'estat 3
            if info == 'f':
                estat = 3
            #En el cas que la informació siguic, el seguent nombre serà la columna de destí i es llegeix en l'estat 4
            elif info == 'c':
                estat = 4
    elif estat == 3:
        #Espera a que hi hagi alguna cosa per llegir si no hi ha res
        if ser.inWaiting():
            #Es llegeix un byte
            info = ser.read()
            #Es converteix a enter i es posa a la variable fila
            fila = int(info)
            #Es torna a l'estat anterior
            estat = 2
    elif estat == 4:
        #Espera a que hi hagi alguna cosa per llegir
        if ser.inWaiting():
            #Llegeix un byte
            info = ser.read()
            #Transforma el byte a un nombre enter i el guarda a la variable columna
            columna = int(info)
            #Es passa al següent estat
            estat = 5
    elif estat == 5:
        #Espera a que hi hagi alguna cosa per llegir si no hi ha res
        if ser.inWaiting():
            #Es llegeix un byte
            info = ser.read()
            #En el cas que el byte fos 9 es tornaria a l'estat inicial ja que significaria que hi ha hagut algun error
            if int(info) == 9:
                estat = 0
            #En el cas que el nombre sigui parell es va a l'estat 6
            elif int(info)%2 == 0:
                estat = 6
            #En cas que sigui senar a l'estat 7
            else: estat = 7
    elif estat == 6:
        #S'envien les posicions d'aproximar-se a les peces en forma de creu al robot
        mc.send_angles(CREUINTER,VELOCITAT)
        #s'sindica que el robot s'està movent
        movent = True
        sleep(0.1)
        #En cas que el robot hagi arribat a la posició desitjada
        if mc.is_in_position(CREUINTER):
            #S'indica que el robot ja no es mou
            movent = False
            #Es passa al seguent estat
            estat = 8
    elif estat == 7:
        #S'envien les posicions d'aproximar-se a les peces en forme de cercle al robot
        mc.send_angles(CERCLEINTER,VELOCITAT)
        #s'sindica que el robot s'està movent
        movent = True
        sleep(0.1)
        #En cas que el robot hagi arribat a la posició desitjada
        if mc.is_in_position(CERCLEINTER):
            #S'indica que el robot ja no es mou
            movent = False
            #Es passa al següent estat
            estat = 9
    elif estat == 8:
        #Es calcula quina peça s'ha d'agafar del carregador
        pos = int(info) / 2
        #s'envien els angles d'aquella peça
        mc.send_angles(recollircreu[pos],VELOCITAT)
        movent = True
        sleep(0.1)
        #Si el robot estigui en posició
        if mc.is_in_position(recollircreu[pos]):
            movent = False
            #Es passa a l'estat següent
            estat = 10
            #Es tanca la pinça
            mc.set_pwm_output(23,50,28)
    elif estat == 9:
        #Es calcula quina peça s'ha d'agafar del carregador
        pos = (int(info)-1)/2
        #s'envien els angles d'aquella peça
        mc.send_angles(recollircercle[pos],VELOCITAT)
        movent = True
        sleep(0.1)
        #En cas que el robot estigui en posició
        if mc.is_in_position(recollircercle[pos]):
            movent = False
            #Es passa al següent estat
            estat = 11
            #Es tanca la pinça
            mc.set_pwm_output(23,50,28)
    elif estat == 10:
        #S'envia el robot al punt d'aproximació una altra vegada
        mc.send_angles(CREUINTER,VELOCITAT)
        movent = True
        sleep(0.1)
        #Si és al punt d'aproximació es passa al següent estat
        if mc.is_in_position(CREUINTER):
            movent = False
            estat = 12
    elif estat == 11:
        #S'envia el robot al punt d'aproximació una altra vegada
        mc.send_angles(CERCLEINTER,VELOCITAT)
        movent = True
        sleep(0.1)
        #Si és al punt d'aproximació es passa al següent estat
        if mc.is_in_position(CERCLEINTER):
            movent = False
            estat = 12
    elif estat == 12:
        #S'envia el robot al punt d'aproximació de la graella
        mc.send_angles(INTERSORITR, VELOCITAT)
        movent = True
        sleep(0.1)
        # Si el robot és al punt d'aproximació de la graella
        if mc.is_in_position(INTERSORITR):
            movent = False
            #Es passa al seguent estat
            estat = 13
    elif estat == 13:
        #Es calcula la posició de la graella on es guarden els angles del destí
        pos = fila * 3 + columna
        #S'envien els angles corresponents
        mc.send_angles(posicions[pos],VELOCITAT)
        movent = True
        sleep(0.1)
        #En cas que el robot hagi arribat al seu destí
        if mc.is_in_position(posicions[pos]):
            movent = False
            #Es passa al següent estat
            estat = 14
    elif estat == 14:
        sleep(0.5)
        #S'obre la pinça
        mc.set_pwm_output(23,50,15) 
        estat = 15
        
    elif estat == 15:
        #S'envien els angles d'aproximació a la graella altra vegada
        mc.send_angles(INTERSORITR, VELOCITAT)
        movent = True
        sleep(0.1)
        #En el cas que el robot hagi assolit la posició d'aproximació
        if mc.is_in_position(INTERSORITR):
            movent = False
            #Es salta al següent estat
            estat = 16
    elif estat == 16:
        #S'envia el robot a l'estat 1 amb la posició inicial
        estat = 1
        mc.send_angles(INICI, VELOCITAT)
        movent = True
        sleep(0.1)