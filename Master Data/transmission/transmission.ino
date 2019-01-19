#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"

#include <Wire.h>

int address = 0x28; // 28 is the address
byte byte1, byte2, byte3, byte4;

RF24 radio (8, 10);

struct dataStruct {
  int table;
  char teamName;
  char response;
} transmitter1_data;

unsigned char ADDRESS0[5]  =
{
  0xb1, 0x43, 0x88, 0x99, 0x45
}; // Define a static TX address

void setup()
{
  radio.begin();

  // When you do control shift m, (or command shift m), you must set your baud rate to 115200.
  Serial.begin(115200);
  printf_begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setRetries(1, 1);
  radio.enableDynamicPayloads();
  radio.setDataRate(RF24_250KBPS);
  radio.openWritingPipe(ADDRESS0);
  radio.openReadingPipe(0, ADDRESS0);
  radio.stopListening();

  radio.printDetails();
  int buttonNr = 0;
  pinMode(2, INPUT);           // set pin to input
  pinMode(3, INPUT);           // set pin to input
  pinMode(4, INPUT);           // set pin to input
  pinMode(5, INPUT);           // set pin to input
  digitalWrite(2, HIGH);       // turn on pullup resistors
  digitalWrite(3, HIGH);       // turn on pullup resistors
  digitalWrite(4, HIGH);       // turn on pullup resistors
  digitalWrite(5, HIGH);       // turn on pullup resistors
  Serial.println("Configured as a transmitter.");
}

void loop()
{
  /*
  	TODO:
  		Set your team name by setting transmitter1_data.teamName      --- MUST BE 6 CHARACTERS OR LESS!
  		Set transmitter1_data.table table number to the number written on your bag

  */

  transmitter1_data.table = 48;



  while (digitalRead(2) != 0 && digitalRead(3) != 0 && digitalRead(4) != 0 && digitalRead(5) != 0)
  {
    //  After arduino boots, it loads the loop() continuously. Since we want to detect when the D2, D3, D4, D5 pins are grounded, we want to loop on these reads rapidly until a change is detected
    //  To do this, we run an infinite loop until a digital read equals 0.
    //
    delay(20);
  }


  /*
  	TODO:
  		Use logic to send a, b, c, d, depending on the pin that equals 0.

  		Pseudo Code: if d2 equals 0, set transmitter1_data.response equal to the character a

  		Requirements:   Responses can only be a single character
  						Responses should be all lower case
  						Responses should be set to a b c or d

  		Additional Tips:
  			In another project, I wanted to read pin D9 to see if it was grounded out. I used     if (digitalRead(9)==0).

  			To send the data to my radio, here's the code:   bool ok=radio.write(&transmitter1_data, sizeof(transmitter1_data));
  			Don't change that single line or you'll see bad things.  Simply copy that line after you set all the stuff and send it over!

  			I'd strongly recommend you use these lines to help debug your code:

  			String test = "Table: " + String(transmitter1_data.table) + "\tTeam Name: " + String(transmitter1_data.teamName) + "\tResponse: " + String(transmitter1_data.response) + "";
  			Serial.println(test);

  			Check the struct at the top of this file to see the data I need!
  */
  if (digitalRead(2) == 1) {
    transmitter1_data.response = 'a';
  }
  else if (digitalRead(3) == 1) {
    transmitter1_data.response = 'b';
  }
  else if (digitalRead(4) == 1) {
    transmitter1_data.response = 'c';
  }
  else if (digitalRead(5) == 1) {
    transmitter1_data.response = 'd';
  }
  bool ok=radio.write(&transmitter1_data, sizeof(transmitter1_data));
  // Don't remove this line.
  String test = "Table: " + String(transmitter1_data.table) + "\tTeam Name: " + String(transmitter1_data.teamName) + "\tResponse: " + String(transmitter1_data.response) + "";
  Serial.println(test);
  delay(30);
}
