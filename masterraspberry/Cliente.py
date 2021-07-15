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
        
    

#         async def cambio_estados(self,websocket):
#             action = self.action_pin[str(pin)]
#             if action=='Luz_0':
#                 await websocket.send(json.dumps({'Luz_0': 'cambio'}))
#             if action=='Luz_1':
#                 await websocket.send(json.dumps({'Luz_1': 'cambio'}))
#         #     if action=='Motor_0_abrir' and GPIO.input(pin):
        #         await websocket.send(json.dumps({'Motor_0': 'abrir'}))
        #     if action=='Motor_0_abrir' and not(GPIO.input(pin)):
        #         await websocket.send(json.dumps({'Motor_0': 'parar'}))
        #     if action=='Motor_0_cerrar' and GPIO.input(pin):
        #         await websocket.send(json.dumps({'Motor_0': 'cerrar'}))
        #     if action=='Motor_0_cerrar' and not(GPIO.input(pin)):
        #         await websocket.send(json.dumps({'Motor_0': 'parar'}))
        # for pin in list(self.pinin.keys()):
        #     GPIO.add_event_detect(self.pinin[pin], GPIO.BOTH)
        #     GPIO.add_event_callback(self.pinin[pin], cambio_estados(websocket), bouncetime=200)
            
class Salidas:
    def __init__(self, estados_iniciales, websocket):
        self.ws = websocket
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) 
        self.estados = estados_iniciales
        self.pinout = {
                'Luz_0':0,
                'Luz_1':5,
                'Motor_0_p0':6,
                'Motor_0_p1':13,
                'Motor_0_p2':19,
                'Motor_0_p3':26,
                }
        for pin in list(self.pinout.keys()):
            GPIO.setup(self.pinout[pin],GPIO.OUT)
    async def recibir_instrucciones(self):
        estado = await self.ws.recv()
        estado = json.loads(estado)
        self.estados = estado
        return self.estados
    async def cambio_luz(self):
        for i in range(2):
            GPIO.output(self.pinout[f"Luz_{i}"],self.estados[f"Luz_{i}"])
    async def control_motor(self):
        time_step = 0.01
        if self.estados['Motor_0']=='parar':
            for i in range(4):
                GPIO.output(self.pinout[f"Motor_0_p{i}"],False)
        while self.estados['Motor_0']=='abrir':
            GPIO.output(self.pinout[f"Motor_0_p1"],False)
            GPIO.output(self.pinout[f"Motor_0_p2"],False)
            GPIO.output(self.pinout[f"Motor_0_p3"],False)
            GPIO.output(self.pinout[f"Motor_0_p0"],True)
            await asyncio.sleep(time_step/4)
            GPIO.output(self.pinout[f"Motor_0_p0"],False)
            GPIO.output(self.pinout[f"Motor_0_p1"],True)
            await asyncio.sleep(time_step/4)
            GPIO.output(self.pinout[f"Motor_0_p1"],False)
            GPIO.output(self.pinout[f"Motor_0_p2"],True)
            await asyncio.sleep(time_step/4)
            GPIO.output(self.pinout[f"Motor_0_p2"],False)
            GPIO.output(self.pinout[f"Motor_0_p3"],True)
            await asyncio.sleep(time_step/4)
            # await self.ws.send(json.dumps({'refrescar_datos':True}))
            # msg = await asyncio.wait_for(self.ws.recv(), timeout=10)
            # print(msg)
            # self.estados = json.loads(await self.ws.recv())
            # print(self.estados )
        while self.estados['Motor_0']=='cerrar':
            GPIO.output(self.pinout[f"Motor_0_p1"],False)
            GPIO.output(self.pinout[f"Motor_0_p2"],False)
            GPIO.output(self.pinout[f"Motor_0_p3"],False)
            GPIO.output(self.pinout[f"Motor_0_p0"],True)
            await asyncio.sleep(time_step/4)
            GPIO.output(self.pinout[f"Motor_0_p0"],False)
            GPIO.output(self.pinout[f"Motor_0_p3"],True)
            await asyncio.sleep(time_step/4)
            GPIO.output(self.pinout[f"Motor_0_p3"],False)
            GPIO.output(self.pinout[f"Motor_0_p2"],True)
            await asyncio.sleep(time_step/4)
            GPIO.output(self.pinout[f"Motor_0_p2"],False)
            GPIO.output(self.pinout[f"Motor_0_p1"],True)
            await asyncio.sleep(time_step/4)
            # await self.ws.send(json.dumps({'refrescar_datos':True}))
            # estado = await self.ws.recv()
            # estado = json.loads(estado)
            # self.estados = estado

        # GPIO.output(self.pinout[f"Luz_{0}"],msg['Luz_0'])
        # GPIO.output(self.pinout[f"Luz_{1}"],msg['Luz_1'])
        # if msg['Motor_0']=='parar':
        #     for i in range(4) : GPIO.output(self.pinout[f"Motor_0_p[{i}'"],False)
        # elif msg['Motor_0']=='abrir':
        #     for i in range(4) : GPIO.output(self.pinout[f"Motor_0_p[{i}'"],False)
        #     GPIO.output(self.pinout[f"Motor_0_p[{i}'"],True)
        #     await asyncio.sleep(vel_s)
        #     GPIO.output(self.pinout[f"Motor_0_p[{i}'"],False)
        #     await asyncio.sleep(vel_s/10)
        # elif msg['Motor_0']=='cerrar':




#######conexion websocket###############

async def connect(websocket):
    msg = await websocket.recv()
    msg = json.loads(msg)
    return msg
async def recieve(websocket,control_class):
    msg = await websocket.recv()
    msg = json.loads(msg)
    return msg
async def send(websocket, dict_data):
    await websocket.send(json.dumps(dict_data))
    await asyncio.sleep(1)
async def use_ws():
    uri = "ws://localhost:8000/ws/test/"
    async with websockets.connect(uri) as websocket:
        estado_inicial = await connect(websocket)
        # control_in = control_programa(websocket)
        control_out = Salidas(estado_inicial,websocket)

        # task_luz = asyncio.create_task(control_out.cambio_luz())
        # task_motor = asyncio.create_task(control_out.control_motor())
        # task_get = asyncio.create_task(control_out.recibir_instrucciones())
        while True: 
            # await send(websocket)
            await asyncio.gather(
                control_out.recibir_instrucciones(),
                control_out.cambio_luz(),
                control_out.control_motor(),
                # control_in.enviar_instrucciones()
                )
            
asyncio.get_event_loop().run_until_complete(use_ws())
