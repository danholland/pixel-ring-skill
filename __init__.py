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

    def initialize(self):
        self.log.info("PixelRing initializing")
        self.pixel_ring = PixelRing()
        brightness = self.settings.get('brightness', 15)
        self.pixel_ring.set_brightness(brightness)
        self.pixel_ring.wakeup()

#    def on_settings_changed(self):
#        brightness = self.settings.get('brightness', 15)
#        pattern = self.settings.get('pattern', 'echo')
#        self.pixel_ring.set_brightness(brightness)
#        self.pixel_ring.change_pattern(pattern)

    @intent_file_handler('ring.pixel.intent')
    def handle_ring_pixel(self, message):
        self.speak_dialog('ring.pixel')
        self.pixel_ring.wakeup()

    @intent_file_handler('ring.pixel.change.intent')
    def handle_ring_pixel_change(self, message):
        pattern_type = message.data.get('type')
        self.log.info(pattern_type)

        def google():
            self.log.info("GOOGLE")
            self.pixel_ring.change_pattern('google')

        def echo():
            self.log.info("ECHO")
            self.pixel_ring.change_pattern('echo')

        def on():
            self.log.info("ON")
            self.pixel_ring.off()
            self.en.write(0)
            self.pixel_ring.wakeup()

        def off():
            self.log.info("OFF")
            self.stop()

        known_types = {
            "google": google,
            "echo": echo,
            "amazon": echo,
            "on": on,
            "off": off
        }
        func = known_types.get(
            pattern_type, lambda: self.speak("Sorry, I don't understand"))
        self.log.info(func)
        return func()

    @intent_file_handler('ring.pixel.demo.intent')
    def handle_ring_pixel_demo(self, message):
        self.log.info("Running Pixel Ring demo")
        self.log.debug("PixelRing Wakeup")
        self.pixel_ring.wakeup()
        time.sleep(3)
        self.log.debug("PixelRing Listen")
        self.pixel_ring.listen()
        time.sleep(3)
        self.log.debug("PixelRing Think")
        self.pixel_ring.think()
        time.sleep(3)
        self.log.debug("PixelRing Speak")
        self.pixel_ring.speak()
        time.sleep(3)
        self.log.debug("PixelRing Off")
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
