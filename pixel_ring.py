from .apa102 import APA102
from .patterns import Echo
import time
from mycroft.util.log import LOG
import threading
try:
    import queue as Queue
except ImportError:
    import Queue as Queue


class PixelRing(object):
    PIXELS_N = 12

    def __init__(self, pattern='echo'):
        LOG.debug("Init PixelRing core")
        self.dev = APA102(num_led=self.PIXELS_N)
        self.pattern = Echo(dev=self.dev)
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

    def change_pattern(self, pattern='echo'):
        LOG.debug("PixelRing changing pattern to " + pattern)
        pass

    def wakeup(self, direction=0):
        LOG.debug("PixelRing wakeup called")

        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        LOG.debug("PixelRing listen called")
        self.put(self.pattern.listen)

    def think(self):
        LOG.debug("PixelRing think called")
        self.put(self.pattern.think)

    def speak(self):
        LOG.debug("PixelRing speak called")
        self.put(self.pattern.speak)

    def off(self):
        LOG.debug("PixelRing off called")
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()
