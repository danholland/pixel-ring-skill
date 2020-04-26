from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

from . import mraa
import os
import time
from .pixel_ring import PixelRing


class PixelRingSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.en = mraa.Gpio(12)
        if os.geteuid() != 0:
            time.sleep(1)

        self.en.dir(mraa.DIR_OUT)
        self.en.write(0)

        self.pixel_ring = PixelRing()

    def initialize(self):
        self.log.info("PixelRing initializing")
        self.register_intent_file(
            'ring.pixel.demo.intent', self.handle_ring_pixel_demo)
        brightness = self.settings.get('brightness', 15)
        self.pixel_ring.set_brightness(brightness)
        self.pixel_ring.wakeup()

    def on_settings_changed(self):
        brightness = self.settings.get('brightness', 15)
        pattern = self.settings.get('pattern', 'echo')
        self.pixel_ring.set_brightness(brightness)
        self.pixel_ring.change_pattern(pattern)

    @intent_file_handler('ring.pixel.intent')
    def handle_ring_pixel(self, message):
        self.speak_dialog('ring.pixel')
        self.pixel_ring.wakeup()

    def handle_ring_pixel_demo(self, message):
        self.log.info("Running Pixel Ring demo")
        self.pixel_ring.wakeup()
        time.sleep(3)
        self.pixel_ring.think()
        time.sleep(3)
        self.pixel_ring.speak()
        time.sleep(3)
        self.pixel_ring.off()

    def stop(self):
        self.log.debug("PixelRing stopping")
        self.pixel_ring.off()

    def shutdown(self):
        self.log.debug("PixelRing shutting down")
        self.pixel_ring.off()
        self.en.write(1)


def create_skill():
    return PixelRingSkill()
