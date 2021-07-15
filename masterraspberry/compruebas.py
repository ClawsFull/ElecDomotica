import serialComunication
import time
import asyncio
import random

arduino = serialComunication.com_serial(dir_com="/dev/ttyUSB0")
print(arduino._com_serial__channel)
arduino.init_com()
time.sleep(2)

try:
    while True:
        arduino.send_comand(random.randint(0,2),'c')
        arduino.recive()
        time.sleep(0.1)
    
except Exception as error:
    if error =='KeyboardInterrupt':
        print("Fin del programa")
    else:
        print("Error :" , error)
finally:
    arduino.close_com()
a=input("")
