#include <pt.h>
#include <LobotServoController.h>

// Definiciones para el puente H
#define PH1IN1A 2
#define PH1IN2A 3
#define PH1ENA 4

LobotServoController myse;

// Declara dos protothreads
static struct pt ptServo, ptMotor;

void setup() {
  // Configuración del puente H
  pinMode(PH1IN1A, OUTPUT);
  pinMode(PH1IN2A, OUTPUT);
  pinMode(PH1ENA, OUTPUT);
  analogWrite(PH1ENA, 0);

  // Inicializa Serial y espera a que esté listo
  Serial.begin(9600);
  while (!Serial);

  // Inicializa los protothreads
  PT_INIT(&ptServo);
  PT_INIT(&ptMotor);
}

// Protothread para controlar el servo
static int protothreadServo(struct pt *pt) {
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) {
    PT_WAIT_UNTIL(pt, millis() - timestamp > 2000);
    myse.moveServo(2, 800, 1000); // Mueve el servo
    timestamp = millis();
    PT_WAIT_UNTIL(pt, millis() - timestamp > 1000);
    myse.moveServo(2, 0, 1000); // Mueve el servo de vuelta
    timestamp = millis();
  }
  PT_END(pt);
}

// Protothread para controlar el motor
static int protothreadMotor(struct pt *pt) {
  static unsigned long timestamp = 0;
  PT_BEGIN(pt);
  while(1) {
    PT_WAIT_UNTIL(pt, millis() - timestamp > 2000);
    // Mueve el motor
    digitalWrite(PH1IN1A, LOW);
    digitalWrite(PH1IN2A, HIGH);
    analogWrite(PH1ENA, 200);
    timestamp = millis();
    PT_WAIT_UNTIL(pt, millis() - timestamp > 5000);
    // Detiene el motor
    digitalWrite(PH1IN1A, LOW);
    digitalWrite(PH1IN2A, LOW);
    analogWrite(PH1ENA, 0);
    timestamp = millis();
  }
  PT_END(pt);
}

void loop() {
  protothreadServo(&ptServo); // Ejecuta el protothread del servo
  protothreadMotor(&ptMotor); // Ejecuta el protothread del motor
}
