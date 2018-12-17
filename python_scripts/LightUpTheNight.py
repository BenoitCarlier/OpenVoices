import board
import neopixel
import time
from time import sleep
pixel_pin = board.D18
num_pixels = 8
ORDER = neopixel.RGB

ColorDict = { "black":0x000000, "white":0x101010, "red":0x100000, "blue":0x000010, "green":0x001000, "yellow":0x101000, "orange":0x100600, "pink":0x100508, "teal":0x100508, "teal":0x000808, "purple":0x080008}

#Example of colorString : "Fear:blue,Surprise:yellow"
def SetColors(colorString):
    EmoDict = {}
    colorsEmo = colorString.split(",")
    for k in range(len(colorsEmo)):
        oneColorEmo = colorsEmo[k].split(":")
        #print(oneColorEmo, ColorDict(oneColorEmo[1]))
        EmoDict[oneColorEmo[0]] = ColorDict[oneColorEmo[1]]
    return EmoDict

def LightAll(color):
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order = ORDER)
    pixels.fill(ColorDict[color])

def LightLast(emotion, EmoDict):
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order = ORDER)
    if (len(pixels)>1):
        for k in range(1, len(pixels)):
            pixels[k] = pixels[k-1]
    pixels[0] = EmoDict[emotion]
    print(pixels)
    pixels.show()

def play():
    EmoDict = SetColors("neutral:white,surprise:yellow,happiness:orange,fear:blue,disgust:green,sad:purple")
    LightAll("black")
    while(True):
        LightLast("happiness",EmoDict)
        time.sleep(0.8)
        LightLast("surprise",EmoDict)
        time.sleep(0.8)
        LightLast("fear",EmoDict)
        time.sleep(0.8)
        LightLast("neutral",EmoDict)
        time.sleep(0.8)
        LightLast("sad",EmoDict)
        time.sleep(0.8)
    return 0

play()

