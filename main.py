import os
import signal
import sys
from time import sleep

import rainbowhat as rh

from embedded.LightInMotionRainbow import LightInMotionRainbow
from embedded.MLAnalysis import MLAnalysis
from embedded.Record import Record

ColorDict = {"black": 0x000000,
             "white": 0xFFFFFF,
             "red": 0xFF0000,
             "blue": 0x0000FF,
             "green": 0x00FF00,
             "yellow": 0xFFFF00,
             "orange": 0xFF8000,
             "pink": 0xFFC0CB,
             "teal": 0x008080,
             "purple": 0x080080}

MAP_EMOTION_2_COLOR = {
    'neutral': ColorDict["yellow"],
    'calm': ColorDict["white"],
    'happy': ColorDict["orange"],
    'sad': ColorDict["blue"],
    'angry': ColorDict["red"],
    'fearful': ColorDict["purple"],
    'disgust': ColorDict["green"],
    'surprised': ColorDict["pink"],
}

NUM_PIXEL = 8
BRIGHTNESS = 0.1

global recording_loop
recording_loop = False
global count
count = 0

if __name__ == '__main__':
    ## Init modules
    record = Record(record_seconds=3, channels=1)  # because our mic has only one channel
    ml_analysis = MLAnalysis('knn', 'python_scripts/Models/knnEmotion7')
    # light_in_motion = LightInMotion(map_emotion_2_color=MAP_EMOTION_2_COLOR,
    #                                 num_pixels=NUM_PIXEL,
    #                                 brightness=BRIGHTNESS)
    light_in_motion = LightInMotionRainbow(map_emotion_2_color=MAP_EMOTION_2_COLOR,
                                           brightness=BRIGHTNESS)
    base_output_file = 'output_embedded/'


    ##

    ## Handle keyboard interrupt
    def signal_handler(signal, frame):
        print('\nYou pressed Ctrl+C! - EXIT')
        record.terminate()
        light_in_motion.terminate()
        os.system("stty -cbreak echo")
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)

    led_red = False
    led_green = False
    led_blue = False


    ##

    ## Handle rainbow Touch button
    @rh.touch.A.press()
    def touch_a(channel):
        led_red = True
        rh.lights.rgb(led_red, led_green, led_blue)
        light_in_motion.change_brightness()


    @rh.touch.A.release()
    def release_a(channel):
        led_red = False
        rh.lights.rgb(led_red, led_green, led_blue)


    @rh.touch.B.press()
    def touch_b(channel):
        led_green = True
        rh.lights.rgb(led_red, led_green, led_blue)
        wav_file = "{base}record_manual.wav".format(base=base_output_file)
        record.record(wav_file)
        emotion = ml_analysis.get_emotion(wav_file)

        print()
        print("File: {}".format(wav_file))
        print("Emotion: {}".format(emotion))

        light_in_motion.set_emotion(emotion)


        led_green = False
        rh.lights.rgb(led_red, led_green, led_blue)


    @rh.touch.B.release()
    def release_b(channel):
        pass


    @rh.touch.C.press()
    def touch_c(channel):
        global recording_loop, count
        recording_loop = not recording_loop

        led_blue = recording_loop
        rh.lights.rgb(led_red, led_green, led_blue)

        count = 0


    @rh.touch.C.release()
    def release_c(channel):
        pass

    ##

    while 1:
        if recording_loop:
            current_wav = "{base}record_{num}.wav".format(base=base_output_file, num=count)
            record.record(current_wav)
            emotion = ml_analysis.get_emotion(current_wav)
            light_in_motion.set_emotion(emotion)

            print()
            print("File: {}".format(current_wav))
            print("Emotion: {}".format(emotion))

            count += 1
            sleep(2)
