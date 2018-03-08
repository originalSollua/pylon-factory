import time
import subprocess
import RPi.GPIO as gpio
#from tsl2561 import TSL2561

pinFan = 0
fanOn = False

def initPylonIO():
    global pinFan
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    pinFan = 21

    gpio.setup(pinFan, gpio.OUT, initial=gpio.LOW)

def readCoreTemp():
    result = subprocess.check_output(['cat','/sys/class/thermal/thermal_zone0/temp'])
    return result

def activateFan():
    global pinFan
    global fanOn
    gpio.output(pinFan, gpio.HIGH)
    fanOn = True

def deactivateFan():
    global pinFan
    global fanOn
    gpio.output(pinFan, gpio.LOW)
    fanOn = False

