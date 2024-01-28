// Include the Arduino Stepper.h library:
#include "Stepper.h"
#include <Servo.h>

// Define number of steps per rotation:
const int stepsPerRevolution = 2048;
int i=1;

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
     Motor1.setSpeed (17);
     Motor2.setSpeed (15);
  }
  
  else if(mstep<0)
  {
     Motor1.setSpeed (15);
     Motor2.setSpeed (17);
  }
  
  Motor1.step(mstep);   
  Motor2.step(-1*mstep);
}


void setup ()
{
  // Attach the servo to the pin
  myservo.attach(SERVO_PIN);
}

void loop ()
{
  // get the current time in milliseconds
  unsigned long startTime = millis();

  // +1 Up
  // -1 Down

  // +1 left
  // -1 right

  penup();
  while (millis() - startTime < 1000)
  {
    //tight();
    leftright(+1);
    //updown(+1);
  }
  allstop();

}
