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
