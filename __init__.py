from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft.util.log import LOG

import mraa
import os
import time
from .pixel_ring import PixelRing

class PixelRingSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        LOG.debug("Pixel Ring initializing")
        en = mraa.Gpio(12)
        if os.geteuid() != 0 :
            time.sleep(1)
    
        en.dir(mraa.DIR_OUT)
        en.write(0)

        pixel_ring = PixelRing()

        pixel_ring.set_brightness(20)
        pixel_ring.wakeup()

    @intent_file_handler('ring.pixel.intent')
    def handle_ring_pixel(self, message):
        self.speak_dialog('ring.pixel')

    def stop(self):
        LOG.debug("Pixel Ring stopping")
        pixel_ring.off()
        en.write(1)

def create_skill():
    return PixelRingSkill()

