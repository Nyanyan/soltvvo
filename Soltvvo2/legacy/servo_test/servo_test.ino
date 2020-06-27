#include <Servo.h>
Servo myservo;

void setup() {
  //9ピンからサーボモーターの回転信号をPWM出力
  myservo.attach(9); 
}

void loop() {
  myservo.write(0); //0度に回転
  delay(1000);      //1000㎳待つ
  
  myservo.write(90);
  delay(1000);
  
  myservo.write(180);
  delay(1000);
  
  myservo.write(90);
  delay(1000);
}
