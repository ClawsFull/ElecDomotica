// Version bidirecional de comunicacion serial con pantalla, el arduino responde segun una solicitud
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
// Para el Manejo de pantalla es necesario tener disponible los pines I2C por lo que se sacrifican dos posibles sensores para tener una 
// pantalla en la que se muentran los comandos entrantes en el dispositivo, el codigo es funcional para cualquier pantalla compatible 
// con la libreria U8glib.h y se comunique por I2C. Referencia: https://github.com/olikraus/u8glib
//

#include "U8glib.h"

// Aqui se ingresa el tipo de pantalla que corresponde para la creacion del objeto u8g 
// NOTA IMPORTANTE: La lista est[a] incompleta. La lista de todos los dispositivos se puede 
// encontrar en el siguiente enlace: https://github.com/olikraus/u8glib/wiki/device
// Para si se quiere cambiar la pantalla tomar en cuenta las indicaciones anteriores y descomentar
// la opcion que se requiere y comentar el resto de dispositivos.
//U8GLIB_NHD27OLED_BW u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD27OLED_2X_BW u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD27OLED_GR u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD27OLED_2X_GR u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD31OLED_BW u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD31OLED_2X_BW u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD31OLED_GR u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_NHD31OLED_2X_GR u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGS102 u8g(13, 11, 10, 9, 8);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGM132 u8g(13, 11, 10, 9);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGM128 u8g(13, 11, 10, 9);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGM128_2X u8g(13, 11, 10, 9);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_ST7920_128X64_1X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, di=17,rw=16
//U8GLIB_ST7920_128X64_4X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, di=17,rw=16
//U8GLIB_ST7920_128X64_1X u8g(18, 16, 17);	// SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
//U8GLIB_ST7920_128X64_4X u8g(18, 16, 17);	// SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
//U8GLIB_ST7920_192X32_1X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, di=17,rw=16
//U8GLIB_ST7920_192X32_4X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, di=17,rw=16
//U8GLIB_ST7920_192X32_1X u8g(18, 16, 17);	// SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
//U8GLIB_ST7920_192X32_4X u8g(18, 16, 17);	// SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
//U8GLIB_ST7920_192X32_1X u8g(13, 11, 10);	// SPI Com: SCK = en = 13, MOSI = rw = 11, CS = di = 10
//U8GLIB_ST7920_192X32_4X u8g(10);		// SPI Com: SCK = en = 13, MOSI = rw = 11, CS = di = 10, HW SPI
//U8GLIB_ST7920_202X32_1X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, di=17,rw=16
//U8GLIB_ST7920_202X32_4X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, di=17,rw=16
//U8GLIB_ST7920_202X32_1X u8g(18, 16, 17);	// SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
//U8GLIB_ST7920_202X32_4X u8g(18, 16, 17);	// SPI Com: SCK = en = 18, MOSI = rw = 16, CS = di = 17
//U8GLIB_LM6059 u8g(13, 11, 10, 9);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_LM6063 u8g(13, 11, 10, 9);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGXL160_BW u8g(10, 9);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGXL160_GR u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGXL160_2X_BW u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_DOGXL160_2X_GR u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_PCD8544 u8g(13, 11, 10, 9, 8);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, Reset = 8
//U8GLIB_PCF8812 u8g(13, 11, 10, 9, 8);		// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, Reset = 8
//U8GLIB_KS0108_128 u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 14, 15, 17, 16); 		// 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, cs1=14, cs2=15,di=17,rw=16
//U8GLIB_LC7981_160X80 u8g(8, 9, 10, 11, 4, 5, 6, 7,  18, 14, 15, 17, 16); 	// 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, cs=14 ,di=15,rw=17, reset = 16
//U8GLIB_LC7981_240X64 u8g(8, 9, 10, 11, 4, 5, 6, 7,  18, 14, 15, 17, 16); 	// 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, cs=14 ,di=15,rw=17, reset = 16
//U8GLIB_LC7981_240X128 u8g(8, 9, 10, 11, 4, 5, 6, 7,  18, 14, 15, 17, 16); 	// 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, cs=14 ,di=15,rw=17, reset = 16
//U8GLIB_ILI9325D_320x240 u8g(18,17,19,U8G_PIN_NONE,16 );  			// 8Bit Com: D0..D7: 0,1,2,3,4,5,6,7 en=wr=18, cs=17, rs=19, rd=U8G_PIN_NONE, reset = 16
//U8GLIB_SBN1661_122X32 u8g(8,9,10,11,4,5,6,7,14,15, 17, U8G_PIN_NONE, 16); 	// 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 cs1=14, cs2=15,di=17,rw=16,reset = 16
//U8GLIB_SSD1306_128X64 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_SSD1306_128X64 u8g(4, 5, 6, 7);	// SW SPI Com: SCK = 4, MOSI = 5, CS = 6, A0 = 7 (new white HalTec OLED)
//U8GLIB_SSD1306_128X64 u8g(10, 9);		// HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NONE|U8G_I2C_OPT_DEV_0);	// I2C / TWI 
//U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_DEV_0|U8G_I2C_OPT_NO_ACK|U8G_I2C_OPT_FAST);	// Fast I2C / TWI 
//U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NO_ACK);	// Display which does not send AC
//U8GLIB_SSD1306_ADAFRUIT_128X64 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_SSD1306_ADAFRUIT_128X64 u8g(10, 9);		// HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
//U8GLIB_SSD1306_128X32 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_SSD1306_128X32 u8g(10, 9);             // HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
//U8GLIB_SSD1306_128X32 u8g(U8G_I2C_OPT_NONE);	// I2C / TWI 
//U8GLIB_SSD1306_64X48 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_SSD1306_64X48 u8g(10, 9);             // HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
//U8GLIB_SSD1306_64X48 u8g(U8G_I2C_OPT_NONE);	// I2C / TWI 
//U8GLIB_SH1106_128X64 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_SH1106_128X64 u8g(4, 5, 6, 7);	// SW SPI Com: SCK = 4, MOSI = 5, CS = 6, A0 = 7 (new blue HalTec OLED)
//U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NONE);	// I2C / TWI 
//U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_DEV_0|U8G_I2C_OPT_FAST);	// Dev 0, Fast I2C / TWI
//U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NO_ACK);	// Display which does not send ACK
//U8GLIB_SSD1309_128X64 u8g(13, 11, 10, 9);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_SSD1327_96X96_GR u8g(U8G_I2C_OPT_NONE);	// I2C
//U8GLIB_SSD1327_96X96_2X_GR u8g(U8G_I2C_OPT_NONE);	// I2C
//U8GLIB_UC1611_DOGM240 u8g(U8G_I2C_OPT_NONE);	// I2C
//U8GLIB_UC1611_DOGM240 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_UC1611_DOGM240 u8g(10, 9);		// HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
//U8GLIB_UC1611_DOGM240 u8g(10, 9);		// HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
//U8GLIB_UC1611_DOGM240 u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 3, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, cs=3, di/a0=17,rw=16
//U8GLIB_UC1611_DOGXL240 u8g(U8G_I2C_OPT_NONE);	// I2C
//U8GLIB_UC1611_DOGXL240 u8g(13, 11, 10, 9);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9
//U8GLIB_UC1611_DOGXL240 u8g(10, 9);		// HW SPI Com: CS = 10, A0 = 9 (Hardware Pins are  SCK = 13 and MOSI = 11)
//U8GLIB_UC1611_DOGXL240 u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 3, 17, 16);   // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7 en=18, cs=3, di/a0=17,rw=16
//U8GLIB_NHD_C12864 u8g(13, 11, 10, 9, 8);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_NHD_C12832 u8g(13, 11, 10, 9, 8);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_LD7032_60x32 u8g(13, 11, 10, 9, 8);	// SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_LD7032_60x32 u8g(11, 12, 9, 10, 8);	// SPI Com: SCK = 11, MOSI = 12, CS = 9, A0 = 10, RST = 8  (SW SPI Nano Board)
//U8GLIB_UC1608_240X64 u8g(13, 11, 10, 9, 8);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X64_2X u8g(13, 11, 10, 9, 8);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X64 u8g(10, 9, 8);	// HW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X64_2X u8g(10, 9, 8);	// HW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X u8g(13, 11, 10, 9, 8);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X64_2X u8g(13, 11, 10, 9, 8);	// SW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X64 u8g(10, 9, 8);	// HW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_UC1608_240X64_2X u8g(10, 9, 8);	// HW SPI Com: SCK = 13, MOSI = 11, CS = 10, A0 = 9, RST = 8
//U8GLIB_T6963_240X128 u8g(8, 9, 10, 11, 4, 5, 6, 7, 14, 15, 17, 18, 16); // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7, cs=14, a0=15, wr=17, rd=18, reset=16
//U8GLIB_T6963_128X128 u8g(8, 9, 10, 11, 4, 5, 6, 7, 14, 15, 17, 18, 16); // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7, cs=14, a0=15, wr=17, rd=18, reset=16
//U8GLIB_T6963_240X64 u8g(8, 9, 10, 11, 4, 5, 6, 7, 14, 15, 17, 18, 16); // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7, cs=14, a0=15, wr=17, rd=18, reset=16
//U8GLIB_T6963_128X64 u8g(8, 9, 10, 11, 4, 5, 6, 7, 14, 15, 17, 18, 16); // 8Bit Com: D0..D7: 8,9,10,11,4,5,6,7, cs=14, a0=15, wr=17, rd=18, reset=16
//U8GLIB_HT1632_24X16 u8g(3, 2, 4);		// WR = 3, DATA = 2, CS = 4
//U8GLIB_SSD1351_128X128_332 u8g(13, 11, 8, 9, 7); // Arduino UNO: SW SPI Com: SCK = 13, MOSI = 11, CS = 8, A0 = 9, RESET = 7 (http://electronics.ilsoft.co.uk/ArduinoShield.aspx)
//U8GLIB_SSD1351_128X128_332 u8g(76, 75, 8, 9, 7); // Arduino DUE: SW SPI Com: SCK = 13, MOSI = 11, CS = 8, A0 = 9, RESET = 7 (http://electronics.ilsoft.co.uk/ArduinoShield.aspx)
//U8GLIB_SSD1351_128X128_332 u8g(8, 9, 7); // Arduino: HW SPI Com: SCK = 13, MOSI = 11, CS = 8, A0 = 9, RESET = 7 (http://electronics.ilsoft.co.uk/ArduinoShield.aspx)
//U8GLIB_SSD1351_128X128_HICOLOR u8g(76, 75, 8, 9, 7); // Arduino DUE, SW SPI Com: SCK = 76, MOSI = 75, CS = 8, A0 = 9, RESET = 7 (http://electronics.ilsoft.co.uk/ArduinoShield.aspx)
//U8GLIB_SSD1351_128X128_HICOLOR u8g(8, 9, 7); // Arduino, HW SPI Com: SCK = 76, MOSI = 75, CS = 8, A0 = 9, RESET = 7 (http://electronics.ilsoft.co.uk/ArduinoShield.aspx)
//U8GLIB_SSD1351_128X128GH_332 u8g(8, 9, 7); // Arduino, HW SPI Com: SCK = 76, MOSI = 75, CS = 8, A0 = 9, RESET = 7 (Freetronics OLED)
//U8GLIB_SSD1351_128X128GH_HICOLOR u8g(8, 9, 7); // Arduino, HW SPI Com: SCK = 76, MOSI = 75, CS = 8, A0 = 9, RESET = 7 (Freetronics OLED)

