import serial 
import time
import json
import platform


class com_serial :
    """Class de objeto que facilita la comunicacion Serial """
    
    def __init__(self,dir_com = '', time_input = '', inter_name = 0, public_name = 'COM_ARDUINO0', flag = False ):
        """Clase de Comunicacion Serial para Python: """
        #  Parametros fijos
        self.__platform = platform.system() #Llamado para oiptener el nombre del sistema en el que se opera
        if (dir_com=='' and self.__platform=="Linux"):
            self.__dirCom = '/dev/tyyUSB0' 
        elif (dir_com!=''):
            self.__dirCom = dir_com 
        else: 
            self.__dirCom = 'Error_NONE_DIR'
        self.__inter_name = inter_name # Numero interno para operar multiples administradores de canales USB 
        self.__public_name = public_name # Nombre para hacer referencia la objeto creado, como en prints o hacer referencias en archivos externos
        self.__flag = flag if str(type(flag)) != "<class 'bool'>" else False
        self.__channel = [] #Ubicacion de guardado para alojamiento para uno o mas canales
        self.__dict_arduino = {"L298N":"F+0","A0":0,"A1":0,"A2":0}
        self.__workingChannel = [False]
        self.__dict_com = {0 :"RA0" , # 0-59 for request Analog Read or Digital Read pin m
                        1 :"RA1" , 
                        2 :"RA2" ,
                        3 :"RA3" ,
                        4 :"RA4" ,
                        5 :"RA5" ,
                        6 :"RA6" ,
                        7 :"RA7" ,
                        8 :"RA8" ,
                        9 :"RA9" ,
                        10:"RA10" ,
                        11:"RA11" ,
                        12:"RA12" ,
                        13:"RA13" ,
                        14:"RA14" ,
                        15:"RA15" ,
                        40:"on"  , # codigo de prueba 1 
                        41:"off" , # codigo de prueba 2
                        60:"F+0" , # 60-xx for functions or complex comands
                        61:"F+1" ,
                        62:"F+2" ,
                        63:"F+4" ,
                        64:"F+8" ,
                        65:"F+16" ,
                        66:"F+32" ,
                        67:"F+64" ,   # Vuelta 1/8 sentido horario
                        68:"F+128" ,  # Vuelta 1/4 sentido horario
                        69:"F+256" ,  # Vuelta 1/2 sentido horario
                        70:"F+512" ,  # Vuelta 1 sentido horario
                        71:"F+1024" , # Vuelta 2 sentido horario
                        72:"F+2048" , # Vuelta 4 sentido horario
                        73:"F+4096" , # Vuelta 8 sentido horario
                        80:"F-0" , # 60-xx for functions or complex comands
                        81:"F-1" ,    # Vuelta 1/512 sentido horario
                        82:"F-2" ,    # Vuelta 1/256 sentido horario
                        83:"F-4" ,    # Vuelta 1/128 sentido horario
                        84:"F-8" ,    # Vuelta 1/64 sentido horario
                        85:"F-16" ,   # Vuelta 1/32 sentido horario
                        86:"F-32" ,   # Vuelta 1/16 sentido horario
                        87:"F-64" ,   # Vuelta 1/8 sentido horario
                        88:"F-128" ,  # Vuelta 1/4 sentido horario
                        89:"F-256" ,  # Vuelta 1/2 sentido horario
                        90:"F-512" ,  # Vuelta 1 sentido horario
                        91:"F-1024" , # Vuelta 2 sentido horario
                        92:"F-2048" , # Vuelta 4 sentido horario
                        93:"F-4096" } # Vuelta 8 sentido horario
        #  Parametros temporales
        self.__time_init = time_input if time_input != '' else time.ctime() #Fecha de creacion del objeto
        self.__time_start = '0' #Fecha de inicio de comunicacion
        self.__time_finish = '0' # Fecha de fin de comunicacion
        self.__cycles = 0  #Numero de mensajes enviados
    # Metodos
    def init_com(self,canal=0,baud=9600):
        """Metodo de Iniciar Comunicacion"""
        try:
            arduino_channel = serial.Serial(self.__dirCom,baudrate=baud,timeout=0.1) # Se crea y abre el canal de comunicacion
            self.__channel.append(arduino_channel) # Se guarda el canal dentro de una lista de canales disponibles
            self.__channel[canal].flushInput() #limpiar el buffer de entrada del canal
            print(self.__channel[canal])
            print("Inicio ", end="")
            print(str(self.__channel[canal].name))
        except SerialException as SerExp:
            print(SerExp)
        finally:
                self.__cycles = 0
        return None

    def send_comand(self, data, mode = 'a',canal=0):
        """Metodo de Enviar Mensaje Serial"""
        if self.__cycles == 0:
            self.__time_start = time.ctime()
        if mode == 'a':  # Si se opera con el metodo 'a' se ingresan los datos directamente desde la llamada del metodo
            dato = data
        elif mode == 'b': # Si se opera con el metodo 'b' se ingresan los datos desde Terminal
            dato = input('Input>>> ')
        elif mode == 'c': # Si se opera con el metodo 'c' solo se ingresa un numero de indice del diccionario de comunicacion
            dato = self.__dict_com[data]
            #print(dato)
        try:    
            dato += '\n'
            for bin_data in dato:
                self.__channel[canal].write(bin_data.encode())
                #print(bin_data.encode())
            if dato[0:1] == "F*":
                self.__workingChannel[canal]=False
        except serial.serialutil.SerialException:
            print('Puerto ocupado')
        #finally:
            #print('Mensaje enviado')
        return None

    def recive (self,canal=0):
        """Metodo de recepcion de Mensajes"""
        try:
            raw_string_b = self.__channel[canal].readline() # Se intenta Leer la ultima linea hasta el salto de linea en el buffer
            raw_string_s = raw_string_b.decode('utf-8') # Se decifra el mensaje en formato utf-8
            if(raw_string_s.index("}")>=0 and raw_string_s.index("{")==0): # Si el mensaje est[a] en formato json entonces 
                raw_string_s = raw_string_s[0:raw_string_s.index("}")+1]
                raw_string_j = json.loads(raw_string_s) # Transforma el mensaje en bruto a uno objeto diccionario
                # entrada general
                #print(raw_string_j)
                list_values = list(raw_string_j.values())
                print(list_values)
                if self.__workingChannel[canal]:
                    if (list_values[0]=="L298N" and list_values[1][-1]=='f'):
                        list_values[1]=list_values[1][:-1]
                    if (list_values[0]=="L298N" and list_values[1][-1]=='c' ):
                        print(list_values[1])
                        list_values[1]=list_values[1][:-1]
                        print(list_values[1])
                        self.__workingChannel[canal]=False
                    if (list_values[0]=="L298N" and list_values[1][-6:-1]=='RA0RA1'):
                        print(list_values[1])
                        list_values[1]=list_values[1][:-6]
                        print(list_values[1])
                        self.__workingChannel[canal]=False
                if (list_values[0]=="L298N" and list_values[1][-1]!='f' and list_values[1][-1]!='c' ):
                    self.__workingChannel[canal]=True
                self.__dict_arduino.update({list_values[0]:list_values[1]}) # Crea un diccionario con la informacion actializada de los sensores y motores
                print(f'{"Variable":15}: {"Valor":15}')
                print(f'{"Canal":15}: {self.__workingChannel[canal]:<15}')
                for data , value in self.__dict_arduino.items(): # Se muestra en pantalla los elementos 
                    print(f'{data:<15}: {value:<10} ')

            else:
                print("error/ no } found.")
        except Exception as name_exception:
            #print("Exception occurred, somthing wrong...")
            #print("Error: ",name_exception)
            pass
    def close_com(self,canal=0):
        """Metodo de cierre de Canal Serial"""
        # Si se abri[o] un canal de comunicacion es obligatorio cerrarlo pues este quedar[a] incomunicado para otras aplicaciones
        try:
            if self.__channel[canal].isOpen(): #Si el puerto aun est[a] abierto
                self.__channel[canal].close()  # Se cierra el canal 
                self.__channel[canal].flushInput() # Se limpia el buffer de entrada
                self.__channel[canal].flushOutput() # Se limpia el buffer de Salida
                # Seccion reserbada para el guardado de datos a largo plazo
                # Fin de seccion
                self.__channel.pop(canal) # Se elimina el canal selecionado
                print('Serial Port Closed')
        except Exception as error_desconocido:
            print(error_desconocido)
        finally:
            self.__time_finish = time.ctime() # Se guarda cuando fue la ultima coneccion realizada dentro del administrador de canales de comunicacion serial
            print(self.__channel)
            print(self.__time_start)
            print(self.__time_finish)
    
    # Gets
    def get_channel(self,canal=0):
        """Metodo Get para obtener los canales disponibles en el administrador de canales"""
        return self.__channel[canal]
    def get_dict_comunication():
        """Metodo Get para obtener los objetos y sus estados actuales"""
        return self.__dict_arduino