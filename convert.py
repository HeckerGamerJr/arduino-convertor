# Example Python code
## NOTE: YOU MAY NEED TO INSTALL MODULES FOR I2C DISPLAY OR OLED
## EXAMPLE UPLOAD COMMAND (uses CLI - old bootloader): arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328old [sketch_name]
import time

led_pin = 13
# 1 pin connected to GND and other connected to a pin (eg: D5)
button_pin = 5  # D5 pin example

########## I2C Display Configuration ##########
# Hardware connections (hardcoded - change in code for different setup):
# VCC → 5V
# GND → GND  
# SDA → A4 (Arduino pin)
# SCL → A5 (Arduino pin)

lcd_address = 0x27  # I2C address - may depend on your LCD module
lcd_cols = 16
lcd_rows = 2

########## For OLED (alternative) ##########
# oled_address = 0x3C  # Common OLED I2C address - may depend on your OLED module
# oled_width = 128
# oled_height = 64

def setup():
    # Initialize pins
    pinMode(led_pin, "OUTPUT")
    pinMode(button_pin, "INPUT_PULLUP")  # Use internal pull-up resistor
    
    # Initialize screen
    lcd_init(lcd_address, lcd_cols, lcd_rows)
    lcd_clear()
    lcd_print("Arduino Ready")
    lcd_set_cursor(0, 1)  # Second line
    lcd_print("Press button...")

def loop():
    # Main loop - runs forever
    if digitalRead(button_pin):
        digitalWrite(led_pin, True)
        lcd_clear()
        lcd_print("Button Pressed")
        lcd_set_cursor(0, 1)
        lcd_print("LED ON")
        time.sleep(0.5)
        
        digitalWrite(led_pin, False)
        lcd_clear()
        lcd_print("Button Released")
        lcd_set_cursor(0, 1)
        lcd_print("LED OFF")
        time.sleep(0.5)
    else:
        digitalWrite(led_pin, False)

# Arduino style functions 
def pinMode(pin, mode):
    pass

def digitalWrite(pin, value):
    pass

def digitalRead(pin):
    return True

# Screen functions
def lcd_init(address, cols, rows):
    pass

def lcd_clear():
    pass

def lcd_print(text):
    pass

def lcd_set_cursor(col, row):
    pass

def oled_init(width, height):
    pass

def oled_clear():
    pass

def oled_print(text, x, y):
    pass