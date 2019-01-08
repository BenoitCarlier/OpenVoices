import rainbowhat as rh


class LightInMotionRainbow:
    def __init__(self, map_emotion_2_color={}, brightness=1, verbose = False):
        self.map_emotion_2_color = map_emotion_2_color
        self.map_emotion_2_color.setdefault('-1', 0x008080)
        self.brightness = brightness
        self.verbose = verbose

        self.__clear()
        self.__show()

    def set_emotion(self, emotion):
        self.__clear()

        rgb = self.map_emotion_2_color[emotion]
        if not isinstance(rgb, tuple):
            rgb = (rgb & 255, (rgb >> 8) & 255, (rgb >> 16) & 255)

        if self.verbose:
            print("Set emotion {}".format(emotion))
            print("Set color {}".format(rgb))

        rh.rainbow.set_all(*rgb, brightness=self.brightness)

        to_display = emotion
        if to_display == '-1':
            to_display = 'SHIT'
        else:
            to_display = emotion[:4].upper()

        rh.display.print_str(to_display)

        self.__show()

    def __clear(self):
        rh.rainbow.clear()
        rh.display.clear()

    def __show(self):
        rh.rainbow.show()
        rh.display.show()


    def terminate(self):
        self.__clear()
        self.__show()

        print("LightInMotionRainbow: terminated")
