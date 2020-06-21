void setup(){
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
}
int DIR = 0;
void loop() {
  DIR = 1 - DIR;
  digitalWrite(3, DIR);
  for (int i = 0; i < 200 * 2; i++) {
    digitalWrite(4, HIGH);
    delayMicroseconds(100);
    digitalWrite(4, LOW);
    delayMicroseconds(100);
  }
  delay(1000);
}
