import time
from .colours import Colours, interpolate


class Pattern(object):
    def __init__(self, dev, num_pixels=12, brightness=100):
        self.dev = dev
        self.num_pixels = num_pixels
        self.stop = True
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

    def dim(self, pixels, steps=10, delay=0.2, dir='out'):
        factor = int(self.brightness / steps)
        b = []
        if dir == 'out':
            for i in range(self.brightness, 0, -factor):
                b.append(i)
        else:
            for i in range(0, self.brightness, factor):
                b.append(i)
        self.dev.clear_strip()
        for j in b:
            for led_num in range(len(pixels)):
                self.dev.set_pixel_rgb(led_num, pixels[led_num], j)
            self.dev.show()
            time.sleep(delay)

    def off(self):
        self.stop = True
        self.dev.clear_strip()


class Echo(Pattern):
    def wakeup(self, direction=0):
        dir_pixel = int((direction + 15) /
                        (360 / self.num_pixels)) % self.num_pixels
        for b in range(0, self.brightness, int(self.brightness / 10)):
            for i in range(self.num_pixels):
                self.dev.set_pixel_rgb(i, Colours['purple'], b)
            self.dev.set_pixel_rgb(dir_pixel, Colours['aquamarine'], b)
            self.dev.show()
            time.sleep(0.1)

    def listen(self):
        while not self.stop:
            self.pulse(Colours['purple'])

    def think(self):
        pixels = [Colours['aquamarine'], Colours['purple'], Colours['purple']]
        half_brightness = int(self.brightness / 2)
        while not self.stop:
            self.spin(pixels, 0.5, half_brightness)

    def speak(self):
        while not self.stop:
            self.pulse(Colours['aquamarine'], Colours['purple'], 6, 0.1)


class Google(Pattern):
    base_pixels = [
        Colours['red'],
        Colours['black'],
        Colours['black'],
        Colours['yellow'],
        Colours['black'],
        Colours['black'],
        Colours['green'],
        Colours['black'],
        Colours['black'],
        Colours['blue'],
        Colours['black'],
        Colours['black'],
    ]

    def wakeup(self, direction=0):
        for led_num in range(self.num_pixels):
            self.dev.set_pixel_rgb(
                led_num, self.base_pixels[led_num], self.brightness)
        self.dev.show()

    def listen(self):
        pixels = self.base_pixels
        factor = int(self.brightness / 10)
        while not self.stop:
            for b in range(self.brightness, 0, -factor):
                for led_num in range(self.num_pixels):
                    self.dev.set_pixel_rgb(
                        led_num, pixels[led_num], b)
                self.dev.show()
                pixels = self.rotate(pixels)
                time.sleep(0.05)
            for b in range(0, self.brightness, factor):
                for led_num in range(self.num_pixels):
                    self.dev.set_pixel_rgb(
                        led_num, pixels[led_num], b)
                self.dev.show()
                pixels = self.rotate(pixels)
                time.sleep(0.05)

    def think(self):
        while not self.stop:
            self.spin(self.base_pixels, 0.05)

    def speak(self):
        while not self.stop:
            self.dim(self.base_pixels, delay=0.05, dir='in')
            self.dim(self.base_pixels, delay=0.05, dir='out')

    def rotate(self, pixels):
        tmp = pixels[-1]
        for i in range(len(pixels)-1, 0, -1):
            pixels[i] = pixels[i-1]
        pixels[0] = tmp
        return pixels
