#include <TimerOne.h>
#include <Servo.h>

#define turn_steps 200
//#define quarter 50
const int step_dir[2] = {3, 7};
const int step_pul[2] = {4, 8};
const int arm[2] = {5, 6};

char buf[30];
int idx = 0;
int data[3];

int steps, fin, motor_num, cnt, wait_time;
bool motor_hl;

void move_motor_p() {
  cnt++;
  if (cnt == wait_time) {
    if (steps < fin) {
      digitalWrite(motor_num, !motor_hl);
      steps++;
    }
    else Timer1.stop();
  }
}

void move_motor(int num, int deg, int spd) {
  bool hl = true;
  if (deg < 0) hl = false;
  digitalWrite(step_dir[num], hl);
  wait_time = 1000000 * 60 * 360 / turn_steps / spd / 360;
  steps = 0;
  fin = deg / (360 / turn_steps);
  motor_hl = false;
  motor_num = num;
  cnt = 0;
  Timer1.initialize(1);
  Timer1.attachInterrupt(move_motor_p);
  Timer1.start();
}

void release_arm(int num) {
  digitalWrite(13, HIGH);
  digitalWrite(arm[num], LOW);
  digitalWrite(13, LOW);
}

void grab_arm(int num) {
  digitalWrite(13, HIGH);
  digitalWrite(arm[num], HIGH);
  digitalWrite(13, LOW);
}

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 2; i++)
    pinMode(arm[i], OUTPUT);
  pinMode(13, OUTPUT);
  //Serial.println("start");
}

void loop() {
  if (Serial.available()) {
    buf[idx] = Serial.read();
    if (buf[idx] == '\n') {
      buf[idx] = '\0';
      //for (int i = 0; i < 30; i++) Serial.print(buf[i]);
      //Serial.println(' ');
      data[0] = atoi(strtok(buf, " "));
      data[1] = atoi(strtok(NULL, " "));
      data[2] = atoi(strtok(NULL, " "));
      /*
        Serial.print(data[0]);
        Serial.print('\t');
        Serial.print(data[1]);
        Serial.print('\t');
        Serial.println(data[2]);
      */
      if (data[1] == 5) grab_arm(data[0]);
      else if (data[1] == 6) release_arm(data[0]);
      else move_motor(data[0], data[1], data[2]);
      idx = 0;
    }
    else {
      idx++;
    }
  }
}
