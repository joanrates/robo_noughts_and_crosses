from pymycobot.mycobot import MyCobot
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)
mc = MyCobot('/dev/ttyAMA0',1000000)
if ser.in_waiting():
    info = ser.read()
    print(info)
    print(type(info))
    
if ser.writable():

    ser.write(b'm')
    ser.write(b'a')
    ser.write(b'a')
    ser.write(b'a')
    ser.write(b'a')
    print('a')
