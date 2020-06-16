#include <Stepper.h>

#define turn_steps 120
//#define rpm 10
#define quarter 32

const int arm[2] = {8, 7};

char buf[30];
int idx = 0;
int data[3];

Stepper stepper0(turn_steps, A1, A0, A3, A4);
Stepper stepper1(turn_steps, 9, 10, 11, 12);

float turning_time(int deg, int speed_motor) {
  return abs(1000 * quarter * deg / turn_steps * 60 / speed_motor);
}

void move_motor(int num, int deg, int spd) {
  digitalWrite(13, HIGH);
  if (num == 0) {
    stepper0.setSpeed(spd);
    stepper0.step(quarter * deg);
  } else if (num == 1) {
    stepper1.setSpeed(spd);
    stepper1.step(quarter * deg);
  }
  //delay(turning_time(deg, spd) * 1.1);
  digitalWrite(13, LOW);
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
