#include <Adafruit_NeoPixel.h>

#define PIN 6
Adafruit_NeoPixel strip = Adafruit_NeoPixel(30, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(115200);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  
  delay(100);
  String control = "KBCGYRMKBCGYRMKBCGYRMKBCGYRMKBC\n";
  colorSet(control);
}

void loop() {
  // Wait for control message from Python
  if(Serial.available() > 0) {
    
    delay(1);   // allow buffer to fill
    char c = 'M';
    String control = "";
    
    while(c != '\n') {
        c = Serial.read();
        control = control + c;
    }
    
//    // Test to see message length
//    uint8_t len = control.length();
//    uint8_t hundreds = len/100;
//    len = len - hundreds*100;
//    uint8_t tens = len/10;
//    uint8_t ones = len - tens*10;
//    
//    String control2 = "KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK\n";
//    control2.setCharAt(hundreds, 'R');
//    control2.setCharAt(tens, 'G');
//    control2.setCharAt(ones, 'B');
//    colorSet(control2);
    
    colorSet(control);
  }

  delay(10);
}

// Assign colors to LED's from Python message
void colorSet(String control) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      switch(control.charAt(i)) {
        case 'W':
            strip.setPixelColor(i, strip.Color(255, 255, 255));
            break;
        case 'K':
            strip.setPixelColor(i, strip.Color(0, 0, 0));
            break;
        case 'B':
            strip.setPixelColor(i, strip.Color(0, 0, 255));
            break;
        case 'C':
            strip.setPixelColor(i, strip.Color(0, 255, 255));
            break;
        case 'G':
            strip.setPixelColor(i, strip.Color(0, 255, 0));
            break;
        case 'Y':
            strip.setPixelColor(i, strip.Color(255, 255, 0));
            break;
        case 'R':
            strip.setPixelColor(i, strip.Color(255, 0, 0));
            break;
        case 'M':
            strip.setPixelColor(i, strip.Color(255, 0, 255));
            break;
      }
  }
  strip.show();
}





