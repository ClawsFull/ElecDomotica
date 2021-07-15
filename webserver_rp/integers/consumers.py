import json
#Se importan websockets en modo asincrono
from channels.generic.websocket import AsyncWebsocketConsumer
#funciones basicas de debug para mostrar lo que esta ocurriendo
def apgar_luz(luz):
    print('apagar')
    print(luz)
def encender_luz(luz):
    print('encender')
    print(luz)
#funcion principal de la aplicacion websocket
class WSConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]
    #funcion para enviar un mensaje a todos los clientes
    async def broadcast_send(self, event):
        await self.send(text_data=event['message'])
    async def connect(self):
        #definir grupo general
        self.group = "broadcast"
        #agregar el nuevo cliente al grupo general
        await self.channel_layer.group_add(
                    self.group,
                    self.channel_name
                )
        #aceptar la conexion entrante
        await self.accept()
        try:
            # envia el estado a todos los clientes 
            await self.channel_layer.group_send(
                        self.group,
                        {
                            "type": "broadcast_send",
                            "message": json.dumps(self.estados),
                        },
                    )
        except:
            #define los estados iniciales cuando se genera la primera conexion
            self.estados = {
                'Luz_0':False,
                'Luz_1':False,
                }
            # envia el estado a todos los clientes 
            await self.channel_layer.group_send(
                        self.group,
                        {
                            "type": "broadcast_send",
                            "message": json.dumps(self.estados),
                        },
                    )
    async def receive(self, text_data):
        #se obtiene el mensaje
        data_estados = json.loads(text_data)
        #se obtienen las llaves que tenga el mensaje
        data_key = [key for key in data_estados]
        #cambia los estados segun el mensaje
        for data in data_key:
            if data_estados[data]=='cambio':
                data_estados[data]=not(self.estados[data])
            self.estados[data] = data_estados[data]
        #envia el nuevo estado a todos los clientes
        await self.channel_layer.group_send(
                    self.group,
                    {
                        "type": "broadcast_send",
                        "message": json.dumps(self.estados),
                    },
                )
        # debug, solo muestra los datos en consola
        for data in data_key:
            if data=='Luz_0' and self.estados[data]==False:
                apgar_luz(data)
            elif data=='Luz_1' and self.estados[data]==False:
                apgar_luz(data)
            elif data=='Luz_0' and self.estados[data]==True:
                encender_luz(data)
            elif data=='Luz_1' and self.estados[data]==True:
                encender_luz(data)