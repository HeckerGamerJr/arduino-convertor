// Simple Arduino Nano test with LCD
#include <LiquidCrystal_I2C.h>

// I2C LCD connections: VCC->5V, GND->GND, SDA->A4, SCL->A5
LiquidCrystal_I2C lcd(0x27, 16, 2);

int led_pin = 13;
int button_pin = 5;

void setup() {
  pinMode(led_pin, OUTPUT);
  pinMode(button_pin, INPUT_PULLUP);
  
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.print("Arduino Ready!");
  lcd.setCursor(0, 1);
  lcd.print("Press button...");
}

void loop() {
  if (digitalRead(button_pin) == LOW) {  // Button pressed
    digitalWrite(led_pin, HIGH);
    lcd.clear();
    lcd.print("Button Pressed!");
    lcd.setCursor(0, 1);
    lcd.print("LED ON");
    delay(500);
    
    digitalWrite(led_pin, LOW);
    lcd.clear();
    lcd.print("Button Released");
    lcd.setCursor(0, 1);
    lcd.print("LED OFF");
    delay(500);
  } else {
    digitalWrite(led_pin, LOW);
  }
}
