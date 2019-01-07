import board
import neopixel


class LightInMotion:
    def __init__(self, map_emotion_2_color={}, num_pixels=8, pin=board.D18, order=neopixel.RGB, brightness=1):
        self.map_emotion_2_color = map_emotion_2_color
        self.map_emotion_2_color.setdefault('-1', 0x008080)
        self.num_pixels = num_pixels
        self.pin = pin
        self.order = order
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(pin=self.pin,
                                        n=self.num_pixels,
                                        brightness=self.brightness,
                                        pixel_order=self.order)

    def set_emotion(self, emotion):
        print("Set emotion {}".format(emotion))
        print("Set color {}".format(self.map_emotion_2_color[emotion]))
        self.pixels.fill(self.map_emotion_2_color[emotion])
