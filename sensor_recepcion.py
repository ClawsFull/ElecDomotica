import serial
import asyncio
import time
import websockets
import json
#clase para recibir informacion desde un sensor analogo en arduino mediante comunicacion serial
class sensor:
    def __init__(self, websocket, puerto_arduino):
        #websocket para enviar la informacion
        self.ws = websocket
        #Conexion serial a arduino
        self.serial_arduino = serial.Serial(puerto_arduino,9600)
        #espera para que se conecte correctamente
        time.sleep(1)
    #funcion para enviar datos al websocket
    async def enviar_instrucciones(self):
        #estado inicial
        estado_0 = 'normal'
        while True:
            #Recepcion del valor
            valor = int(self.serial_arduino.readline().decode('ascii'))
            #Se define que si el valor equivale a estar en sombra se envia que el motor debe abrir para dejar paso de luz
            if valor>400:
                estado_1 = 'sombreado'
                await self.ws.send(json.dumps({'Motor_0':'abrir'}))
            #Se define que si el valor equivale a estar iluminado se envia que el motor debe cerrar para disminuir el paso de luz
            elif valor <200:
                estado_1 = 'iluminado'
                await self.ws.send(json.dumps({'Motor_0':'cerrar'}))
            #En caso de que el valor se encuentre entre los valores aceptables el motor debe parar, 
            # se evita que lo envie constantemente para poder realizar control manual
            else:
                estado_1 = 'normal'
                if not(estado_0==estado_1):
                    await self.ws.send(json.dumps({'Motor_0':'parar'}))
            #se asigna estado actual al estado anterior
            estado_0 = estado_1
#funcion de uso para interconectar arduino con el websocket
async def use_ws():
    #definir ruta de websocket a conectarse
    uri = "ws://localhost:8000/ws/test/"
    #definir ruta de arduino a conectarse
    puerto_arduino = '/dev/ttyUSB0'
    while True:
        #Se utiliza while y try para que el programa intente conectarse hasta que obtenga conexion
        try:
            #conectarse al websocket
            async with websockets.connect(uri) as websocket:
                #iniciar la clase que se comunica con arduino
                sensor_arduino = sensor(websocket, puerto_arduino)
                #Iniciar la funcion que envia instrucciones al servidor
                await asyncio.gather(
                                    sensor_arduino.enviar_instrucciones(),
                                    ),
        except: pass
#iniciar programa
asyncio.get_event_loop().run_until_complete(use_ws())