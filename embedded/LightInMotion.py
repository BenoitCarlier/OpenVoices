import board
import neopixel


class LightInMotion:
    def __init__(self, map_emotion_2_color, num_pixels=8, pin=board.D18, order=neopixel.RGB, brightness=1):
        self.map_emotion_2_color = map_emotion_2_color
        self.num_pixels = num_pixels
        self.pin = pin
        self.order = order
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(self.pin,
                                        self.num_pixels,
                                        self.brightness,
                                        self.pixel_order)

    def set_emotion(self, emotion):
        pixels.fill(self.map_emotion_2_color[emotion])

