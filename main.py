# Title: "Virtual Finite State Machine for Raspberry Pi 3B"
# Version: 0.20200413
# Description: -*- coding: utf-8 -*-
# Created By: Camilo Alfonso Santibanez Chacon
# Created: 2020/03/10
# Last Modified: 2020/04/12
# Based on:
# * https://www.raspberrypi-spy.co.uk/2013/01/ultrasonic
#   -distance-measurement-using-python-part-2/
# * https://projects.raspberrypi.org/en/projects/physical
#   -computing
# * https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
# * https://docs.python.org/3/library/csv.html
# * https://docs.python.org/3/library/time.html
# * https://docs.python.org/3/library/random.html
# * http://www.stateworks.com/active/download/wagf92-software-engineering.pdf

from rasp import *
from fsm import *
from state import *

def main():
    # Creacion de todos los objetos

    st0 = state_class([{'sa3': 0}, {'sa3': 1}],
                      [1, 1], [0.01, 0.1, 1], 0, 'ST0',
                      False)
    st1 = state_class([{'sb1': 1}],
                      [2], [0.01, 0.1, 1], 1, 'ST1',
                      False)
    st2 = state_class([{'sa3': 1}, {'sa5': 1}],
                      [3, 17], [0.01, 0.1, 1], 2, 'ST2',
                      False)
    st3 = state_class([{'sa3': 0}, {'sa3': 1}],
                      [4, 4], [0.01, 0.1, 1], 3, 'ST3',
                      False)
    st4 = state_class([{'sa3': 0}, {'sa3': 1}],
                      [5, 5], [0.01, 3, 1], 4, 'ST4',
                      False)
    st5 = state_class([{'sa3': 0}, {'sa3': 1}],
                      [6, 6], [0.01, 1, 1], 5, 'ST5',
                      False)
    st6 = state_class([{'sa3': 0}, {'sa3': 1}],
                      [7, 7], [0.01, 3, 1], 6, 'ST6',
                      False)
    st7 = state_class([{'sa3': 0}, {'sa3': 1}, {'sa5': 1}],
                      [8, 8, 18], [0.01, 1, 1], 7, 'ST7',
                      False)
    st8 = state_class([{'sa5': 0}, {'sa5': 1}],
                      [9, 19], [0.01, 0.7, 1], 8, 'ST8',
                      False)
    st9 = state_class([{'sa5': 0, 'sa2': 0}, {'sa5': 1},
                       {'sa5': 0, 'sa2': 1}],
                      [8, 20, 10], [0.01, 0.7, 1], 9, 'ST9',
                      False)
    st10 = state_class([{'sa5': 0}, {'sa5': 1}],
                       [11, 21], [0.01, 0.5, 1], 10, 'ST10',
                       False)
    st11 = state_class([{'sa3': 0}, {'sa3': 1}],
                       [12, 12], [0.01, 0.2, 1], 11, 'ST11',
                       False)
    st12 = state_class([{'sa3': 0}, {'sa3': 1}],
                       [13, 13], [0.01, 1, 1], 12, 'ST12',
                       False)
    st13 = state_class([{'sa3': 0}, {'sa3': 1}],
                       [14, 14], [0.01, 0.1, 1], 13, 'ST13',
                       False)
    st14 = state_class([{'sa4': 1}, {'sa4': 0, 'sa5': 1}],
                       [15, 22], [0.01, 0.1, 1], 14, 'ST14',
                       False)
    st15 = state_class([{'sb1': 0}, {'sb1': 1, 'sa5': 1}],
                       [16, 23], [0.01, 7, 1], 15, 'ST15',
                       False)
    st16 = state_class([],
                       [], [0.01, 1, 1], 16, 'ST16',
                       True)
    st17 = state_class([{'sa5': 1}],
                       [2], [0.01, 7, 1], 17, 'ST17',
                       False)
    st18 = state_class([{'sa5': 1}],
                       [7], [0.01, 7, 1], 18, 'ST18',
                       False)
    st19 = state_class([{'sa5': 1}],
                       [9], [0.01, 7, 1], 19, 'ST19',
                       False)
    st20 = state_class([{'sa5': 1}],
                       [8], [0.01, 7, 1], 20, 'ST20',
                       False)
    st21 = state_class([{'sa5': 1}],
                       [10], [0.01, 7, 1], 21, 'ST21',
                       False)
    fsm0 = fsm_class({'sb1': [16, 18], 'sa2': 7, 'sa3': 11,
                      'sa4': 13, 'sa5': 22},
                     [st0, st1, st2, st3, st4, st5,
                      st6, st7, st8, st9, st10, st11, st12,
                      st13, st14, st15, st16, st17, st18,
                      st19, st20, st21],
                     # asegurar la botella
                     {0: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      1: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      2: {'v5': 0, 'v4': 1, 'v3': 0, 'v2': 0, 'v1': 0},
                      # inicio de llenado
                      3: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      # barrido
                      4: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 1},
                      5: {'v5': 0, 'v4': 0, 'v3': 1, 'v2': 0, 'v1': 1},
                      6: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 1},
                      7: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      # Liberacion de la cerveza
                      8: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 1, 'v1': 0},
                      9: {'v5': 0, 'v4': 0, 'v3': 1, 'v2': 1, 'v1': 0},
                      # Liberacion de CO_2 sobrante
                      10: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      11: {'v5': 0, 'v4': 0, 'v3': 1, 'v2': 0, 'v1': 0},
                      # Fin de llenado
                      12: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      # Liberacion de la botella
                      13: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      14: {'v5': 1, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      15: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      # Fin del proceso
                      16: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      # Pausas
                      17: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      18: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      19: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      20: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0},
                      21: {'v5': 0, 'v4': 0, 'v3': 0, 'v2': 0, 'v1': 0}},
                     {'v1': 21, 'v2': 23, 'v3': 29, 'v4': 15, 'v5': 19},
                     0, 'FSM0')

    administrador_vfsm = rasp_class({'sb1': [16, 18], 'sa2': 7, 'sa3': 11,
                                     'sa4': 13, 'sa5': 22, 'v1': 21, 'v2': 23,
                                     'v3': 29, 'v4': 15, 'v5': 19},
                                    [fsm0])
    # Bucle Principal

    while True:
        administrador_vfsm.read_all_input()
        administrador_vfsm.administrator_m()
        administrador_vfsm.write_all_output()


if __name__ == '__main__':
    main()
