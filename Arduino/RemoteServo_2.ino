
#include <Servo.h> 
 
Servo myservo1;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
Servo myservo2;  // create servo object to control a servo 
 
int pos = 0;    // variable to store the servo position 
int servo1_ready = 1;
int servo2_ready = 1;

void setup() 
{ 
  pinMode(5,INPUT);
  pinMode(6,INPUT);
  myservo1.attach(9);  // attaches the servo on pin 9 to the servo object 
  myservo2.attach(10);  // attaches the servo on pin 9 to the servo object 
  
  myservo1.write(0);              // tell servo to go to position in variable 'pos' 
  myservo2.write(90);              // tell servo to go to position in variable 'pos' 
} 
 
 
void loop() 
{ 

  if(digitalRead(5)==HIGH && servo1_ready>0){

    for(pos = 0; pos < 90; pos += 1)  // goes from 0 degrees to 180 degrees 
      {                                  // in steps of 1 degree 
        myservo1.write(pos);              // tell servo to go to position in variable 'pos' 
        delay(15);                       // waits 15ms for the servo to reach the position 
      }     
      
    for(pos = 90; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
    {                                
      myservo1.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(15);                       // waits 15ms for the servo to reach the position 
    } 
   
    servo1_ready = 0;
    servo2_ready = 1;
  }

  
  if(digitalRead(6)==HIGH && servo2_ready>0){

    for(pos = 90; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
    {                                
      myservo2.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(15);                       // waits 15ms for the servo to reach the position 
    } 

    for(pos = 0; pos < 90; pos += 1)  // goes from 0 degrees to 180 degrees 
    {                                  // in steps of 1 degree 
      myservo2.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(15);                       // waits 15ms for the servo to reach the position 
    }     
    servo2_ready = 0;
    servo1_ready = 1;
  }  

  
} 
