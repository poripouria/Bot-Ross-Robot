#include "SerialTransfer.h"
#include <Servo.h>

SerialTransfer myTransfer;

// Create a Servo object
Servo myservo;
#define SERVO_PIN 14   // Pin 14 = A0

void penup()  {myservo.write(80);}

void pendown()  {myservo.write(140);}

void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
  // Attach the servo to the pin
  myservo.attach(SERVO_PIN);
  pendown();
}


void loop()
{
  
  if(myTransfer.available())
  {
    penup();
    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++)
      myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    delay(2000);
    myTransfer.sendData(myTransfer.bytesRead);
    pendown();
  }
}
