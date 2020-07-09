#include <Servo.h>

const long turn_steps = 400;
const int step_dir[2] = {11, 9};
const int step_pul[2] = {12, 10};
//const int grab_deg[2] = {79, 75};
//const int release_deg[2] = {101, 97};
const int grab_deg[2] = {74, 74};
const int release_deg[2] = {96, 96};
const int offset = 3;

char buf[30];
int idx = 0;
long data[3];

Servo servo0;
Servo servo1;

void move_motor(long num, long deg, long spd) {
  bool hl = true;
  if (deg < 0) hl = false;
  digitalWrite(step_dir[num], hl);
  long steps = abs(deg) * turn_steps / 360;
  long avg_time = 1000000 * 60 / turn_steps / spd;
  long max_time = 1000;
  long slope = 100;
  bool motor_hl = false;
  long accel = min(steps / 2, max(0, (max_time - avg_time) / slope));
  for (int i = 0; i < accel; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    delayMicroseconds(max_time - slope * i);
  }
  for (int i = 0; i < steps * 2 - accel * 2; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    delayMicroseconds(avg_time);
  }
  for (int i = 0; i < accel; i++) {
    motor_hl = !motor_hl;
    digitalWrite(step_pul[num], motor_hl);
    delayMicroseconds(max_time - slope * accel + accel * (i + 1));
  }
}

void release_arm(int num) {
  if (num == 0)servo0.write(release_deg[num] + offset);
  else servo1.write(release_deg[num] + offset);
  /*
  delay(70);
  if (num == 0)servo0.write(release_deg[num]);
  else servo1.write(release_deg[num]);
  */
}

void grab_arm(int num) {
  if (num == 0)servo0.write(grab_deg[num] - offset);
  else servo1.write(grab_deg[num] - offset);
  delay(70);
  if (num == 0)servo0.write(grab_deg[num]);
  else servo1.write(grab_deg[num]);
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 2; i++) {
    pinMode(step_dir[i], OUTPUT);
    pinMode(step_pul[i], OUTPUT);
  }
  servo0.attach(7);
  servo1.attach(8);
  servo0.write(release_deg[0] + 5);
  servo1.write(release_deg[1] + 5);
  delay(70);
  servo0.write(release_deg[0]);
  servo1.write(release_deg[1]);
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
