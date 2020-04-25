import time
from .colours import Colours, fade


class Echo():
    def __init__(self, num_pixels=12):
        self.num_pixels = num_pixels
        self.stop = False
        self.brightness = 100

    def wakeup(self, direction=0):
        for b in range(0, self.brightness, self.brightness / 10):
            for i in range(self.num_pixels):
                self.dev.set_pixel_rgb(i, Colours['pruple'], b)
            dir_pixel = int((direction + 15) /
                            (360 / self.num_pixels)) % self.num_pixels
            self.dev.set_pixel_rgb(dir_pixel, Colours['aquamarine'], b)
            self.dev.show()
            time.sleep(0.1)

    def listen(self):
        while not self.stop:
            for b in range(0, self.brightness, int(self.brightness/10)):
                for i in range(self.num_pixels):
                    self.dev.set_pixel_rgb(i, Colours['pruple'], b)
                self.dev.show()
                time.sleep(0.1)
            for b in range(self.brightness, 0, int(-self.brightness/10)):
                for i in range(self.num_pixels):
                    self.dev.set_pixel_rgb(i, Colours['pruple'], b)
                self.dev.show()
                time.sleep(0.1)

    def think(self):
        half_brightness = int(self.brightness / 2)
        for i in range(self.num_pixels):
            if i % 2 == 0:
                self.dev.set_pixel_rgb(
                    i, Colours['purple'], half_brightness)
            else:
                self.dev.set_pixel_rgb(
                    i, Colours['aquamarine', half_brightness])
        while not self.stop:
            self.dev.show()
            time.sleep(0.4)
            self.dev.rotate()

    def speak(self):
        colours = fade(Colours['aquamarine'], Colours['purple'], 6)
        while not self.stop:
            for colour in colours:
                for i in range(self.num_pixels):
                    self.dev.set_pixel_rgb(i, colour)
                self.dev.show()
                time.sleep(0.1)
            for colour in reversed(colours):
                for i in range(self.num_pixels):
                    self.dev.set_pixel_rgb(i, colour)
                self.dev.show()
                time.sleep(0.1)
