import rainbowhat as rh


class LightInMotionRainbow:
    def __init__(self, map_emotion_2_color={}, brightness=1):
        self.map_emotion_2_color = map_emotion_2_color
        self.map_emotion_2_color.setdefault('-1', 0x008080)
        self.brightness = brightness

    def set_emotion(self, emotion):
        print("Set emotion {}".format(emotion))
        rgb = self.map_emotion_2_color[emotion]
        if not isinstance(rgb, tuple):
            rgb = (rgb & 255, (rgb >> 8) & 255, (rgb >> 16) & 255)
        print("Set color {}".format(rgb))
        rh.rainbow.set_all(*rgb, brightness=self.brightness)
        rh.display.print_str(emotion[:4])
        rh.rainbow.show()
