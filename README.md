# :bulb: Proyecto ElecDomotica :bulb:
## Resumen de proyecto
* Title: "ElecDomotica"
* Version: 0.20210715
* Created By: Camilo Alfonso Santibanez Chacon, Alen Asenie Rosas
* Created: 2021/06/02
* Last Modified: 2021/07/15
* Description:  
El proyecto está orientado a controlar cortina y luces
Se dispone de arduinos como tranformadores de señal Analogico/Digital
Una Raspberry Pi 3B para el control principal con conctividad a Wifi y Bluetooth
## Requerimientos
* Modulo Relé de al menos dos canales
* Dos o más LDR GL5528 10Kohm
* Arduino o equinalente:
    * Minimo de 3 pines analogico (se recomiendan 3 más 2 para protocolo I2C de la pantalla) 
    * 4 pines digitales para motor
    * Conexión USB o adaptador para comunicación serial 
* Driver de 4 canales, 5V de entrada y activacion de almenos 3V para los mines de control
* Raspberry Pi 3B+:
    * 16GB de memoria SD como minimo
    * 1GB de ram o más
* Conexión a internet Wifi o Ethernet
* Fuente de alimentación de 12 a 5V para el motor
* Fuente de alimentación para Raspberry de minimo 2A 
* Pantalla Oled con comunicacion I2C (opcional)
## Referencias 
1. Django: https://docs.djangoproject.com/en/3.2/
2. Channels: https://channels.readthedocs.io/en/stable/
3. Websocket: https://websockets.readthedocs.io/en/stable/
4. Asyncio: https://docs.python.org/3/library/asyncio.html
5. Pyserial: https://pythonhosted.org/pyserial/
6. threading: https://docs.python.org/es/3/library/threading.html
7. Arduino: https://www.arduino.cc/reference/en/
8. Raspberry: https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/

