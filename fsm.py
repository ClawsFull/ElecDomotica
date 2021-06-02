import csv
import time


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
