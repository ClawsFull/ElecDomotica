import serial
entrada_serial = input('Puerto USB a usar >> ')
if entrada_serial == "" :
    entrada_serial = 'COM4'
elif entrada_serial== "pi":
    entrada_serial = '/dev/ttyUSB0'

while True:
    try:   
        ardNano = serial.Serial(entrada_serial,9600)
        print("Inicio ", end="")
        print(ardNano.name)
        dato = input('Input >> ')+'\n'
        for bin_data in dato:
            ardNano.write(bin_data.encode())
            print(bin_data.encode())
        
        ardNano.close()

    #except serial.serialutil.SerialException:
    #    print('Puerto ocupado')
    finally:
        print('Fin de la comunicacion')
        input ('')