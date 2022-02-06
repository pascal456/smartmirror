"""
last update on 20170603
- defines a motion sensor (PIR)
    - turns on the monitor when a motion is detected
    - turns off the monitor after a specified time
    - resets the timer when motion is detected while monitor is already on
- defines a led strip
    - turn on the led strip incrementally by percentage of given target colors
    - turns off the led strip after a specified time
    - resets the timer when motion is detected while led strip is already on
"""

import os
import sys
import subprocess
import time
from gpiozero import MotionSensor


"""
display configuration
"""
os.environ['DISPLAY'] = ":0"
SHUTOFF_DELAY = 180  # seconds
PIR_PIN = 4  # Pin 7 on the board

"""
LED strip configuration
"""
pin_red = '17'      # reference
pin_green = '22'    # reference
pin_blue = '24'     # reference
rgb = [250, 255, 30]  # color setting [red, green, blue], in a range of 0 to 255
red = 0             # temp value
green = 0           # temp value
blue = 0            # temp value
subprocess.call('sudo pigpiod', shell=True)  # start pigpio deamon


"""
**main function
program entrance...
"""


def main():
    pir = MotionSensor(PIR_PIN)
    turnDisplay_on()  # initially turn monitor on
    led_on()  # initially turn led strip on
    turned_off = False
    last_motion_time = time.time()

    while True:
        if pir.motion_detected:
            last_motion_time = time.time()
            print("info:", "Motion detected!")
            if turned_off:
                turned_off = False
                turnDisplay_on()
                led_on()
        else:
            if not turned_off and time.time() > (last_motion_time + SHUTOFF_DELAY):
                turned_off = True
                turnDisplay_off()
                led_off()
        time.sleep(1)
        print("debug-info -->", "time left:", SHUTOFF_DELAY -
              (time.time() - last_motion_time))


"""
**turnDisplay_on() function
- this function will turn the monitor on
"""


def turnDisplay_on():
    print("debug-info -->", "turn ON")
    subprocess.call('vcgencmd display_power 1', shell=True)


"""
**turnDisplay_off() function
- this function will turn the monitor off
"""


def turnDisplay_off():
    print("debug-info -->", "turn OFF")
    subprocess.call('vcgencmd display_power 0', shell=True)


"""
**led_on() function
- this function will turn on the LEDs (strip)
- it will generally be set the values from 0% to 100% of the color specified above
"""


def led_on():
    global red, green, blue
    percentage = 0
    while percentage < 101:
        red = int(rgb[0] * percentage / 100)
        green = int(rgb[1] * percentage / 100)
        blue = int(rgb[2] * percentage / 100)
        subprocess.call('pigs p ' + pin_red + ' ' + str(red) + ' && pigs p ' + pin_green +
                        ' ' + str(green) + ' && pigs p ' + pin_blue + ' ' + str(blue), shell=True)
        percentage += 1


"""
**led_off() function
this function will turn on the LEDs (strip)
it will generally be set the values from 0% to 100% of the color specified above
"""


def led_off():
    global red, green, blue
    percentage = 100
    while percentage >= 0:
        red = int(rgb[0] * percentage / 100)
        green = int(rgb[1] * percentage / 100)
        blue = int(rgb[2] * percentage / 100)
        subprocess.call('pigs p ' + pin_red + ' ' + str(red) + ' && pigs p ' + pin_green +
                        ' ' + str(green) + ' && pigs p ' + pin_blue + ' ' + str(blue), shell=True)
        percentage -= 1


if __name__ == '__main__':      # to make main() be called
    #print("info:","script starting")
    main()
