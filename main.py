#!/usr/bin/env python3

import ast
import re

class PythonToArduinoConverter:
    def __init__(self):
        self.arduino_code = []
        self.variables = {}
        self.functions = {}
        
    def convert_file(self, input_file="convert.py", output_file="output.ino"):
        try:
            with open(input_file, 'r') as f:
                python_code = f.read()
            
            arduino_code = self.convert_python_to_arduino(python_code)
            
            with open(output_file, 'w') as f:
                f.write(arduino_code)
            
            print(f"Converted {input_file} to {output_file}")
            print("\n" + "="*50)
            print("GENERATED ARDUINO CODE:")
            print("="*50)
            print(arduino_code)
            
        except Exception as e:
            print(f"rror converting file: {e}")
    
    def convert_python_to_arduino(self, python_code):
        lines = python_code.split('\n')
        arduino_code = []
        
        arduino_code.append("// Created in Python - converted to Arduino")
        arduino_code.append("")
        
        if 'lcd_' in python_code:
            lcd_addr = "0x27"
            if 'lcd_address' in python_code:
                import re
                addr_match = re.search(r'lcd_address\s*=\s*(0x[0-9A-Fa-f]+)', python_code)
                if addr_match:
                    lcd_addr = addr_match.group(1)
            
            arduino_code.append("#include <LiquidCrystal_I2C.h>")
            arduino_code.append("// I2C LCD connections: VCC->5V, GND->GND, SDA->A4, SCL->A5")
            arduino_code.append(f"LiquidCrystal_I2C lcd({lcd_addr}, 16, 2);")
            arduino_code.append("")
        
        if 'oled_' in python_code:
            oled_addr = "0x3C"
            if 'oled_address' in python_code:
                import re
                addr_match = re.search(r'oled_address\s*=\s*(0x[0-9A-Fa-f]+)', python_code)
                if addr_match:
                    oled_addr = addr_match.group(1)
            
            arduino_code.append("#include <Adafruit_GFX.h>")
            arduino_code.append("#include <Adafruit_SSD1306.h>")
            arduino_code.append("// I2C OLED connections: VCC->5V, GND->GND, SDA->A4, SCL->A5")
            arduino_code.append(f"Adafruit_SSD1306 display(128, 64, &Wire, -1);")
            arduino_code.append("")
        
        setup_code = []
        loop_code = []
        global_vars = []
        
        in_setup = False
        in_loop = False
        current_function = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('#') or line.startswith('import') or not line:
                continue
            
            if line.startswith('def setup()'):
                in_setup = True
                current_function = 'setup'
                continue
            elif line.startswith('def loop()'):
                in_loop = True
                current_function = 'loop'
                continue
            elif line.startswith('def ') and 'pinMode' in line or 'digitalWrite' in line or 'digitalRead' in line:
                continue
            
            if '=' in line and not line.startswith('def') and not 'if' in line:
                var_line = self.convert_variable(line)
                if current_function is None:
                    global_vars.append(var_line)
                elif in_setup:
                    setup_code.append('    ' + var_line)
                elif in_loop:
                    loop_code.append('    ' + var_line)
            
            elif current_function:
                converted_line = self.convert_line(line)
                if converted_line:
                    if in_setup:
                        setup_code.append('    ' + converted_line)
                    elif in_loop:
                        loop_code.append('    ' + converted_line)
        
        arduino_code.extend(global_vars)
        arduino_code.append("")
        arduino_code.append("void setup() {")
        arduino_code.extend(setup_code)
        arduino_code.append("}")
        arduino_code.append("")
        arduino_code.append("void loop() {")
        arduino_code.extend(loop_code)
        arduino_code.append("}")
        
        return '\n'.join(arduino_code)
    
    def convert_variable(self, line):
        if '=' in line and not line.startswith('def'):
            var_name, value = line.split('=', 1)
            var_name = var_name.strip()
            value = value.strip()
            
            if '#' in value:
                value = value.split('#')[0].strip()
            
            if value.isdigit():
                return f"int {var_name} = {value};"
            elif value.replace('.', '').isdigit():
                return f"float {var_name} = {value};"
            elif value in ['True', 'False']:
                arduino_value = 'true' if value == 'True' else 'false'
                return f"bool {var_name} = {arduino_value};"
            elif value.startswith('"') or value.startswith("'"):
                return f"String {var_name} = {value};"
            else:
                return f"int {var_name} = {value};"
        
        return line
    
    def convert_line(self, line):
        if 'time.sleep(' in line:
            delay_value = re.search(r'time\.sleep\(([^)]+)\)', line)
            if delay_value:
                seconds = float(delay_value.group(1))
                milliseconds = int(seconds * 1000)
                return f"delay({milliseconds});"
        
        if 'digitalWrite(' in line:
            line = line.replace('True', 'HIGH').replace('False', 'LOW')
            return line + ';' if not line.endswith(';') else line
        
        if 'pinMode(' in line:
            line = line.replace('"OUTPUT"', 'OUTPUT').replace('"INPUT"', 'INPUT')
            line = line.replace("'OUTPUT'", 'OUTPUT').replace("'INPUT'", 'INPUT')
            line = line.replace('"INPUT_PULLUP"', 'INPUT_PULLUP').replace("'INPUT_PULLUP'", 'INPUT_PULLUP')
            return line + ';' if not line.endswith(';') else line
        
        if 'digitalRead(' in line:
            return line + ';' if not line.endswith(';') else line
        
        if 'lcd_init(' in line:
            return line.replace('lcd_init', 'lcd.begin') + ';' if not line.endswith(';') else line
        
        if 'lcd_clear(' in line:
            return 'lcd.clear();'
        
        if 'lcd_print(' in line:
            return line.replace('lcd_print', 'lcd.print') + ';' if not line.endswith(';') else line
        
        if 'lcd_set_cursor(' in line:
            return line.replace('lcd_set_cursor', 'lcd.setCursor') + ';' if not line.endswith(';') else line
        
        if 'oled_init(' in line:
            return 'display.begin(SSD1306_SWITCHCAPVCC, 0x3C);'
        
        if 'oled_clear(' in line:
            return 'display.clearDisplay(); display.display();'
        
        if 'oled_print(' in line:
            match = re.search(r'oled_print\(([^,]+),\s*(\d+),\s*(\d+)\)', line)
            if match:
                text, x, y = match.groups()
                return f'display.setCursor({x}, {y}); display.print({text}); display.display();'
        
        if line.startswith('if '):
            line = line.replace(':', ' {')
            return line
        
        if line == 'else:':
            return '} else {'
        
        if line and not line.startswith('if') and not line.startswith('else'):
            pass
        
        return line

def main():
    converter = PythonToArduinoConverter()
    converter.convert_file("convert.py", "output.ino")

main()
