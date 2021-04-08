from .leds import LedsSoft

class LedsCustom(LedsSoft):  # pragma: no cover

    def __init__(self):
        super().__init__()
        strip = 'init'

    def do_set(self, led, red, green, blue):
        led_ix = led.value
        strip = 'do_set'

    def do_show(self):
        strip = 'show'
