#include "Stepper.h"
#include <Servo.h>
#include "SerialTransfer.h"

SerialTransfer myTransfer;

// Define number of steps per rotation:
const int stepsPerRevolution = 2048;
int penstate=0;
int work=0;

// Wiring:

// Left Motor = Motor1
// Pin 2 to IN1 on the ULN2003 driver
// Pin 3 to IN2 on the ULN2003 driver
// Pin 4 to IN3 on the ULN2003 driver
// Pin 5 to IN4 on the ULN2003 driver


// Right Motor = Motor2
// Pin 6 to IN1 on the ULN2003 driver
// Pin 7 to IN2 on the ULN2003 driver
// Pin 8 to IN3 on the ULN2003 driver
// Pin 9 to IN4 on the ULN2003 driver


// Center Motor = Motor3
// Pin 10 to IN1 on the ULN2003 driver
// Pin 11 to IN2 on the ULN2003 driver
// Pin 12 to IN3 on the ULN2003 driver
// Pin 13 to IN4 on the ULN2003 driver


// Servo = myservo
// Pin A0 => 14 => Orange Wire


// Create stepper object, note the pin order:
Stepper Motor1 = Stepper (stepsPerRevolution,  2,  4,  3,  5);  // Left Motor
Stepper Motor2 = Stepper (stepsPerRevolution,  6,  8,  7,  9);  // Right Motor
Stepper Motor3 = Stepper (stepsPerRevolution, 10, 12, 11, 13);  // Center Motor

// Create a Servo object
Servo myservo;
#define SERVO_PIN 14   // Pin 14 = A0


  // Motor1 = LeftMotor
  // Left '-' => Baz
  // Left '+' => Jam

  // Motor2 = RightMotor
  // Right '-'  => Baz
  // Right '+'  => Jam

  // Motor3 = CenterMotor
  // Center '+' => Jam
  // Center '-' => Baz

  // myservo = Servo
  // 80 degree = Up
  // 140 degree = Down

void penup()  {myservo.write(80);}

void pendown()  {myservo.write(140);}

void allstop()
{
  Motor1.setSpeed(0);
  Motor2.setSpeed(0);
  Motor3.setSpeed(0);
}

void tight()
{
  Motor1.setSpeed (15);
  Motor2.setSpeed (15);
  Motor1.step(+1);
  Motor2.step(+1);
}
void updown(int mstep)
{
  Motor3.setSpeed(15);
  Motor3.step(mstep); 
}

void leftright(int mstep)
{
  if(mstep>0)
  {
     Motor1.setSpeed (15);
     Motor2.setSpeed (15);
  }
  
  else if(mstep<0)
  {
     Motor1.setSpeed (15);
     Motor2.setSpeed (15);
  }
  
  Motor1.step(mstep);   
  Motor2.step(-1*mstep);
}




void setup()
{
  Serial.begin(115200);
  myTransfer.begin(Serial);
  
  // Attach the servo to the pin
  myservo.attach(SERVO_PIN);
  work=0;
  penup();
  penstate=0;
  
}

void loop()
{
  while(myTransfer.available())
  {
    // send all received data back to Python
    for(uint16_t i=0; i < myTransfer.bytesRead; i++)
        myTransfer.packet.txBuff[i] = myTransfer.packet.rxBuff[i];
    
    if(work==0)
    {
      unsigned long startTime0 = millis();
      //starting point
      while(millis() - startTime0 < 5000)    leftright(-1);
      startTime0 = millis();
      while(millis() - startTime0 < 500)    tight();
      work=1;
    }

    
    else if(work==1)
    {
      unsigned long startTime;
      startTime = millis();
       // +1 Up
       // -1 Down
    
       // +1 left
       // -1 right
      
       if(myTransfer.packet.txBuff[0]=='1' && penstate==0)
        {
          while(millis() - startTime < 200)
          {
            pendown();
            penstate=1;
          }
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
    
        else if(myTransfer.packet.txBuff[0]=='0' && penstate==1)
        {
          while(millis() - startTime < 200)
          {
            penup();
            penstate=0;
          }
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
    
    
        //down
        if(myTransfer.packet.txBuff[1]=='-' && myTransfer.packet.txBuff[2]=='0')
        {
          while(millis() - startTime < 100)   updown(-1);
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
          
        //up
        else if(myTransfer.packet.txBuff[1]=='+' && myTransfer.packet.txBuff[2]=='0')
        {
          while(millis() - startTime < 100)   updown(+1);
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
          
        //right
        else if(myTransfer.packet.txBuff[1]=='0' && myTransfer.packet.txBuff[2]=='-')
        {  
          while(millis() - startTime < 100)   leftright(-1);
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
          
        //left
        else if(myTransfer.packet.txBuff[1]=='0' && myTransfer.packet.txBuff[2]=='+')
        {
          while(millis() - startTime < 100)   leftright(+1);
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
    
    
    
        //down-right
        else if(myTransfer.packet.txBuff[1]=='-' && myTransfer.packet.txBuff[2]=='-')
        {
          while(millis() - startTime < 100)
          {
            updown(-1);
            leftright(-1);
          }
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
    
        //up-right
        else if(myTransfer.packet.txBuff[1]=='+' && myTransfer.packet.txBuff[2]=='-')
        {
          while(millis() - startTime < 100)
          {
            updown(+1);
            leftright(-1);
          }
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
    
        //down-left
        else if(myTransfer.packet.txBuff[1]=='-' && myTransfer.packet.txBuff[2]=='+')
        {
          while(millis() - startTime < 100)
          {
            updown(-1);
            leftright(+1);
          }
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }
        
        //up-left
        else if(myTransfer.packet.txBuff[1]=='+' && myTransfer.packet.txBuff[2]=='+')
        {
          while(millis() - startTime < 100)
          {
            updown(+1);
            leftright(+1);
          }
          startTime = millis();
          while (millis() - startTime < 50);
          startTime = millis();
        }

        else if(myTransfer.packet.txBuff[0]=='0' && myTransfer.packet.txBuff[1]=='0' && myTransfer.packet.txBuff[2]=='0')
        {
          penup();
          startTime = millis();
          while (millis() - startTime < 5000)   leftright(+1);
          startTime = millis();
          while (millis() - startTime < 1000)   tight();
        }
        
        else if(myTransfer.packet.txBuff[0]=='x' && myTransfer.packet.txBuff[1]=='x' && myTransfer.packet.txBuff[2]=='x')
        {
          startTime = millis();
          while (millis() - startTime < 300)   tight(); 
          startTime = millis();
          while (millis() - startTime < 100);
          startTime = millis();
        }
        
    }
    myTransfer.sendData(myTransfer.bytesRead);
  }
}
