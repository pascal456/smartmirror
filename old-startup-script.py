"""Startup Script to control the Light and monitor states.

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
import subprocess
import time
from gpiozero import MotionSensor


# Display configuration
os.environ['DISPLAY'] = ":0"
SHUTOFF_DELAY = 180  # seconds
PIR_PIN = 4  # Pin 7 on the board

# LED strip configuration
PIN_RED = '17'      # GPIO pin reference (Broadcom)
PIN_GREEN = '22'    # GPIO pin reference (Broadcom)
PIN_BLUE = '24'     # GPIO pin reference (Broadcom)
RGB = [250, 255, 30]  # color setting [red, green, blue], in a range of 0 to 255
STATE_RED = 0
STATE_GREEN = 0
STATE_BLUE = 0


def main():
    """Start main procedure."""
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
        print("debug-info -->", "time left:",
              SHUTOFF_DELAY - (time.time() - last_motion_time))


def turnDisplay_on():
    """Turn display on.

    Turns on the physical monitor display connected via HDMI interface.
    """
    subprocess.call('vcgencmd display_power 1', shell=True)


def turnDisplay_off():
    """Turn display off.

    Turns off the physical monitor display connected via HDMI interface.
    """
    subprocess.call('vcgencmd display_power 0', shell=True)


def led_on():
    """Turn LEDs on.

    This function will turn on the LEDs (strip).
    It will gradually be set the values from 0% to 100% of the color specified above.
    """
    global STATE_RED, STATE_GREEN, STATE_BLUE
    percentage = 0
    while percentage < 101:
        STATE_RED = int(RGB[0] * percentage / 100)
        STATE_GREEN = int(RGB[1] * percentage / 100)
        STATE_BLUE = int(RGB[2] * percentage / 100)
        subprocess.call((f'pigs p {PIN_RED} {str(STATE_RED)}'
                         f' && pigs p {PIN_GREEN} {str(STATE_GREEN)}'
                         f' && pigs p {PIN_BLUE} {str(STATE_BLUE)}'),
                        shell=True)
        percentage += 1


def led_off():
    """Turn LEDs on.

    This function will turn off the LEDs (strip).
    It will gradually be set the values from 0% to 100% of the color specified above.
    """
    global STATE_RED, STATE_GREEN, STATE_BLUE
    percentage = 100
    while percentage >= 0:
        STATE_RED = int(RGB[0] * percentage / 100)
        STATE_GREEN = int(RGB[1] * percentage / 100)
        STATE_BLUE = int(RGB[2] * percentage / 100)
        subprocess.call((f'pigs p {PIN_RED} {str(STATE_RED)}'
                         f' && pigs p {PIN_GREEN} {str(STATE_GREEN)}'
                         f' && pigs p {PIN_BLUE} {str(STATE_BLUE)}'),
                        shell=True)
        percentage -= 1


if __name__ == '__main__':
    subprocess.call('sudo pigpiod', shell=True)  # start pigpio deamon
    main()
