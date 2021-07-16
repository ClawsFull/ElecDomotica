# :bulb: Proyecto ElecDomotica :bulb:
## Resumen de proyecto
* Title: "ElecDomotica"
* Version: 0.20210715
* Created: 2021/06/02
* Description:  
El proyecto está orientado a controlar cortina y luces
Se dispone de Arduino como transformadores de señal Analógico/Digital
Una Raspberry Pi 3B para el control principal con conectividad a Wifi y Bluetooth. 
Se sigue la siguiente estructura para el sistema:
<br>
<img src="https://github.com/ClawsFull/ElecDomotica/blob/main/Sistema%20Domotico.svg" />
<br>

## Requerimientos
* Modulo Relé de al menos dos canales
* Dos o más LDR GL5528 10Kohm
* Arduino o equivalente:
    * Mínimo de 3 pines analógicos (se recomiendan 3 mas 2 para protocolo I2C de la pantalla) 
    * 4 pines digitales para motor
    * Conexión USB o adaptador para comunicación serial a 38400 baudios o superior
* Raspberry Pi 3B:
    * 16GB de memoria microSD como mínimo
    * 1GB de RAM o más
* Conexión a internet Wifi o Ethernet
* Botones
* Driver de 4 canales, 5V de entrada y activación de al menos 3V para los pines de control
* Motor stepper
* Fuente de alimentación de 12 a 5V para el motor
* Fuente de alimentación para Raspberry de mínimo 2A 
* Pantalla Oled con comunicación I2C (opcional)
## Referencias 
1. Django: https://docs.djangoproject.com/en/3.2/
2. Channels: https://channels.readthedocs.io/en/stable/
3. Websocket: https://websockets.readthedocs.io/en/stable/
4. Asyncio: https://docs.python.org/3/library/asyncio.html
5. Pyserial: https://pythonhosted.org/pyserial/
6. threading: https://docs.python.org/es/3/library/threading.html
7. Arduino: https://www.arduino.cc/reference/en/
8. Raspberry: https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
