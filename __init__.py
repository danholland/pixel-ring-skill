from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

from . import mraa
import os
import time
from .pixel_ring import PixelRing

class PixelRingSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        en = mraa.Gpio(12)
        if os.geteuid() != 0 :
            time.sleep(1)
    
        en.dir(mraa.DIR_OUT)
        en.write(0)

        pixel_ring = PixelRing()
    
    def initialize(self):
        self.log.info("Pixel Ring initializing")
        pixel_ring.set_brightness(20)
        pixel_ring.wakeup()

    @intent_file_handler('ring.pixel.intent')
    def handle_ring_pixel(self, message):
        self.speak_dialog('ring.pixel')
        pixel_ring.wakeup()

    def stop(self):
        self.log.debug("Pixel Ring stopping")
        pixel_ring.off()

    def shutdown(self):
        self.log.debug("Pixel Ring shutting down")
        pixel_ring.off()
        en.write(1)

def create_skill():
    return PixelRingSkill()

