import rainbowhat as rh


class LightInMotionRainbow:
    def __init__(self, map_emotion_2_color={}, brightness=1):
        self.map_emotion_2_color = map_emotion_2_color
        self.map_emotion_2_color.setdefault('-1', 0x008080)
        self.brightness = brightness

        rh.rainbow.clear()
        rh.display.clear()

    def set_emotion(self, emotion):
        print("Set emotion {}".format(emotion))
        rgb = self.map_emotion_2_color[emotion]
        if not isinstance(rgb, tuple):
            rgb = (rgb & 255, (rgb >> 8) & 255, (rgb >> 16) & 255)
        print("Set color {}".format(rgb))
        rh.rainbow.set_all(*rgb, brightness=self.brightness)
        rh.rainbow.show()

        to_display = emotion
        if to_display == '-1':
            to_display = 'SHIT'
        else:
            to_display = emotion[:4].upper()

        rh.display.print_str(to_display)
        rh.display.show()

    def terminate(self):
        rh.rainbow.clear()
        rh.rainbow.show()

        rh.display.clear()
        rh.display.show()

        print("LightInMotionRainbow: terminated")

    @staticmethod
    @rh.touch.A.press()
    def touch_a(channel):
        print('Button A pressed')
        rh.lights.rgb(1, 0, 0)


    @staticmethod
    @rh.touch.A.release()
    def release_a(channel):
        print('Button A released')
        rh.lights.rgb(0, 0, 0)
