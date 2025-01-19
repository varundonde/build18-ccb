const int pin1 = 3; 
const int pin2 = 4; 
const int pin3 = 5; 
const int pin4 = 6; 
const int pin5 = 7; 
const int pin6 = 8; 
const int BAUD_RATE = 9600; 


void setup() {
  // put your setup code here, to run once:
  pinMode(pin1, OUTPUT); 
  pinMode(pin2, OUTPUT); 
  pinMode(pin3, OUTPUT); 
  pinMode(pin4, OUTPUT); 
  pinMode(pin5, OUTPUT); 
  pinMode(pin6, OUTPUT); 
  Serial.begin(BAUD_RATE); 
  delay(1000); 
  
}

void loop() {
  digitalWrite(pin1, HIGH); 
  delay(1000); 
  digitalWrite(pin1, LOW); 
  delay(1000); 
  digitalWrite(pin2, HIGH); 
  delay(1000); 
  digitalWrite(pin2, LOW); 
  delay(1000); 
  digitalWrite(pin3, HIGH); 
  delay(1000); 
  digitalWrite(pin3, LOW); 
  delay(1000); 
  digitalWrite(pin4, HIGH); 
  delay(1000); 
  digitalWrite(pin4, LOW); 
  delay(1000); 
  digitalWrite(pin5, HIGH); 
  delay(1000); 
  digitalWrite(pin5, LOW); 
  delay(1000); 
  digitalWrite(pin6, HIGH); 
  delay(1000); 
  digitalWrite(pin6, LOW); 
  delay(1000); 
}
