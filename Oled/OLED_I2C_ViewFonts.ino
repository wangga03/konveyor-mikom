

#include <OLED_I2C.h>

OLED  myOLED(SDA, SCL); // Remember to add the RESET pin if your display requires it...

extern uint8_t SmallFont[];
extern uint8_t TinyFont[];
extern uint8_t BigNumbers[];

void setup()
{
  if(!myOLED.begin(SSD1306_128X32))
    while(1);   // In case the library failed to allocate enough RAM for the display buffer...
}

void loop()
{
  float i = 10.0;
  myOLED.setFont(BigNumbers);
  myOLED.clrScr();
  myOLED.printNumF(10, 0, CENTER, 1);
  myOLED.update();
  delay (5000);

}


