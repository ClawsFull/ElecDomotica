import asyncio
import websockets
import json
import RPi.GPIO as GPIO
#######funciones de uso###############
class control_programa:
    def __init__(self, websocket):
        self.ws = websocket
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.pinin = {
                'Luz_0':17,
                'Luz_1':27,
                'Motor_0_abrir':22,
                'Motor_0_cerrar':23,
                }
        self.action_pin = {}
        for i in self.pinin.keys(): self.action_pin[str(self.pinin[i])] = i
        for pin in list(self.pinin.keys()): 
            GPIO.setup(self.pinin[pin],GPIO.IN)
            GPIO.add_event_detect(self.pinin[pin], GPIO.BOTH, bouncetime=200)
    async def enviar_instrucciones(self):
        while True:
            if GPIO.event_detected(self.pinin['Luz_0']):
                await self.ws.send(json.dumps({'Luz_0':'cambio'}))

            if GPIO.event_detected(self.pinin['Luz_1']):
                await self.ws.send(json.dumps({'Luz_1':'cambio'}))

            if GPIO.event_detected(self.pinin['Motor_0_abrir']):
                if int(GPIO.input(self.pinin['Motor_0_abrir']))==1:
                    await self.ws.send(json.dumps({'Motor_0':'abrir'}))
                else:
                    await self.ws.send(json.dumps({'Motor_0':'parar'}))

            if GPIO.event_detected(self.pinin['Motor_0_cerrar']):
                if int(GPIO.input(self.pinin['Motor_0_cerrar']))==1:
                    await self.ws.send(json.dumps({'Motor_0':'cerrar'}))
                else:
                    await self.ws.send(json.dumps({'Motor_0':'parar'}))
#######conexion websocket###############

async def connect(websocket):
    msg = await websocket.recv()
    msg = json.loads(msg)
    return msg
async def use_ws():
    uri = "ws://localhost:8000/ws/test/"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                estado_inicial = await connect(websocket)
                control_in = control_programa(websocket)
                while True: 
                    # await send(websocket)
                    await asyncio.gather(
                        control_in.enviar_instrucciones()
                        )
        except: print('sin_conexion')
            
asyncio.get_event_loop().run_until_complete(use_ws())
