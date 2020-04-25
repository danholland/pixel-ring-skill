from .apa102 import APA102
from .patterns import Echo
import time
import threading
try:
    import queue as Queue
except ImportError:
    import Queue as Queue


class PixelRing(object):
    PIXELS_N = 12

    def __init__(self, pattern='google'):
        self.dev = APA102(num_led=self.PIXELS_N)
        self.pattern = Echo()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        self.off()

    def set_brightness(self, brightness):
        if brightness > 100:
            brightness = 100

        if brightness > 0:
            self.dev.global_brightness = int(0b11111 * brightness / 100)

    def wakeup(self, direction=0):
        self.pattern.wakeup(direction)

    def listen(self):
        self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)


    def off(self)
        self.pattern.stop = False
        self.dev.clear_strip()
