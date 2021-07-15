
int val = 0; // Se crea la variable val para leer los datos

void setup()
{
  pinMode(A0, INPUT); // Se define el pin analogo 0 como entrada
  Serial.begin(9600); // Inicializo el puerto serial a 9600 baudios
}

void loop()
{
  val = analogRead(A0);  // read the input pin
  Serial.println(val); // se envia mediante comunicacion serial el valor leido
  delay(250);  // se deja un tiempo para disminuir el consumo
}
