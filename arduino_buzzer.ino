const int buzzerPin = 9;  // Pin del buzzer
char receivedChar;

void setup() {
  Serial.begin(9600);
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    receivedChar = Serial.read();

    if (receivedChar == 'M') {  // Movimiento detectado
      tone(buzzerPin, 1000);  // Activa el buzzer a 1000 Hz
      delay(1000);  // Mantiene activo por 1 segundo
    } 
    else if (receivedChar == 'N') {  // No hay movimiento
      noTone(buzzerPin);  // Apaga el buzzer
    }
  }
}
