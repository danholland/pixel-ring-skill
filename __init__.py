from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message

from evdev import InputDevice
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
        self.userkey = None
        try:
            self.userkey = InputDevice("/dev/input/event0")
        except Exception as e:
            self.log.debug("exception while reading InputDevice: {}".format(e))

        if self.userkey:
            self.schedule_repeating_event(
                self.handle_button, None, 0.1, 'PixelRing')

        self.pixel_ring = PixelRing()
        brightness = self.settings.get('brightness', 15)
        self.pixel_ring.set_brightness(brightness)
        self.add_event('recognizer_loop:wakeword', self.handler_wakeword)
        self.add_event('recognizer_loop:record_begin',
                       self.handle_listener_listen)
        self.add_event('recognizer_loop:record_end', self.handle_listener_off)
        self.add_event('recognizer_loop:audio_output_start',
                       self.handle_listener_speak)
        self.add_event('recognizer_loop:audio_output_end',
                       self.handle_listener_off)
        self.add_event('mycroft.skill.handler.start',
                       self.handle_listener_think)
        self.add_event('mycroft.skill.handler.complete',
                       self.handle_listener_off)
        self.pixel_ring.off()

#    def on_settings_changed(self):
#        brightness = self.settings.get('brightness', 15)
#        pattern = self.settings.get('pattern', 'echo')
#        self.pixel_ring.set_brightness(brightness)
#        self.pixel_ring.change_pattern(pattern)

    @intent_file_handler('ring.pixel.change.intent')
    def handle_ring_pixel_change(self, message):
        pattern_type = message.data.get('type')
        self.log.info(pattern_type)

        def google():
            self.pixel_ring.change_pattern('google')

        def echo():
            self.pixel_ring.change_pattern('echo')

        def on():
            self.pixel_ring.off()
            self.en.write(0)
#            self.pixel_ring.wakeup()

        def off():
            self.shutdown()

        known_types = {
            "google": google,
            "echo": echo,
            "amazon": echo,
            "on": on,
            "off": off
        }
        func = known_types.get(
            pattern_type, lambda: self.speak("Sorry, I don't understand"))
        return func()

    def handler_wakeword(self, message):
        self.log.debug("wakeword")
        self.pixel_ring.wakeup()

    def handle_listener_listen(self, message):
        self.log.debug("listen")
        self.pixel_ring.listen()

    def handle_listener_think(self, message):
        self.log.debug("think")
        self.pixel_ring.think()

    def handle_listener_speak(self, message):
        self.log.debug("speak")
        self.pixel_ring.speak()

    def handle_listener_off(self, message):
        self.log.debug("off")
        self.pixel_ring.off()

    @intent_file_handler('ring.pixel.demo.intent')
    def handle_ring_pixel_demo(self, message):
        self.pixel_ring.off()
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

    def handle_button(self, message):
        if not self.userkey:
            return

        longpress_threshold = 4
        respeaker_userkey_code = 194

        if respeaker_userkey_code in self.userkey.active_keys():
            pressed_time = time.time()
            while respeaker_userkey_code in self.userkey.active_keys():
                time.sleep(0.2)
            pressed_time = time.time()-pressed_time
            if pressed_time < longpress_threshold:
                self.bus.emit(Message("mycroft.mic.listen"))
            else:
                self.bus.emit(Message("mycroft.stop"))

    def stop(self):
        self.log.debug("PixelRing stopping")
        self.pixel_ring.off()

    def shutdown(self):
        self.log.debug("PixelRing shutting down")
        self.pixel_ring.off()
        self.en.write(1)


def create_skill():
    return PixelRingSkill()
