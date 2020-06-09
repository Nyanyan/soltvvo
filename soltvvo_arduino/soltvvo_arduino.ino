#include <Stepper.h>

#define turn_steps 120
#define rpm 200
#define quarter -30
#define arm0 7
#define arm1 8

char buf[30];
int idx = 0;
int data[2];

Stepper stepper0(turn_steps, 9, 10, 11, 12);
Stepper stepper1(turn_steps, A1, A0, A3, A4);

float turning_time(int deg, int speed_motor) {
  return abs(1000 * quarter * deg / turn_steps * 60 / speed_motor);
}

void move_motor(int num, int deg, int spd) {
  if (num == 0) {
    stepper0.setSpeed(spd);
    stepper0.step(quarter * deg);
  } else if (num == 1) {
    stepper1.setSpeed(spd);
    stepper1.step(quarter * deg);
  }
  delay(turning_time(deg, spd) * 1.1);
  for (int i = 0; i < 10; i++) {
    Serial.println('f');
    delay(10);
  }
}

void grab_arm(int num) {
  if (num == 0) {
    digitalWrite(arm0, HIGH);
    delay(100);
    digitalWrite(arm1, LOW);
  } else if (num == 1) {
    digitalWrite(arm1, HIGH);
    delay(100);
    digitalWrite(arm0, LOW);
  }
  for (int i = 0; i < 10; i++) {
    Serial.println('f');
    delay(10);
  }
}

void grab_all() {
  digitalWrite(arm0, HIGH);
  digitalWrite(arm1, HIGH);
  delay(100);
  for (int i = 0; i < 10; i++) {
    Serial.println('f');
    delay(10);
  }
}

void release_all() {
  digitalWrite(arm0, LOW);
  digitalWrite(arm1, LOW);
  delay(100);
  for (int i = 0; i < 10; i++) {
    Serial.println('f');
    delay(10);
  }
}
void setup() {
  Serial.begin(1200);
  pinMode(arm0, OUTPUT);
  pinMode(arm1, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    digitalWrite(13, HIGH);
    buf[idx] = Serial.read();
    if (buf[idx] == '\n') {
      buf[idx] = '\0';
      data[0] = atoi(strtok(buf, " "));
      data[1] = atoi(strtok(NULL, " "));
      if (data[1] == 0) grab_arm(data[0]);
      else if (data[1] == 10) grab_all();
      else if (data[1] == 20) release_all();
      else move_motor(data[0], data[1], rpm);
      idx = 0;
    }
    else {
      digitalWrite(13, LOW);
      idx++;
    }
  }
  Serial.print('\n');
}
