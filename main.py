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
BRIGHTNESS = 0.2

global recording_loop
recording_loop = False

if __name__ == '__main__':
    record = Record(record_seconds=3, channels=1)  # because our mic has only one channel
    ml_analysis = MLAnalysis('knn', 'python_scripts/Models/knnEmotion7')

    # light_in_motion = LightInMotion(map_emotion_2_color=MAP_EMOTION_2_COLOR,
    #                                 num_pixels=NUM_PIXEL,
    #                                 brightness=BRIGHTNESS)

    light_in_motion = LightInMotionRainbow(map_emotion_2_color=MAP_EMOTION_2_COLOR,
                                           brightness=BRIGHTNESS)

    base_output_file = 'output_embedded/'

    def signal_handler(signal, frame):
        print('\nYou pressed Ctrl+C! - EXIT')
        record.terminate()
        light_in_motion.terminate()
        os.system("stty -cbreak echo")
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)


    @rh.touch.A.press()
    def touch_a(channel):
        print('Button A pressed')
        rh.lights.rgb(1, 0, 0)


    @rh.touch.A.release()
    def release_a(channel):
        print('Button A released')
        rh.lights.rgb(0, 0, 0)


    @rh.touch.B.press()
    def touch_b(channel):
        print('Button B pressed')
        rh.lights.rgb(0, 1, 0)


    @rh.touch.B.release()
    def release_b(channel):
        print('Button B released')
        rh.lights.rgb(0, 0, 0)


    @rh.touch.C.press()
    def touch_c(channel):
        global recording_loop
        print('Button C pressed')
        print("recording_loop: {}".format(recording_loop))

        rh.lights.rgb(0, 0, 1)
        recording_loop = not recording_loop


    @rh.touch.C.release()
    def release_c(channel):
        global recording_loop
        print('Button C released')
        print("recording_loop: {}".format(recording_loop))
        rh.lights.rgb(0, 0, 0)

        count = 0

        while recording_loop:
            current_wav = "{base}record_{num}.wav".format(base=base_output_file, num=count)
            record.record(current_wav)
            emotion = ml_analysis.get_emotion(current_wav)
            light_in_motion.set_emotion(emotion)
            print("Emotion: ", end="\t\t")
            print(emotion)

            count += 1
            sleep(2)


    while True:
        pass
