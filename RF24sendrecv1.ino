#include<SPI.h>
#include<RF24.h>

//ce. csn pins
RF24 radio(9, 10);

int buttonPin = 3;
int ledPin = 2;
int x;

void setup(void) {
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);
  while (!Serial);
  Serial.begin(9600);

  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  const uint64_t pipe = 0xE8E8F0F0E1LL;
  radio.openReadingPipe(1, pipe);

  radio.enableDynamicPayloads();
  radio.powerUp();

}

void loop() {
  radio.startListening();
  Serial.println("Starting Loop, Radio on 1P.");
  char receivedMessage[32] = {0};
  if (radio.available()) {
    radio.read(receivedMessage, sizeof(receivedMessage));
    Serial.print("Received Message: ");
    Serial.println(receivedMessage);
    Serial.println("Turning off the radio.");
    radio.stopListening();

    String stringMessage(receivedMessage);

// Actual action if asked for button press
    if (stringMessage == "1P") {
      digitalWrite(ledPin,HIGH);

      while (digitalRead(buttonPin) == HIGH){
            }
      digitalWrite(ledPin, LOW);      
      Serial.println("looks like they want a string");
      const char text[] = "Node 1P - Hello";
      radio.write(text, sizeof(text));
      Serial.println("We sent our message: " + String(text));
    }

// Test scenario    
    if (stringMessage == "TEST") {
      for(x=0; x < 5; x++){
      digitalWrite(ledPin,HIGH); 
      delay(500);
      digitalWrite(ledPin, LOW);
      delay(500);
      }
      Serial.println("Test completed");
      const char text[] = "Test done";
      radio.write(text, sizeof(text));
      Serial.println("We sent our message: " + String(text));
    
    }

  }

  delay(100);
}

