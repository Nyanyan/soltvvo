#include <Servo.h>

const long turn_steps = 400;
const int step_dir[2] = {3, 7};
const int step_pul[2] = {4, 8};

char buf[30];
int idx = 0;
long data[3];

Servo servo0;
Servo servo1;

void move_motor(long num, long deg, long spd) {
  bool hl = true;
  if (deg < 0) hl = false;
  digitalWrite(step_dir[num], hl);
  long wait_time = 1000000 * 60 / turn_steps / spd;
  long steps = abs(deg) * turn_steps / 360;
  bool motor_hl = false;
  for (int i = 0; i < steps; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    delayMicroseconds(wait_time);
  }
}

void release_arm(int num) {
  if (num == 0)servo0.write(120);
  else servo1.write(120);
}

void grab_arm(int num) {
  if (num == 0)servo0.write(60);
  else servo1.write(60);
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 2; i++) {
    pinMode(step_dir[i], OUTPUT);
    pinMode(step_pul[i], OUTPUT);
  }
  servo0.attach(5);
  servo1.attach(6);
}

void loop() {
  if (Serial.available()) {
    buf[idx] = Serial.read();
    if (buf[idx] == '\n') {
      buf[idx] = '\0';
      data[0] = atoi(strtok(buf, " "));
      data[1] = atoi(strtok(NULL, " "));
      data[2] = atoi(strtok(NULL, " "));
      if (data[1] == 1000) grab_arm(data[0]);
      else if (data[1] == 2000) release_arm(data[0]);
      else move_motor(data[0], data[1], data[2]);
      idx = 0;
    }
    else {
      idx++;
    }
  }
}
