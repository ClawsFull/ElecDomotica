import asyncio
import websockets
import json
import RPi.GPIO as GPIO
import time
import serial
import serialComunication
import random

#######funciones de uso###############   
##Clase para controlar las salidas
class Salidas:
    def __init__(self, estados_iniciales, websocket):
        #cargar websocket para la comunicacion
        self.ws = websocket
        #preparar GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) 
        #Guardar estado inicial
        self.estados = estados_iniciales
        #Definir pines de salida
        self.pinout = {
                'Luz_0':0,
                'Luz_1':5,
                }
        #Set pines de salida
        for pin in list(self.pinout.keys()):
            GPIO.setup(self.pinout[pin],GPIO.OUT)
    #Funcion para recibir estados desde el servidor
    async def recibir_instrucciones(self):
        while True:
            #recibir nuevo estado
            self.estados = json.loads(await self.ws.recv())
            # Actualizar el estado de las luces
            await self.cambio_luz()
    # Funcion para actualizar el estado de las luces
    async def cambio_luz(self):
        for i in range(2):
            GPIO.output(self.pinout[f"Luz_{i}"],self.estados[f"Luz_{i}"])

#######funciones de uso###############
#control a partir de botones
class control_botones:
    def __init__(self, websocket):
        # definir websocket para enviar datos
        self.ws = websocket
        # preparar GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        # definir pines de entrada 
        self.pinin = {
                'Luz_0':17,
                'Luz_1':27,
                }
        # asignar una veriable que indique la accion que representa cada pin ({pin:accion})
        self.action_pin = {}
        for i in self.pinin.keys(): self.action_pin[str(self.pinin[i])] = i
        #set pines de entrada y agregarles deteccion de edge
        for pin in list(self.pinin.keys()): 
            GPIO.setup(self.pinin[pin],GPIO.IN)
            GPIO.add_event_detect(self.pinin[pin], GPIO.BOTH, bouncetime=200)
    #envio de datos al servidor
    async def enviar_instrucciones(self):
        while True:
            await asyncio.sleep(0.0001)
            #si se cambia el estado en el pin de Luz0 se envia el mensaje para cambiar estado
            if (GPIO.event_detected(self.pinin['Luz_0']) and int(GPIO.input(self.pinin['Luz_0']))==1):
                await self.ws.send(json.dumps({'Luz_0':'cambio'}))

            #si se cambia el estado en el pin de Luz1 se envia el mensaje para cambiar estado
            if (GPIO.event_detected(self.pinin['Luz_1']) and int(GPIO.input(self.pinin['Luz_1']))==1):
                await self.ws.send(json.dumps({'Luz_1':'cambio'}))
class conexion_serial:
    def __init__(self):
        arduino = serialComunication.com_serial(dir_com="/dev/ttyUSB0")
        self.arduino=arduino
        print(arduino._com_serial__channel)
        arduino.init_com(baud=38400)   
        self.llamados_de_motor=[63,64,83,84] 
        
    async def mesajes_aleatorios(self):
        await asyncio.sleep(2.0)
        try:
            while True:
                if random.randint(1, 25)==1:
                    self.arduino.send_comand(self.llamados_de_motor[random.randint(0,3)],'c')
                    await asyncio.sleep(0.1)
                self.arduino.send_comand(0,'c')
                for conteo in [0,1]:
                     self.arduino.recive()
                self.arduino.send_comand(1,'c')
                for conteo in [0,1]:
                    self.arduino.recive()
                self.arduino.send_comand(2,'c')
                for conteo in [0,1]:
                    self.arduino.recive()
                await asyncio.sleep(0.8)
        except Exception as error:
            if error =='KeyboardInterrupt':
                
                print("Fin del programa")
            else:
                print("Error :" , error)
        finally:
            self.arduino.close_com()
    
#######conexion websocket###############
#recibir el mensaje que envia el servidor al conectarse
async def connect(websocket):
    msg = await websocket.recv()
    msg = json.loads(msg)
    return msg

#programa principal
async def use_ws():
    #definir ruta de websocket a conectarse
    uri = "ws://localhost:8000/ws/test/"
    while True:
        #Se utiliza while y try para que el programa intente conectarse hasta que obtenga conexion
        #try:
            #conectarse al websocket
            async with websockets.connect(uri) as websocket:
                #recibir estado inicial
                estado_inicial = await connect(websocket)
                #iniciar la clase que controla los pines de salida
                control_out = Salidas(estado_inicial,websocket)
                #iniciar la clase que controla los pines de entrada
                control_in = control_botones(websocket)
                #iniciar la clase de comunicacion serial
                control_serial = conexion_serial()
                ##iniciar en paralelo la recepcion de estados (junto con el control de luz), 
                #y el envio de cambios de estado segun los botones (en ese orden)
                await asyncio.gather(
                                    control_out.recibir_instrucciones(),
                                    control_in.enviar_instrucciones(),
                                    control_serial.mesajes_aleatorios()
                                    ),
        #except: pass
#iniciar programa
asyncio.get_event_loop().run_until_complete(use_ws())
