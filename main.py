from time import sleep

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

if __name__ == '__main__':
    record = Record(record_seconds=1, channels=1)  # because our mic has only one channel
    ml_analysis = MLAnalysis('knn', 'python_scripts/Models/knnEmotion7')

    # light_in_motion = LightInMotion(map_emotion_2_color=MAP_EMOTION_2_COLOR,
    #                                 num_pixels=NUM_PIXEL,
    #                                 brightness=BRIGHTNESS)

    light_in_motion = LightInMotionRainbow(map_emotion_2_color=MAP_EMOTION_2_COLOR,
                                           brightness=BRIGHTNESS)

    base_output_file = 'output_embedded/'
    count = 0
    try:
        while True:
            current_wav = "{base}record_{num}.wav".format(base=base_output_file, num=count)
            record.record(current_wav)
            emotion = str(ml_analysis.get_emotion(current_wav)[2])
            light_in_motion.set_emotion(emotion)
            print("Emotion: ", end="\t\t")
            print(emotion)

            count += 1
            sleep(2)
    except KeyboardInterrupt:
        record.terminate()
        light_in_motion.terminate()
