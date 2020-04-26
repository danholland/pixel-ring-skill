import time
from .colours import Colours, interpolate


class Pattern(object):
    def __init__(self, dev, num_pixels=12, brightness=100):
        self.dev = dev
        self.num_pixels = num_pixels
        self.stop = False
        self.brightness = brightness

    def spin(self, pixels, delay=0.3, brightness=100, positions=1):
        for led_num in range(self.num_pixels):
            rgb_colour = pixels[led_num % len(pixels)]
            self.dev.set_pixel(led_num, (rgb_colour & 0xFF0000) >> 16,
                               (rgb_colour & 0x00FF00) >> 8, rgb_colour & 0x0000FF,
                               brightness)
        for i in range(self.num_pixels):
            self.dev.show()
            time.sleep(delay)
            self.dev.rotate(positions)

    def fade(self, start, end=0x0, steps=10, delay=0.2, brightness=100):
        colours = interpolate(start, end, steps)
        for rgb_colour in colours:
            for led_num in range(self.num_pixels):
                self.dev.set_pixel(led_num, (rgb_colour & 0xFF0000) >> 16,
                                   (rgb_colour & 0x00FF00) >> 8, rgb_colour & 0x0000FF,
                                   brightness)
            self.dev.show()
            time.sleep(delay)

    def pulse(self, start, end=0x0, steps=10, delay=0.2, brightness=100):
        self.fade(start, end, steps, delay, brightness)
        self.fade(end, start, steps, delay, brightness)


class Echo(Pattern):
    def __init__(self, dev, num_pixels=12, brightness=100):
        super().__init__(dev=dev, num_pixels=num_pixels, brightness=brightness)

    def wakeup(self, direction=0):
        for b in range(0, self.brightness, int(self.brightness / 10)):
            for i in range(self.num_pixels):
                self.dev.set_pixel_rgb(i, Colours['purple'], b)
            dir_pixel = int((direction + 15) /
                            (360 / self.num_pixels)) % self.num_pixels
            self.dev.set_pixel_rgb(dir_pixel, Colours['aquamarine'], b)
            self.dev.show()
            time.sleep(0.1)

    def listen(self):
        while not self.stop:
            self.pulse(Colours['purple'])

    def think(self):
        pixels = [Colours['aquamarine'], Colours['purple']]
        half_brightness = int(self.brightness / 2)
        while not self.stop:
            self.spin(pixels, 0.3, half_brightness)

    def speak(self):
        while not self.stop:
            self.pulse(Colours['aquamarine'], Colours['purple'], 6, 0.1)

    def off(self):
        self.stop = True
        self.dev.clear_strip()
