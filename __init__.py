from mycroft import MycroftSkill, intent_file_handler


class PixelRing(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('ring.pixel.intent')
    def handle_ring_pixel(self, message):
        self.speak_dialog('ring.pixel')


def create_skill():
    return PixelRing()

