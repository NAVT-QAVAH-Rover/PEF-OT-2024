#include <LobotServoController.h>

LobotServoController myse;

// Definiciones para los puentes H
#define PH1IN1A 22
#define PH1IN2A 23
#define PH1ENA 2

#define PH1IN1B 24
#define PH1IN2B 25
#define PH1ENB 3

#define PH1IN1C 26
#define PH1IN2C 27
#define PH1ENC 5

#define PH1IN1D 28
#define PH1IN2D 29
#define PH1END 44

#define PH1IN1E 30
#define PH1IN2E 31
#define PH1ENE 45

#define PH1IN1F 32
#define PH1IN2F 33
#define PH1ENF 46

char command1 = '0'; // Inicializar variables de comando
char command2 = '0';

void setup() {
  Serial.begin(9600);  
  Serial1.begin(9600);  
  
  // Inicializar puentes H
  initBridgeH();
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); 

    if (command1 == '0') {
      command1 = command; 
    } else { 
      command2 = command; 
      executeCommands(command1, command2);
      command1 = '0';
      command2 = '0';
    }
  }
}

void initBridgeH() {
  // Inicializar todos los puentes H aquí
  const int pins[] = {PH1IN1A, PH1IN2A, PH1ENA, PH1IN1B, PH1IN2B, PH1ENB, PH1IN1C, PH1IN2C, PH1ENC, PH1IN1D, PH1IN2D, PH1END, PH1IN1E, PH1IN2E, PH1ENE, PH1IN1F, PH1IN2F, PH1ENF};
  for (int pin : pins) {
    pinMode(pin, OUTPUT);
    analogWrite(pin, 0); // Asumiendo que el pin es de habilitación
  }
}

void executeCommands(char cmd1, char cmd2) {
  // Ejecutar comandos para los puentes H
  executeBridgeHCommands(cmd1);
  // Ejecutar comandos para los servos
  executeServoCommands(cmd2);
}

void executeBridgeHCommands(char cmd) {
  // Definir un array con los pines directamente
  int pins[] = {PH1IN1A, PH1IN2A, PH1ENA, PH1IN1B, PH1IN2B, PH1ENB, PH1IN1C, PH1IN2C, PH1ENC, PH1IN1D, PH1IN2D, PH1END, PH1IN1E, PH1IN2E, PH1ENE, PH1IN1F, PH1IN2F, PH1ENF};

  // Iterar sobre el array de pines
  for (int i = 0; i < sizeof(pins) / sizeof(pins[0]); ++i) {
    if (cmd == '1') {
      // Activar o desactivar motores según el comando
      if (i % 3 == 2) { // Pines de habilitación (ENx)
        analogWrite(pins[i], 250); // Habilitar motor con PWM
      } else {
        // Configurar pines de dirección (INx)
        digitalWrite(pins[i], (i % 3 == 0) ? LOW : HIGH); // Por ejemplo, IN1x en LOW y IN2x en HIGH para mover en una dirección
      }
    } else if (cmd == '2') {
      if (i % 3 == 2) { // Pines de habilitación (ENx)
        analogWrite(pins[i], 0); // Deshabilitar motor
      } else {
        // No es necesario configurar los pines de dirección si el motor está deshabilitado
        // Pero si deseas asegurarte de que están en un estado conocido, podrías ponerlos en LOW
        digitalWrite(pins[i], LOW);
      }
    }
  }
}



void executeServoCommands(char cmd) {
  if (cmd == '3' || cmd == '4') {
    int position = (cmd == '3') ? 600 : 375;
    for (int id = 1; id <= 6; ++id) {
      if (id != 3 && id != 4) { // Excepto los servos 3 y 4
        myse.moveServo(id, position, 1000);
      }
    }
    delay(2000);
  }
}