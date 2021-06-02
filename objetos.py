import csv
import time
from random import randint

import RPi.GPIO as GPIO


# Administracion de los vfsm en raspberry pi 3
class rasp_class:
    """Clase para administra las maquina y la raspberry"""

    def __init__(self,
                 pins={},
                 machines=[]):
        self.__upine = pins
        self.__machine = machines
        self.__vpines = [7, 11, 12, 13, 15, 16, 18, 19,
                         21, 22, 23, 24, 26, 29, 31, 32,
                         33, 35, 36, 37, 38, 40]
        self.__date = 'Llamar os por fecha'
        self.__type_sensor = {'sa': 'dig',
                              'sb': 'dig+M',
                              'sc': 'alog',
                              'sd': 'alog+M'}
        # Todo elemento con +metodo tiene estructura de 'sbN':[pin,pin_aux]
        self.__all_inputs = {}
        self.__all_outputs = {}
        self.__data_inputs = {}
        self.__data_outputs = {}
        GPIO.setmode(GPIO.BCM)

        for aux_ej, aux_oa in self.__upine.items():
            if aux_ej[0: 1] == 'sa':
                self.__all_inputs[aux_ej] = aux_oa
                GPIO.setup(aux_oa, GPIO.IN)
            elif 'v' == aux_ej[0]:
                self.__all_outputs[aux_ej] = aux_oa
                GPIO.setup(aux_oa, GPIO.OUT)
            elif aux_ej[0: 1] == 'sb':
                GPIO.setup(aux_oa[0], GPIO.IN)
                GPIO.setup(aux_oa[1], GPIO.OUT)
            else:
                print('Pin ', aux_oa, ' no asignado!')

    def read_all_input(self):
        for aux_qp, aux_zu in self.__all_inputs.items():
            if aux_qp[0: 1] == 'sa':
                if GPIO.input(aux_zu):
                    self.__data_inputs[aux_qp] = 1
                else:
                    self.__data_inputs[aux_qp] = 0
            elif aux_qp[0: 1] == 'sb':
                GPIO.output(aux_zu[1], True)
                time.sleep(0.00001)
                GPIO.output(aux_zu[1], False)
                StartTime = time.time()
                StopTime = time.time()
                # save StartTime
                while GPIO.input(aux_zu[0]) == 0:
                    StartTime = time.time()
                # save time of arrival
                while GPIO.input(aux_zu[0]) == 1:
                    StopTime = time.time()
                # time difference between start and arrival
                TimeElapsed = StopTime - StartTime
                # multiply with the sonic speed (34300 cm/s)
                # and divide by 2, because there and back
                distance = (TimeElapsed * 34300) / 2
                if distance <= 10:
                    self.__data_inputs[aux_qp] = 1
                else:
                    self.__data_inputs[aux_qp] = 0
            elif aux_qp[0: 1] == 'sc':
                pass
            elif aux_qp[0: 1] == 'sd':
                pass
            else:
                pass

    def administrator_m(self):
        for aux_kl in self.__machine:
            if aux_kl.pause_machine():
                aux_kl.read_inputs(self.__data_inputs)
                aux_kl.update_state()
                aux_kl.update_output()
                for aux_mv, aux_rg in aux_kl.write_output('return'):
                    self.__data_outputs[aux_mv] = aux_rg
                if not aux_kl.get_inter_state():
                    aux_kl.save_data()
                    aux_kl.reset_machine()
        return None

    def write_all_output(self):
        for aux_dq, aux_jq in self.__data_outputs:
            GPIO.output(self.__all_outputs[aux_dq], aux_jq)
        return None

    def get_machines(self):

        return self.__machine

    def help(self):
        print('read_all_input,administrator_m,write_all_output,get_machines')
        return None


