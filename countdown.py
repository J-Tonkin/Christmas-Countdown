# Using rpi_ws281x library
# Author: Tony DiCola (tony@tonydicola.com)


import time
from rpi_ws281x import *
import argparse
import datetime
import math

# LED strip configuration:
LED_COUNT      = 28      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def GetRow(seg,disp):
    offset = disp*14
    if (seg == 0):
        leds = [0,13]
    if (seg == 1):
        leds = [1,12]
    if (seg == 2):
        leds = [2,11]
    if (seg == 3):
        leds = [3,10]
    if (seg == 4):
        leds = [4,9]
    if (seg == 5):
        leds = [5,8]
    if (seg == 6):
        leds = [6,7]
    return [z+offset for z in leds]

def GetPinwheel(seg,disp):
    offset = disp*14
    if (seg == 0):
        leds = [6,13]
    if (seg == 1):
        leds = [5,12]
    if (seg == 2):
        leds = [4,11]
    if (seg == 3):
        leds = [3,10]
    if (seg == 4):
        leds = [2,9]
    if (seg == 5):
        leds = [1,8]
    if (seg == 6):
        leds = [0,7]
    return [z+offset for z in leds]

def DigitToLed(num,disp):
    offset = disp*14
    if (num == 0):
        leds = [1,2,4,5,6,7,8,9,11,12,13,0]
    if (num == 1):
        leds = [8,9,11,12]
    if (num == 2):
        leds = [0,3,4,5,6,7,10,11,12,13]
    if (num == 3):
        leds = [0,3,6,7,8,9,10,11,12,13]
    if (num == 4):
        leds = [1,2,3,8,9,10,11,12]
    if (num == 5):
        leds = [0,1,2,3,6,7,8,9,10,13]
    if (num == 6):
        leds = [0,1,2,3,4,5,6,7,8,9,10,13]
    if (num == 7):
        leds = [0,8,9,11,12,13]
    if (num == 8):
        leds = [1,2,3,4,5,6,7,8,9,10,11,12,13,0]
    if (num == 9):
        leds = [1,2,3,6,7,8,9,10,11,12,13,0]
    return [z+offset for z in leds]

def DIGIT(state,num,disp,r,g,b):
    leds = DigitToLed(num,disp)
    offset = disp*14
    dispLeds = [z+offset for z in range(0,13,1)]
    for led in dispLeds:
        strip.setPixelColor(led,Color(0,0,0))
        state[led] = 0
    for led in leds:
        strip.setPixelColor(led,Color(r,g,b))
        state[led] = 1
    return state

def UpAndDown(r,g,b):
    print("Running Vertical Swipe")
    leds = []
    prevRow = []
    for disp in range(math.floor(LED_COUNT/14)):
        prevRow = []
        for seg in range (7):
            prevRow = leds
            leds = GetRow(seg,disp)
            for led in leds:
                strip.setPixelColor(led,Color(r,g,b))
            if(seg != 0):
                for led in prevRow:
                    strip.setPixelColor(led,Color(0,0,0))
            strip.show()
            time.sleep(.1)
        for seg in range (6,-1,-1):
            prevRow = leds
            leds = GetRow(seg,disp)
            for led in leds:
                strip.setPixelColor(led,Color(r,g,b))
            for led in prevRow:
                if (state[led]):
                    strip.setPixelColor(led,Color(r,g,b))
                else :
                    strip.setPixelColor(led,Color(0,0,0))
            strip.show()
            time.sleep(.1)
        prevRow = leds
        for led in prevRow:
            if (state[led]):
                strip.setPixelColor(led,Color(r,g,b))
            else :
                strip.setPixelColor(led,Color(0,0,0))
        strip.show()

def Rotate(r,g,b):
    print("Running Rotate")
    leds = []
    prevRow = []
    for disp in range(math.floor(LED_COUNT/14)):
        prevRow = []
        for seg in range (7):
            prevRow = leds
            leds = GetPinwheel(seg,disp)
            for led in leds:
                strip.setPixelColor(led,Color(r,g,b))
            if(seg != 0):
                for led in prevRow:
                    strip.setPixelColor(led,Color(0,0,0))
            strip.show()
            time.sleep(.1)
        for seg in range (6,-1,-1):
            prevRow = leds
            leds = GetPinwheel(seg,disp)
            for led in leds:
                strip.setPixelColor(led,Color(r,g,b))
            for led in prevRow:
                if (state[led]):
                    strip.setPixelColor(led,Color(r,g,b))
                else :
                    strip.setPixelColor(led,Color(0,0,0))
            strip.show()
            time.sleep(.1)
        prevRow = leds
        for led in prevRow:
            if (state[led]):
                strip.setPixelColor(led,Color(r,g,b))
            else :
                strip.setPixelColor(led,Color(0,0,0))
        strip.show()

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()

    dt = datetime.datetime
    prevTime = dt.now()
    state = []
    for x in range(LED_COUNT):
        state.append(0)

    try:

        while True:
            #for j in range(0,10,1):
            #    DIGIT(j)
            #    strip.show()
            #    time.sleep(1)
            now = dt.now()
            timeLeft = dt(year = 2021, month = 12, day = 25) - dt(year=now.year, month=now.month, day=now.day)
            print("Days left until Christmas:")
            print(timeLeft.days)
            digitList = [int(i) for i in str(timeLeft.days)]
            display = 0
            for n in digitList:
                DIGIT(state,n,display,0,255,0)
                display = display + 1
            strip.show()
            time.sleep(5)
            Rotate(255,0,0)
            time.sleep(5)

            now = dt.now()
            timeLeft = dt(year = 2021, month = 12, day = 25) - dt(year=now.year, month=now.month, day=now.day)
            print("Days left until Christmas:")
            print(timeLeft.days)
            digitList = [int(i) for i in str(timeLeft.days)]
            display = 0
            for n in digitList:
                DIGIT(state,n,display,255,0,0)
                display = display + 1
            strip.show()
            time.sleep(5)
            UpAndDown(0,255,0)
            time.sleep(5)


    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)
