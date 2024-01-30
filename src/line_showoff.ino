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
  while (millis() - startTime < 205000)
  {
    //starting point
    while(millis() - startTime < 5000)    leftright(-1);

    //5cm vertical line
    pendown();
    while(millis() - startTime > 5000 && millis() - startTime < 10000)   leftright(-1);
    
    //2cm shift 
    penup();
    while(millis() - startTime > 10000 && millis() - startTime < 10500);
    while(millis() - startTime > 10500 && millis() - startTime < 12500)   leftright(-1);

    //5cm horizontal line
    pendown();
    while(millis() - startTime > 12500 && millis() - startTime < 17500)   updown(-1);

    //2cm shift
    penup();
    while(millis() - startTime > 17500 && millis() - startTime < 18000);
    while(millis() - startTime > 18000 && millis() - startTime < 20000)   leftright(-1);

    //5*sqrt(2) diagonal 1
    pendown();
    while(millis() - startTime > 20000 && millis() - startTime < 25000)
    {
      leftright(-1);
      updown(+1);
    }

    //2cm shift
    penup();
    while(millis() - startTime > 25000 && millis() - startTime < 25500);
    while(millis() - startTime > 25500 && millis() - startTime < 27500)   leftright(-1);

    //5*sqrt(2) diagonal 2
    pendown();
    while(millis() - startTime > 27500 && millis() - startTime < 32500)
    {
      leftright(-1);
      updown(-1);
    }    

    //come back
    //new staring position
    penup();
    while(millis() - startTime > 32500 && millis() - startTime < 33000);
    while(millis() - startTime > 33000 && millis() - startTime < 38000)   updown(-1);
    while(millis() - startTime > 38000 && millis() - startTime < 59000)   leftright(+1);

    
    //tighten
    while(millis() - startTime > 59000 && millis() - startTime < 60000)    tight();  

    //5cm square
    pendown();
    while(millis() - startTime > 60000 && millis() - startTime < 65000)   leftright(-1);
    while(millis() - startTime > 65000 && millis() - startTime < 70000)   updown(-1);
    while(millis() - startTime > 70000 && millis() - startTime < 75000)   leftright(+1);
    while(millis() - startTime > 75000 && millis() - startTime < 80000)   updown(+1);

    //2cm shift
    penup();
    while(millis() - startTime > 80000 && millis() - startTime < 80500);
    while(millis() - startTime > 80500 && millis() - startTime < 87500)   leftright(-1);

    //10cm*5cm rectangle 
    pendown();
    while(millis() - startTime > 87500 && millis() - startTime < 97500)   leftright(-1);
    while(millis() - startTime > 97500 && millis() - startTime < 102500)   updown(-1);
    while(millis() - startTime > 102500 && millis() - startTime < 112500)   leftright(+1);
    while(millis() - startTime > 112500 && millis() - startTime < 117500)   updown(+1);

    //3cm shift
    penup();
    while(millis() - startTime > 117500 && millis() - startTime < 118000);
    while(millis() - startTime > 118000 && millis() - startTime < 131000)   leftright(-1);

    //triangle 1
    pendown();
    while(millis() - startTime > 131000 && millis() - startTime < 136000)   updown(-1);
    while(millis() - startTime > 136000 && millis() - startTime < 141000)   leftright(-1);
    while(millis() - startTime > 141000 && millis() - startTime < 146000)
    {
      leftright(+1);
      updown(+1);
    }    

    //triangle 2 starting position
    penup();
    while(millis() - startTime > 146000 && millis() - startTime < 146500);
    while(millis() - startTime > 146500 && millis() - startTime < 149500)   leftright(-1);

    pendown();
    while(millis() - startTime > 149500 && millis() - startTime < 154500)   leftright(-1);
    while(millis() - startTime > 154500 && millis() - startTime < 159500)   updown(-1);
    while(millis() - startTime > 159500 && millis() - startTime < 164500)
    {
      leftright(+1);
      updown(+1);
    }    

    //comeback to starting pos
    penup();
    while(millis() - startTime > 164500 && millis() - startTime < 165000);
    while(millis() - startTime > 165000 && millis() - startTime < 193000)   leftright(+1);
    while(millis() - startTime > 193000 && millis() - startTime < 203000)   updown(+1);
    while(millis() - startTime > 203000 && millis() - startTime < 205000)   tight();
  }
  allstop();

}
