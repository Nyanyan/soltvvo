#include <Stepper.h>
 
// 1回転(360度)するステップ数
// ※SPG27-1101の場合は常に120です。
// ※モーターが異なる場合は変更して下さい。
const float turnSteps = 120;
 
// [変更可能]毎分の回転数(rpm)
// ※回転時間の計算はloop()内のコードを参照
float rpm = 200;
// [変更可能]このステップ数分のモータを回転する(マイナスも設定可能)
// ※この例では「20 / 120 * 360」で60度回転します。
float Steps = 60; 
 
Stepper myStepper(turnSteps, 8,9,10,11);
 
void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(rpm) ;
}
 
void loop() {
  Serial.print("ステップ数："); 
  Serial.print(Steps,0);
  Serial.print(" 回転角度：");   
  Serial.print(Steps / turnSteps * 360,0); 
  Serial.print("度");   
  Serial.print(" 回転時間："); 
  float times = (Steps / turnSteps) * (180 / rpm);
  Serial.print(abs(times));  
  Serial.println("秒");    
  
  myStepper.step(Steps);
  
  Serial.println("delay(500);" );
  delay(500);
}