String inputString = ""; // Cadena para guardar el comando recibido
String inputStringNum = "";
String json_data = ""; // Cadena pata emitir
bool first_run = true; // Flag first run
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
int IN_default = 0; // Si se quiere invertir la logica default de salida de motor cambiar a 1
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
int stepM[4][4] = // matriz (array bidimensional) con la secuencia de pasos logica invertida
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
#define SPACELINE u8g.getFontLineSpacing()
// setup input buffer
#define LINE_MAX 30 
uint8_t line_buf[LINE_MAX-1] = "<< DEBUG CONSOLE >>";
uint8_t line_pos = 0;

// setup a text screen to support scrolling
#define ROW_MAX 13


uint8_t screen[ROW_MAX][LINE_MAX];
uint8_t rows, cols;

// line height, which matches the selected font (5x7)
#define LINE_PIXEL_HEIGHT 7

// clear entire screen, called during setup
void clear_screen(void) {
  uint8_t i, j;
  for( i = 0; i < ROW_MAX; i++ )
    for( j = 0; j < LINE_MAX; j++ )
      screen[i][j] = 0;  
}

// append a line to the screen, scroll up
void add_line_to_screen(void) {
  uint8_t i, j;
  for( j = 0; j < LINE_MAX; j++ )
    for( i = 0; i < rows-1; i++ )
      screen[i][j] = screen[i+1][j];
  if (first_run){
    screen[rows-1][0]=' ';
    screen[rows-1][1]=' ';
    screen[rows-1][2]=' ';
    for( j = 0; j < LINE_MAX-3; j++ ) //recorte de print 3 rows antes
      screen[rows-1][j+3] = line_buf[j];
    first_run = false;
  }else{
  screen[rows-1][0]='>';
  screen[rows-1][1]='>';
  screen[rows-1][2]=' ';
  for( j = 0; j < LINE_MAX-3; j++ ) //recorte de print 3 rows antes
    screen[rows-1][j+3] = line_buf[j];
  }
}

