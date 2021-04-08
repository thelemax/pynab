#!/home/pi/pynab/venv/bin/python

# Script executed at boot and at shutdown.
# At boot, set leds to orange.
# At shutdown, turn leds off.

from apa102_pi.driver import apa102
import sys


def set_leds(shutdown):
    LED_MOSI = 10 
    LED_SCLK = 11
    LED_BRIGHTNESS = 31
    LED_COUNT = 5

    strip = apa102.APA102(
        num_led=LedsAPA102.LED_COUNT, 
        mosi=LedsAPA102.LED_MOSI, 
        sclk=LedsAPA102.LED_SCLK, 
        order='rgb',
    )
    
    # Intialize the library (must be called once before other functions).
    strip.begin()

    if shutdown:
        color = (0 << 16) + (0 << 8) + (0)
    else:
        color = (255 << 16) + (0 << 8) + (255)

    for led in range(6):
        strip.set_pixel_rgb(led, color)

    strip.show()


def set_system_led(shutdown):
    # No need to set it at shutdown.
    # It will still blink multiple time after system halt even if it has been
    # disabled in Linux.
    if shutdown:
        return

    with open("/sys/class/leds/led0/trigger", "w") as f:
        f.write("none")

    with open("/sys/class/leds/led0/brightness", "w") as f:
        f.write("0")


if __name__ == "__main__":
    shutdown = len(sys.argv) > 1 and sys.argv[1] != "start"
    set_system_led(shutdown)
    set_leds(shutdown)
