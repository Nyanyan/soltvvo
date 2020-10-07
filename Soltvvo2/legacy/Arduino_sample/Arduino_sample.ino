#include <Servo.h>

Servo servo0;
Servo servo1;

void setup(){
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  servo0.attach(5);
  servo1.attach(6);
}
int DIR = 0;
void loop() {
  /*
  DIR = 1 - DIR;
  digitalWrite(3, DIR);
  for (int i = 0; i < 200 * 2; i++) {
    digitalWrite(4, HIGH);
    delayMicroseconds(1000);
    digitalWrite(4, LOW);
    delayMicroseconds(1000);
  }
  delay(1000);
  */
  servo0.write(0);
  delay(1000);
  servo0.write(180);
  delay(1000);
}