// U8GLIB draw procedure: output the screen
void draw(void) {
  uint8_t i, y;
  // graphic commands to redraw the complete screen are placed here    
  y = 0;       // reference is the top left -1 position of the string
  y = -2;             // correct the -1 position of the drawStr 
  for( i = 0; i < rows; i++ )
  {
    u8g.drawStr( 1, y, (char *)(screen[i]));
    y = y + SPACELINE;
  }
}

void exec_line(void) {
  // echo line to the serial monitor
  //Serial.println((const char *)line_buf);
  delay(5);
  // add the line to the screen
  add_line_to_screen();
  
  // U8GLIB picture loop
  u8g.firstPage();  
  do {
    draw();
  } while( u8g.nextPage() );
}

// clear current input buffer
void reset_line(void) { 
      line_pos = 0;
      line_buf[line_pos] = '\0'; // Replace ">> "; to '\0';
        
}

// add a single character to the input buffer 
void char_to_line(uint8_t c) {
      line_buf[line_pos] = c;
      line_pos++;
      line_buf[line_pos] = '\0';  
}


void setup()
{
  //Setup principal
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
  pinMode(A0, INPUT);  // pines analogos habilitados
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  inputString.reserve(200);


  //Setup pantalla
  // set font for the console window
  u8g.setFont(u8g_font_5x7);
  //u8g.setFont(u8g_font_9x15);
  
  // set upper left position for the string draw procedure
  u8g.setFontPosTop();
  
  // calculate the number of rows for the display
  rows = u8g.getHeight() / u8g.getFontLineSpacing();
  if ( rows > ROW_MAX )
    rows = ROW_MAX; 
  
  // estimate the number of columns for the display
  cols = u8g.getWidth() / u8g.getStrWidth("m");
  if ( cols > LINE_MAX-1 )
    cols = LINE_MAX-1; 
  
  clear_screen();               // clear screen
  delay(100);                   // do some delay
  Serial.begin(38400);           // init serial normalmente a 9600 pero se requiere de 38400
  exec_line();                  // place the input buffer into the screen
  reset_line();                 // clear input buffer
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
        // Lineas opcionales:
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
        // Lineas obligatorias de Error:
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
    uint8_t c;
    char inChar = (char) Serial.read(); // Leer caracter
    
    // Codigo de la pantalla
    c = inChar;
    if ( line_pos >= cols-1-3 ) {
      exec_line();
      reset_line();
      char_to_line(c);
    } 
    else if ( c == '\n' ) {
      exec_line();
      reset_line();
    }
    else if ( c == '\r' ) {
      // ignore '\r'
    }
    else {
      //Serial.println(c);
      char_to_line(c);
    }

  // Lectura de las funciones
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
        c = inChar;
        if ( line_pos >= cols-1-3 ) {
          exec_line();
          reset_line();
          char_to_line(c);
        } 
        else if ( c == '\n' ) {
          exec_line();
          reset_line();
        }
        else if ( c == '\r' ) {
          // ignore '\r'
        }
        else {
          //Serial.println(c); //para revisar en tabla ASCII la correcta deteccion 
          char_to_line(c);
        }
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
        else if (inChar == '*')
        {
          //Serial.println("n Detect");
          * dir_pRotationEnd = 0;
          * dir_nRotationEnd = 0;
        }
        inputString += inChar; // Agregar caracter a la cadena
      }
    }
    else if(( * dir_pRotationEnd == 1) ^ ( * dir_nRotationEnd == 1))
    {
      if (inChar == 'F')
      {
        //Serial.println("F Detect");
        //* dir_pRotationEnd = 1;
        //* dir_nRotationEnd = 1;
        delay(5);
        inChar = (char) Serial.read(); // Leer caracter
        c = inChar;
        if ( line_pos >= cols-1-3 ) {
          exec_line();
          reset_line();
          char_to_line(c);
        } 
        else if ( c == '\n' ) {
          exec_line();
          reset_line();
        }
        else if ( c == '\r' ) {
          // ignore '\r'
        }
        else {
          //Serial.println(c); //para revisar en tabla ASCII la correcta deteccion 
          char_to_line(c);
        }
        //Serial.print("Lectura de char: ");
        //Serial.println(inChar);
        if (inChar == '\n')
        {
          // Si el caracter recibido corresponde a un salto de línea
          //Serial.println(" Enter detectado");
          stringEnd = true; // Bandera
        }
        else if (inChar == '*')
        {
          //Serial.println("n Detect");
          * dir_pRotationEnd = 0;
          * dir_nRotationEnd = 0;
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
