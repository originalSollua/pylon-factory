import time
import subprocess
import RPi.GPIO as gpio
import Adafruit_ADS1x15
import Adafruit_CharLCD as LCD
#from tsl2561 import TSL2561

pinFan = 0
fanOn = False
GAIN = 1
adc = Adafruit_ADS1x15.ADS1115()
j = [0, 0, 0, 0]
i = 0
lcd = None
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 27
lcd_d7 = 22
pin_LED = 4
lcd_rows = 4
lcd_cols = 20
lcd_list = [' ', ' ', ' ', ' ']

def initPylonIO():
    global pinFan
    global lcd
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    pinFan = 21
    gpio.setup(pinFan, gpio.OUT, initial=gpio.LOW)
    gpio.setup(pin_LED, gpio.OUT, initial=gpio.LOW)
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_cols, lcd_rows)

def readCoreTemp():
    result = subprocess.check_output(['cat','/sys/class/thermal/thermal_zone0/temp'])
    return result

def lcdLog(msg):
    global lcd_list

    lcd_list.append(msg)
    del lcd_list[0]

def lcdTick():
    global lcd
    global lcd_list
    global j
    global i
    longArr = [False, False, False, False]
    message = ""
    for m in lcd_list:
        message = message+(m.ljust(19))
    lcd.message(message)

    
def activateFan():
    global pinFan
    global fanOn
    gpio.output(pinFan, gpio.HIGH)
    gpio.output(pin_LED, gpio.HIGH)
    fanOn = True

def deactivateFan():
    global pinFan
    global fanOn
    gpio.output(pinFan, gpio.LOW)
    gpio.output(pin_LED, gpio.LOW)
    fanOn = False

def getExternalTemp():
    value = adc.read_adc(0, gain=GAIN)
    tempc = ((value*3.3)/1024.0)-0.5
    return tempc
