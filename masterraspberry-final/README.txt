Contenido de la carpeta:
- blink.py	--------------------------------------	Código principal
- compruebas.py	----------------------------------	Código de ejemplo de Comunicación 
- fsm.py	--------------------------------------	Código de estructura para Finite State Machine
- FSM0.csv	--------------------------------------	Archivo con el registro de operación de los tiempos de operación y veces que se usó un estado dentro de la máquina de estados finitos, en este caso la maquina FSM0
- FSM1.csv	--------------------------------------	Archivo de almacenamiento similar al anterior
- opFSM0.csv	----------------------------------	Archivo de respaldo que registra las veces que se inició la máquina de estado, es decir, las inicializaciones de los objetos llamados FSM0, si no existe con anterioridad, este archivo se crea de forma automática.
- opFSM1.csv	----------------------------------	Archivo de respaldo con el mismo funcionamiento que el anterior.
- serialComunication.py		----------------------	Código que encapsula la API pyserial de modo que se cree un objeto capaz de administrar múltiples canales de comunicación serial y adaptado para interpretar y almacenar la información de los sensores y motor.
- state.py	--------------------------------------	Código de estructura para los estados de la máquina de estados finitos

Descripción de la carpeta:
La carpeta 'masterraspberry-final' corresponde al código de
funcionamiento de Ampolletas con Motor y sensores conectados
a Arduino sin requerir conexión a internet, esta parte del 
proyecto buscando la mayor robustez posible dentro de las co-
nexiones como del funcionamiento en si del sistema. Es por 
esto por lo que el sistema está lo más descentralizado posible
de la computadora principal, que en este caso es la Raspberry
Pi 3+. A esta misma se le conectan directamente por los pi-
nes GPIO un módulo Relé con optoacopladores por lo que es 
seguro su uso, de igual manera se usan botones directamente 
a la Raspberry pues su manejo es seguro. Para el uso de múlti-
ples sensores análogos se optó por el uso de Arduino y el con-
trol del motor al ser un motor paso al paso el que se implementó,
es posible usar el mismo Arduino para el control y uso mediado
por un driver “Uln2003” que admite una alimentación indepen-
diente de 5V a 12V, o un driver “L298N” que admite un rango de
voltajes de entre 5V a 35V, una variante en miniatura basada en
el driver “L298N” que admite de 2V a 10V también una opción via-
ble. Al circuito del Arduino se le suman dos sensores LDR para la
detección de luz fuera de la casa por medio de una ventana 
(sensor A1) y un sensor interno apuntando a la ampolleta prin-
cipal de la habitación (sensor A0). Es necesario que estos sen-
sores se encuentren como periféricos debido a su posición en 
una pared en altura, pues dado el caso que se conecten directa-
mente al sistema requieren de un circuito extra de conversión 
análogo digital que usaría un gran numero de pines del GPIO de 
la Raspberry y generando perdidas o alteración de datos si su 
conexión no es correcta. Por lo tanto, la solución basada en co-
municación serial es la óptima en este caso, permite un movi-
miento holgado de la Raspberry opción necesaria si se quiere 
realizar un monitoreo remoto y una conexión estable por ethernet 
es requerida, además permite un fácil acoplamiento de periféricos. 
Para esta versión del proyecto es requerido que se use la versión 
de slaveArduino.ino o slaveArduinoConsole.ino para dar uso de la 
comunicación fullduplex por puerto serial, para los requisitos 
del Arduino: se necesita de cualquier Arduino que cuente con un 
transformador uart/serial o que admita uno por circuito externo, 
conexión a alimentación externa por batería para sensores y pan-
talla, si se opta por agregar una con la versión consola del pro-
grama para Arduino, para más detalles remitirse a los códigos 
respectivos.
