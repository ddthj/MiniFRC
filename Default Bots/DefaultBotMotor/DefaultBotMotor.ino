//instructions for downloading and installing libraries can be found here: https://www.instructables.com/id/Downloading-All-the-Software-Youll-Need-for-MiniFR/
#include <SoftwareSerial.h>         //this library is part of Arduino by default
#include <AFMotor.h>                //you must download and install this library: https://drive.google.com/file/d/1zsMywqJjvzgMBoVZyrYly-2hXePFXFzw/view?usp=sharing
#include <String.h>
/* <==============================================================>
 *  You will need to change the following variables depending on what
 *  analog pins on your motor shield you are using, which motor goes to
 *  which port, and if your drive logic is flipped. */

//change A0 and A1 to match whatever pins you are useing for your bluetooth chip
SoftwareSerial bluetooth(A0, A1); //RX,TX

//These lines declare which ports your drive motors will be connected to on the motor shield.
AF_DCMotor mLeft(3);
AF_DCMotor mRight(4);

//this line declares which port your extra motor is on
AF_DCMotor mExtra(1);

int xAxisMultiplier = 1;      // Change this variable to -1 if your robot turns the wrong way
int yAxisMultiplier = 1;       // Change ths variable to -1 if your robot drives backward when it should be going forward

/* You shouldn't need to change anything past here unless you're adding
 *  something like an automode, extra motor, or servo. 
 *  <==============================================================> */

// Variables used to recive data from the driverstation and calculate drive logic
float xAxis, yAxis;
int velocityL, velocityR;
String pack;

//this variable is used to control your extra motor
float button;

// In setup, we tell bluetooth communication to start and set all of our motors to not move
void setup() {
  bluetooth.begin(9600);
  drive(0, 0);
  pinMode(16,OUTPUT);
}

void loop() {
  digitalWrite(16,LOW);
  while(bluetooth.available() > 0){                                   // This line checks for any new data in the buffer from the driverstation    
    digitalWrite(16,HIGH);
    if ((bluetooth.read()) == 'a'){                                   // We use 'z' as a delimiter to ensure that the data doesn't desync
      pack = bluetooth.readStringUntil('z');
      xAxis = (getValue(pack,0).toFloat()) * (100) * xAxisMultiplier;     // For each item the driver station sends, we have a variable here to recieve it
      yAxis = (getValue(pack,1).toFloat()) * (100) * yAxisMultiplier;
      button = getValue(pack,2).toInt();

      //these lines control your extra motor. You may have to change them in order to get the desired result from your motor
      if (button == 1){
        mExtra.run(FORWARD);
        mExtra.setSpeed(255);
      } else {
        mExtra.run(FORWARD);
        mExtra.setSpeed(0);
      }
     
      // This line tells the drive function what speed and direction to move the motors in
      drive(xAxis, yAxis);
    } 
  }
}

// This function handles drive logic and actuation. Don't change this unless you know what you're doing.
void drive(int xAxis, int yAxis) {
  float V = (100 - abs(xAxis)) * (yAxis/100) + yAxis;    // This is where the X and Y axis inputs are converted into tank drive logic
  float W = (100 - abs(yAxis)) * (xAxis/100) + xAxis;
  velocityL = ((((V-W)/2)/100)*255);
  velocityR = ((((V+W)/2)/100)*255);

  mRight.run((velocityR >= 0) ? FORWARD : BACKWARD);     // These comands tell the motors what speed and direction to move at
  mRight.setSpeed(abs(velocityR));
  mLeft.run((velocityL >= 0) ? FORWARD : BACKWARD);
  mLeft.setSpeed(abs(velocityL));
}

//This function splits up the inbound package and returns whatever index you want from the split.
String getValue(String data, int index){
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==';' || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }
  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

