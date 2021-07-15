// Version bidirecional de comunicacion serial, el arduino responde segun una solicitud
// Las solicitudes pueden ser 3 tipos:
//  1- 'on' , 'off' : Estas instrucciones controlan el LED de prueba (LED_BUILTIN)
//  2- 'RAx': El comando Request AnalogRead del pin x (se requiere de un pin habilitado y unas lineas de condigo extra en fun_read_led())
//  Ejemplo del linea extra de codigo:
//  
//  else if (inputString.equals("RA4"))
//  {
//    json_data = "{\"Sensor_id\":\"A4\",\"Value\":" + (String) analogRead(A4) + "}";
//    Serial.println(json_data);
//  }
//
//  3- 'F+xxx', 'F-xxx', 'F*' : Estos dos tipos de comandos solicitan la rotacion positiva para '+' 
//                           y negativa para '-'. Donde xxx es el numero de rotaciones totales a ejecutar por el motor
//                           El comando 'F*' fuerza el reset de las variables internas relacionadas con el motor.
// 

String inputString = ""; // Cadena para guardar el comando recibido
String inputStringNum = "";
String json_data = ""; // Cadena pata emitir
bool stringEnd = false; // Flag Reception
int pRotationEnd = 0; // Flag Rotation positiva
int * dir_pRotationEnd = & pRotationEnd; // Direccion en memoria de la variable booleana
int nRotationEnd = 0; // Flag Rotation negativa
int * dir_nRotationEnd = & nRotationEnd; // Direccion en memoria de la variable booleana
int IN1 = 2; // pin digital 8 de Arduino a IN1 de modulo controlador
int IN2 = 3; // pin digital 9 de Arduino a IN2 de modulo controlador
int IN3 = 4; // pin digital 10 de Arduino a IN3 de modulo controlador
int IN4 = 5; // pin digital 11 de Arduino a IN4 de modulo controlador
int demora = 20; // demora entre pasos siempre mayor a 20ms y no se admite menor a 10ms.
int IN_default = 0;
int rNum = 0; // numero de rotaciones ingresado
int rNumA = 0;
int stepN = 0; // numero de pasos fijos para pasar por la matriz
int stepM[4][4] = // matriz (array bidimensional) con la secuencia de pasos
{
  {
    1, 0, 0, 0
  },
  {
    0, 1, 0, 0
  },
  {
    0, 0, 1, 0
  },
  {
    0, 0, 0, 1
  }
};

/*
int stepM[4][4] = // matriz (array bidimensional) con la secuencia de pasos log inver
{
  {
    0, 1, 1, 1
  },
  {
    1, 0, 1, 1
  },
  {
    1, 1, 0, 1
  },
  {
    1, 1, 1, 0
  }
};
*/

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  pinMode(IN1, OUTPUT); // todos los pines como salida
  digitalWrite(IN1, IN_default);
  pinMode(IN2, OUTPUT);
  digitalWrite(IN2, IN_default);
  pinMode(IN3, OUTPUT);
  digitalWrite(IN3, IN_default);
  pinMode(IN4, OUTPUT);
  digitalWrite(IN4, IN_default);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  Serial.begin(38400); // Inicializo el puerto serial a 9600 baudios normalmente
  inputString.reserve(200);
  delay(100);
}

