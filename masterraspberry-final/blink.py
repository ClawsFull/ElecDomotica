import RPi.GPIO as GPIO 
import state 
import fsm
import threading


#GPIO.setup(22, GPIO.OUT)
#GPIO.setup(23, GPIO.OUT)


def funcion_fsm_0(fsm,lectura):
        #print("Dentro del hilo0")
        #print(fsm.pause_machine())
        if fsm.pause_machine():
            #print("Ejecutando comandos de maquina0")
            fsm.read_inputs(lectura)
            #print("Se ingreso la lectura 0")
            fsm.update_state()
            #print("Se actualizo el estado0")
            fsm.update_output()
            #print("se calculo la salida0")
            #lista_de_salida=fsm0.write_output('return')
            #for tipo_variable, numero_variable in lista_de_salida.items():
                #GPIO.output(fsm0.__outputs[tipo_variable], numero_variable)
                #print(fsm0.get_actual_outputs(), numero_variable,fsm0.get_outputs_dict())
            #diseño para grabado en GPIO
            dict_variables_inter=list(fsm.get_actual_outputs().keys())
            for direccion_temp in dict_variables_inter:
                #print(fsm0.get_outputs_dict()[direccion_temp],fsm0.get_actual_outputs()[direccion_temp])
                GPIO.output(fsm.get_outputs_dict()[direccion_temp],fsm.get_actual_outputs()[direccion_temp])
            
                    
            if not fsm0.get_inter_state():
                fsm0.save_data()
                fsm0.reset_machine()
            
    
def funcion_fsm_1(fsm,lectura):
    #print("Dentro del hilo1")
    #print(fsm.pause_machine())
    if fsm.pause_machine():
        #print("Ejecutando comandos de maquina1")
        fsm.read_inputs(lectura)
        #print("Se ingreso la lectura1")
        fsm.update_state()
        #print("Se actualizo el estado1")
        fsm.update_output()
        #print("se calculo la salida1")
        #lista_de_salida=fsm0.write_output('return')
        #for tipo_variable, numero_variable in lista_de_salida.items():
            #GPIO.output(fsm0.__outputs[tipo_variable], numero_variable)
            #print(fsm0.get_actual_outputs(), numero_variable,fsm0.get_outputs_dict())
        #diseño para grabado en GPIO
        dict_variables_inter=list(fsm.get_actual_outputs().keys())
        for direccion_temp in dict_variables_inter:
            #print(fsm0.get_outputs_dict()[direccion_temp],fsm0.get_actual_outputs()[direccion_temp])
            GPIO.output(fsm.get_outputs_dict()[direccion_temp],fsm.get_actual_outputs()[direccion_temp])
                
        if not fsm1.get_inter_state():
            fsm1.save_data()
            fsm1.reset_machine()
            

            
    
GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.IN)
GPIO.setup(9, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

st0_1 = state.state_class([{"sa2":1}],        [1],  [0.01,0.1,1],0,"ST0",False)
st1_1 = state.state_class([{"sa2":0,"sa2":1}],[2,2],[0.01,0.5,1],1,"ST1",False)
st2_1 = state.state_class([{"sa2":1}],        [3],  [0.01,0.1,1],2,"ST2",False)
st3_1 = state.state_class([{"sa2":0,"sa2":1}],[0,0],[0.01,0.5,1],3,"ST3",False)
fsm1 = fsm.fsm_class({'sa2': 9},[st0_1, st1_1,st2_1,st3_1],{0: { 'v1': 1},1: { 'v1': 0},2: { 'v1': 0},3: { 'v1': 1}},{'v1': 27},0, 'FSM1')
st0 = state.state_class([{"sa1":1}],        [1],  [0.01,0.1,1],0,"ST0",False)
st1 = state.state_class([{"sa1":0,"sa1":1}],[2,2],[0.01,0.5,1],1,"ST1",False)
st2 = state.state_class([{"sa1":1}],        [3],  [0.01,0.1,1],2,"ST2",False)
st3 = state.state_class([{"sa1":0,"sa1":1}],[0,0],[0.01,0.5,1],3,"ST3",False)
fsm0 = fsm.fsm_class({'sa1': 10},[st0, st1,st2,st3],{0: { 'v1': 1},1: { 'v1': 0},2: { 'v1': 0},3: { 'v1': 1}},{'v1': 17},0, 'FSM0')
try:
    while True:
        sa1 = {'sa1':int(GPIO.input(10))}
        sa2 = {'sa2':int(GPIO.input(9))}
        #print("Se realizo lectura")
        t0 = threading.Thread(name='hilo0',target=funcion_fsm_0,args=(fsm0,sa1))
        t1 = threading.Thread(name='hilo1',target=funcion_fsm_1,args=(fsm1,sa2))
        #print("Se crearon los hilos")
        t0.start()
        #print("Se inicia el primer hilo")
        t1.start()
        #print("Se inicia el segundo hilo")
        t0.join()
        t1.join()
     
        #print("Se unen los hilos al hilo principal")
           
        
        
except KeyboardInterrupt :
    print("interrupcion por Keyboard")
    fsm0.save_data()
    fsm0.reset_machine()
    fsm1.save_data()
    fsm1.reset_machine()
finally:
    GPIO.cleanup()
    print("fin del programa")