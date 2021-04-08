#https://pimylifeup.com/raspberry-pi-led-strip-apa102/
#https://github.com/tinue/apa102-pi/blob/main/sample.py
#import logging

from apa102_pi.driver import apa102
from .leds import LedsSoft

class LedsAPA102(LedsSoft):  # pragma: no cover
    LED_MOSI = 10 
    LED_SCLK = 11
    LED_BRIGHTNESS = 31
    LED_COUNT = 5

    def __init__(self):
        super().__init__()
        #logging.debug("APA102 - init {a}".format(a=0xFF00FF))
        self.strip = apa102.APA102(
          num_led=LedsAPA102.LED_COUNT, 
          mosi=LedsAPA102.LED_MOSI, 
          sclk=LedsAPA102.LED_SCLK, 
          order='rgb',
        )
        self.strip.set_global_brightness(LedsAPA102.LED_BRIGHTNESS)
        self.strip.clear_strip()
        
    def do_set(self, led, red, green, blue):
        led_ix = led.value
        color = (red << 16) + (green << 8) + (blue);
        #logging.debug("APA102 - do_set - {a} ({b} {c} {d} --> {e})".format(a=led_ix, b=red, c=green, d=blue, e=color))
        self.strip.set_pixel_rgb(led_ix, color)

    def do_show(self):
        #logging.debug("APA102 - show");
        self.strip.show()