# Maquina de estados, Administrador de estados
class fsm_class:
    """Clase FSM """

    def __init__(self,
                 input_dict={},
                 states=[],
                 states_outputs={},
                 output_dict={},
                 inter_name=0,
                 public_name='FSM0'):
        #  Parametros fijos
        self.__inputs = input_dict
        self.__states = states
        self.__states_outputs = states_outputs
        self.__outputs = output_dict
        self.__inter_name = inter_name
        self.__public_name = public_name
        self.__numb_inputs = len(self.__inputs)
        self.__numb_states = len(self.__states)
        self.__numb_outputs = len(self.__outputs)
        #  Parametros temporales
        self.__inter_state = True
        self.__actual_input = dict.fromkeys(self.__inputs)
        self.__actual_state = 0
        self.__actual_output = dict.fromkeys(self.__inputs)
        self.__start_chronometer = time.time()
        self.__stop_chronometer = 0
        #  Otros
        numb_op = 0
        try:
            arch_op = 'op' + self.__public_name + '.csv'
            with open(arch_op, newline='') as file:
                reader = csv.reader(file, delimiter=',', quotechar=',')
                for row in reader:
                    numb_op = int(row[0])
                    print(numb_op)
        except Exception as new_arch:
            arch_op = 'op' + self.__public_name + '.csv'
            with open(arch_op, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([0])
            print('No existe archivo ', arch_op, ' Error:\n', new_arch)
        finally:
            with open(arch_op, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',',
                                    quotechar=',', quoting=csv.QUOTE_MINIMAL)
                aux_we = str(numb_op + 1)
                writer.writerow([aux_we])
                self.__numb_op = numb_op + 1

    #  Metodos
    #  Principal
    def read_inputs(self, inputs={}):
        """Obtener informacion de Sensores"""
        # se requiere de metodos de GPIO
        if inputs == {}:
            for aux_fi, aux_me in self.__inputs.items():
                self.__actual_input[aux_fi] = random_value()
        elif inputs != {}:
            for aux_fi, aux_me in self.__inputs.items():
                self.__actual_input[aux_fi] = inputs[aux_fi]
        return None

    def write_output(self, inst=0):
        """Escribir nuevas salidas"""
        # se requiere de metodos de GPIO
        for aux_pd, aux_wu in self.__actual_output.items():
            print('Salida: ', aux_pd, ' Valor: ', aux_wu,
                  ' Pin: ', self.__outputs[aux_pd],
                  ' Estado: ', self.__actual_state)
            print('')
        if inst == 0:
            return None
        else:
            return self.__actual_output

    def update_state(self):
        """Paso a siguiente estado"""
        aux_th = self.__actual_state
        aux_ga = self.__states[aux_th].get_next(self.__actual_input)
        self.__actual_state = aux_ga
        if self.__states[aux_ga].get_last():
            self.__inter_state = False
        return None

    def update_output(self):
        """Creacion de instruccciones de salida"""
        self.__start_chronometer = time.time()
        self.__actual_output = self.__states_outputs.get(self.__actual_state)
        return None

    def pause_machine(self):
        """Aun pausa todo el sistema"""
        self.__stop_chronometer = time.time()
        delta = self.__stop_chronometer - self.__start_chronometer
        if delta >= self.__states[self.__actual_state].get_time():
            self.__start_chronometer = 0
            self.__stop_chronometer = 0
            return True
        else:
            return False

    def reset_machine(self):
        """Resetea todos lo parametros temporales"""
        self.__inter_state = True
        self.__actual_state = 0
        self.__actual_output = []
        self.__actual_input = dict.fromkeys(self.__inputs)
        self.__start_chronometer = 0
        self.__stop_chronometer = 0
        for aux_uo in self.__states:
            aux_uo.reset_cycles()
            aux_uo.reset_time()
        return None

    def save_data(self):
        """Guardar datos en archivo externo"""
        data = []
        nombre_archivo = self.__public_name + '.csv'
        with open(nombre_archivo, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
            data.append('iteration')
            data.append(self.__numb_op)
            for aux_yb in self.__states:
                data.append(aux_yb.get_name())
                data.append(aux_yb.get_time())
                data.append(aux_yb.get_cycles())
            writer.writerow(data)
        return None

    #  Gets
    def get_numb_input(self):
        """Obtener numero de input"""
        return self.__numb_inputs

    def get_numb_output(self):
        """Obtener numero de salidas"""
        return self.__numb_outputs

    def get_inter_state(self):
        """Obtener si la maquina esta encendida"""
        return self.__inter_state

    def get_actual_inputs(self):
        """Obtener numero de input"""
        return self.__actual_input

    def get_actual_outputs(self):
        """Obtener numero de salidas"""
        return self.__actual_output

    def get_actual_state(self):
        """Obtener si la maquina esta encendida"""
        return self.__actual_state

    #  Sets
    def set_actual_state(self, numb):
        """Obtener la etapa actual del proceso"""
        if numb <= self.__numb_states and numb >= 0:
            self.__actual_state = numb
        return None

    def set_inter_state(self, new_state):
        """Encender o Apagar la maquina"""
        if type(new_state is bool):
            self.__inter_state = new_state
        return None

    # Otros
    def switch_inter_state(self):
        """Conmutar el estado de la maquina"""
        self.__inter_state = not self.__inter_state
        return None

    def help(self):
        print('read_inputs,write_output,update_state,update_output,'
              '\npause_machine,reset_machine,save_data,get_numb_input,'
              '\nget_numb_output,get_inter_state,get_actual_state,'
              '\nset_actual_state,set_inter_state,switch_inter_state')


# Estados
class state_class:
    def __init__(self,
                 input_dict=[],
                 output_dict=[],
                 time=[0.01, 0.5, 1],
                 inter_name=0,
                 public_name='ST0',
                 last_state=False):
        """Clase de Estado: """
        #  Parametros fijos
        self.__inputs = input_dict
        self.__outputs = output_dict
        self.__time = time
        self.__inter_name = inter_name
        self.__public_name = public_name
        self.__numb_inputs = len(self.__inputs)
        self.__numb_outputs = len(self.__outputs)
        self.__final = last_state
        #  Parametros temporales
        self.__actual_time = self.__time[1]
        self.__cycles = 0

    # Metodos
    #  Gets
    def get_next(self, inputs):
        """Obtener el siguiente estado"""
        self.__cycles += 1
        for dictio in self.__inputs:
            aux_sf = 1
            for aux_da, aux_gj in dictio.items():
                if inputs[aux_da] == aux_gj:
                    aux_sf = aux_sf * 1
                else:
                    aux_sf = aux_sf * 0
            if aux_sf == 1:
                return self.__outputs[self.__inputs.index(dictio)]
        return self.__inter_name

    def get_name(self):
        """Obtener el nombre del estado"""
        return self.__public_name

    def get_time(self):
        """Obtener el tiempo operacion"""
        return self.__actual_time

    def get_cycles(self):
        """Obtener el numero de ciclos de operacion"""
        return self.__cycles

    def get_numb_input(self):
        """Obtener numero de entradas"""
        return self.__numb_inputs

    def get_numb_output(self):
        """Obtener numero de salidas"""
        return self.__numb_outputs

    def get_input_list(self):
        """Obtener lista de entradas validas"""
        return self.__inputs

    def get_last(self):
        """Obtiene si es el ultimo estado o no"""
        return self.__final

    #  Sets
    def set_min_time(self, input_time):
        """Fijar tiempo minimo de operacion"""
        if input_time >= 0.01 and input_time <= self.__time[1]:
            self.__time[0] = input_time
        else:
            print('Error input')
        return None

    def set_base_time(self, input_time):
        """Fijar tiempo base de operacion"""
        if input_time >= 0.01 and input_time <= self.__time[2]:
            self.__time[1] = input_time
        else:
            print('Error input')
        return None

    def set_max_time(self, input_time):
        """Fijar tiempo maximo de operacion"""
        if input_time >= self.__time[1]:
            self.__time[2] = input_time
        else:
            print('Error input')
        return None

    def set_time(self, input_time):
        """Fijar nuevo tiempo de operacion"""
        if input_time >= self.__time[0] and input_time:
            self.__actual_time = input_time
        else:
            print('Error input')
        return None

    #  Otros
    def reset_cycles(self):
        """Reiniciar el conteo de ciclos de operacion"""
        self.__cycles = 0
        return None

    def reset_time(self):
        """Reinicio de tiempo de operacion a el tiempo base"""
        self.__actual_time = self.__time[1]
        return None

    def help(self):
        print(
            'get_next,get_name,get_time,get_cycles,get_numb_input,'
            '\nget_numb_output,get_input_list,get_last,set_min_time,'
            '\nset_base_time,set_max_time,set_time,reset_cycles,reset_time')