void loop()
{
  if (stringEnd || (((bool) pRotationEnd == true) || ((bool) nRotationEnd == true)))
  {
    // El Mensaje fue recibido
    // Inicializacion de la entrada String
    if (stringEnd)
    {
      // Codigo de mensaje recibido
      if ((rNum == 0) && (( pRotationEnd == 1) ^ ( nRotationEnd == 1)))
      {
        String inputStringNum = inputString.substring(2);
        //Serial.print("En ejecucion >>> ");
        //Serial.println(inputStringNum);
        rNum = inputStringNum.toInt();
        if (rNum<0)
        {
          rNum = -rNum;
        }
        //Serial.print("Num Rotacion > ");
        //Serial.println(rNum);
        //Serial.println(inputString);
        if ((inputString[0]=='F')&&((inputString[1]=='+')||(inputString[1]=='-')))
        {
          //Serial.println(inputString[0]);
          if(inputString[1]=='+')
          {
            // se detecto correctamente el primer F+xxxx
            //Serial.println(inputString);
            //Serial.println("F +");
            json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"" + inputString + "\" }";
            Serial.println(json_data);
          }
          else if(inputString[1]=='-')
          {
            // se detecto correctamente el primer F-xxxx
            //Serial.println(inputString);
            //Serial.println("F -");
            json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"" + inputString + "\" }";
            Serial.println(json_data);
          }
        }
      }
      // si el primer elemento del mensaje es "F+" o "F-" y ya rNum != 0
      else if ((rNumA !=0) && (((bool) pRotationEnd == true) && ((bool) nRotationEnd == false)))
      {//    Ejecutar codigo de mensaje trabajo pendiente
        fun_read_led();
        inputString = "F+" + String( rNumA ) + "f";
        //Serial.print("En ejecucion : ");
        //Serial.println(inputString);
        json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"" + inputString + "\" }";
        Serial.println(json_data);
      }
      else if ((rNumA!=0) && (((bool) pRotationEnd == false) && ((bool) nRotationEnd == true))) 
      {//    Ejecutar codigo de mensaje trabajo pendiente
        fun_read_led();
        inputString = "F-" + String( rNumA ) + "f";
        //Serial.print("En ejecucion : "); 
        //Serial.println(inputString);
        json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"" + inputString + "\" }";
        Serial.println(json_data);
      }
      
      ///////////////////////////////////////////////////////////////////////////
      //Serial.println("TOP CODE");
      //delay(20); 
      ///////////////////////////////////////////////////////////////////////////
      
      // Ejecucion del Comando Entrante Sensores y LED
      fun_read_led();                                                                                                                                                                                           
    }

    /////////////////////////////////////////////////////////////////////
    //Serial.println("MID CODE");
    delay(10);   
    /////////////////////////////////////////////////////////////////////
    
    if(( pRotationEnd == 1) || ( nRotationEnd == 1))
    {
      // Codigo de motor

      /*
      Serial.print("pRoE > ");
      Serial.print(pRotationEnd);
      Serial.print(" ,nRoE > ");
      Serial.println(nRotationEnd);
      */

      // si error de doble encendido
      if ((pRotationEnd == 1) && (nRotationEnd == 1))
      {
        //    Ejecutar linea de error
        //Serial.println("Error de ejecution de F+-N");
        //Serial.print("Rota P > ");
        //Serial.println(pRotationEnd);
        //Serial.print("Rota N > ");
        //Serial.println(nRotationEnd);
        //Serial.print("rNum > ");
        //Serial.println(rNum);
        //Serial.print("rNumA > ");
        //Serial.println(rNumA);
        //Serial.print("inputString > ");
        //Serial.println(inputString);
        //Serial.print("inputStringNum > ");
        //Serial.println(inputStringNum);
        json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"Error_F+-\" }";
        Serial.println(json_data);
        json_data = "{\"VAR_id\":\"pRotationEnd\",\"Value\": \"" + (String)pRotationEnd + "\" }";
        Serial.println(json_data);
        json_data = "{\"VAR_id\":\"nRotationEnd\",\"Value\": \"" + (String)nRotationEnd + "\" }";
        Serial.println(json_data);
        json_data = "{\"VAR_id\":\"rNum\",\"Value\": \"" + (String)rNum + "\" }";
        Serial.println(json_data);
        json_data = "{\"VAR_id\":\"rNumA\",\"Value\": \"" + (String)rNumA + "\" }";
        Serial.println(json_data);
        json_data = "{\"VAR_id\":\"inputString\",\"Value\": \"" + (String)inputString + "\" }";
        Serial.println(json_data);
        json_data = "{\"VAR_id\":\"inputStringNum\",\"Value\": \"" + (String)inputStringNum + "\" }";
        Serial.println(json_data); // 1 salida de Motor + 6 salidas de Variables
        pRotationEnd =0;
        nRotationEnd =0;
      }
    
      // si pasos hacia adelante 
      else if ((pRotationEnd == 1) && ( nRotationEnd == 0))
      {
        //    Ejecutar secuencia +
        /*
        Serial.print("En ejecucion : ");
        Serial.println(rNumA);
        Serial.print("pRoE >> ");
        Serial.print(pRotationEnd);
        Serial.print(" ,nRoE >> ");
        Serial.println(nRotationEnd);
        */
        if (rNumA < rNum)
        {
          for (stepN = 0; stepN < 4; stepN++)
          // bucle recorre la matriz de a una fila por vez
          {
            // para obtener los valores logicos a aplicar
            digitalWrite(IN1, stepM[stepN][0]); // a IN1, IN2, IN3 e IN4
            digitalWrite(IN2, stepM[stepN][1]);
            digitalWrite(IN3, stepM[stepN][2]);
            digitalWrite(IN4, stepM[stepN][3]);
            delay(demora);
          }
          stepN = 0; // Limpiar numero auxiliar de conteo
          rNumA = rNumA + 1;
          //Serial.print("Refresh rNumA : ");
          //Serial.println(rNumA);
        }
        else
        {
          pRotationEnd = 0;
          //Serial.println("Fin de la Rotacion p");
          inputString = "F+" + String( rNumA ) + "c";
          json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"" + inputString + "\" }";
          Serial.println(json_data);
        }
      }
        
      // si pasos hacia atras
      else if (( pRotationEnd == 0) && (nRotationEnd == 1))
      {
        //    Ejecutar secuencia -
        //Serial.print("En ejecucion : ");
        //Serial.println(rNumA);
        //Serial.print("pRoE >> ");
        //Serial.print(pRotationEnd);
        //Serial.print(" ,nRoE >> ");
        //Serial.println(nRotationEnd);
        if (rNumA < rNum)
        {
          for (stepN = 3; stepN >= 0; stepN--)
          // bucle recorre la matriz de a una fila por vez
          {
            // para obtener los valores logicos a aplicar
            digitalWrite(IN1, stepM[stepN][0]); // a IN1, IN2, IN3 e IN4
            digitalWrite(IN2, stepM[stepN][1]);
            digitalWrite(IN3, stepM[stepN][2]);
            digitalWrite(IN4, stepM[stepN][3]);
            delay(demora);
          }
          stepN = 0; // Limpiar numero auxiliar de conteo
          rNumA = rNumA + 1;
          //Serial.print("Refresh rNumA : ");
          //Serial.println(rNumA);
        }
        else
        {
          nRotationEnd = 0;
          //Serial.println("Fin de la Rotacion n");
          inputString = "F-" + String( rNumA ) + "c";
          json_data = "{\"MOTOR_id\":\"L298N\",\"Value\": \"" + inputString + "\" }";
          Serial.println(json_data);
        }
      }
    }
  }

  ////////////////////////////////////////////////////////////
  //Serial.println("BOTTOM CODE");
  //delay(20); 
  ////////////////////////////////////////////////////////////
  
  // Reset de variables
  //Reinicio de Variables de Menzaje
  inputString = ""; // Limpiar cadena
  json_data = ""; // Limpiar cadena
  stringEnd = false; // Esperando Mensaje

  // si los motores no se mueven 
  // Reinicio de Variable de Motores
  if (( pRotationEnd == 0) && (nRotationEnd == 0))
  {
    rNum = 0; // Limpiar numero de rotaciones
    rNumA = 0; // Limpiar numero auxiliar de conteo
    String inputStringNum = ""; // Reiniciar variable
    digitalWrite(IN1, LOW); // Detiene por 5 seg.
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
  }
}

