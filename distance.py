#Libraries
import RPi.GPIO as GPIO
import time
import pygame
from time import sleep
import Adafruit_CharLCD as LCD

#Initialise pygame and the mixer
pygame.init()
pygame.mixer.init()

#load the sound file
mysound = pygame.mixer.Sound("/home/pi/Downloads/beep-04.wav")

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 4


lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


GPIO_TRIGGER = 4
GPIO_ECHO = 27
LED=5

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(LED,GPIO.OUT)

def distance():

    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()


    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()


    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    TimeElapsed = StopTime - StartTime

    distance = (TimeElapsed * 34300) / 2

    return distance
def LED_on():
    GPIO.output(LED,True)
def LED_blink():
     GPIO.output(LED,True)
     sleep(1)
     GPIO.output(LED,False)
def LED_off():
     GPIO.output(LED,False)

if __name__ == '__main__':
    try:

	lcd.clear()
        while True:
            dist = distance()
	    lcd.clear()
	    lcd.message("distance:%.1f cm" %dist)

            print ("Measured Distance = %.1fcm" % dist)

            if (dist<=5):
		#GPIO.output(LED,True)
                LED_blink()
		mysound.play()

	    if(dist>5 and dist<10):
                LED_on()
	    else:
                GPIO.output(LED,False)

            time.sleep(2)

    except KeyboardInterrupt:
        print("stopped")
        GPIO.cleanup()
