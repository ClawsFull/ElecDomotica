import serialComunication
import time
import random

arduino = serialComunication.com_serial(dir_com="/dev/ttyUSB0")#"COM4")#
print(arduino._com_serial__channel)
arduino.init_com(baud=38400)
time.sleep(2)

try:
    while True:
        if random.randint(1, 25)==1:
            arduino.send_comand(87,'c')
            time.sleep(0.1)
        arduino.send_comand(0,'c')
        for conteo in [0,1]:
            arduino.recive()
        arduino.send_comand(1,'c')
        for conteo in [0,1]:
            arduino.recive()
        arduino.send_comand(2,'c')
        for conteo in [0,1]:
            arduino.recive()
        time.sleep(0.8)
except Exception as error:
    if error =='KeyboardInterrupt':
        
        print("Fin del programa")
    else:
        print("Error :" , error)
finally:
    arduino.close_com()
#a=input("")
