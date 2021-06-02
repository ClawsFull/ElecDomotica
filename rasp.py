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