void serialEvent()
{
  // bool *pRotationEnd,bool *nRotationEnd) {
  while (Serial.available())
  {
    delay(5);
    // minetras exista buffer
    char inChar = (char) Serial.read(); // Leer caracter
    if (inChar == '\n')
    {
      // Si el caracter recibido corresponde a un salto de línea
      stringEnd = true; // Bandera
    }
    else
    {
      // Si no ingresar caracter a la cadena
      inputString += inChar; // Agregar caracter a la cadena
    }
    if (( * dir_pRotationEnd == 0) && ( * dir_nRotationEnd == 0))
    {
      if (inChar == 'F')
      {
        //Serial.println("F Detect");
        * dir_pRotationEnd = 1;
        * dir_nRotationEnd = 1;
        delay(5);
        inChar = (char) Serial.read(); // Leer caracter
        //Serial.print("Lectura de char: ");
        //Serial.println(inChar);
        if (inChar == '\n')
        {
          // Si el caracter recibido corresponde a un salto de línea
          //Serial.println(" Enter detectado");
          stringEnd = true; // Bandera
        }
        else if (inChar == '+')
        {
          //Serial.println("p Detect");
          * dir_nRotationEnd = 0;
        }
        else if (inChar == '-')
        {
          //Serial.println("n Detect");
          * dir_pRotationEnd = 0;
        }
        inputString += inChar; // Agregar caracter a la cadena
      }
    }
  }
}

void fun_read_led()
{
  // Ejecucion del Comando Entrante Sensores y LED
  if (inputString.equals("off"))
  {
    // Si el comando es "off"
    digitalWrite(LED_BUILTIN, 0);
    json_data = "{\"LED_id\":\"BUILTIN\",\"Value\": \"off\" }";
    Serial.println(json_data);
  }
  else if (inputString.equals("on"))
  {
    // Si el comando es "on"
    digitalWrite(LED_BUILTIN, 1);
    json_data = "{\"LED_id\":\"BUILTIN\",\"Value\": \"on\" }";
    Serial.println(json_data);
  }
  else if (inputString.equals("RA0"))
  {
    json_data = "{\"Sensor_id\":\"A0\",\"Value\":" + (String) analogRead(A0) + "}";
    Serial.println(json_data);
  }
  else if (inputString.equals("RA1"))
  {
    json_data = "{\"Sensor_id\":\"A1\",\"Value\":" + (String) analogRead(A1) + "}";
    Serial.println(json_data);
  }
  else if (inputString.equals("RA2"))
  {
    json_data = "{\"Sensor_id\":\"A2\",\"Value\":" + (String) analogRead(A2) + "}";
    Serial.println(json_data);
  }
}
