from embedded.MLAnalysis import MLAnalysis
from embedded.Record import Record
from embedded.LightInMotion import LightInMotion

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
    record = Record(record_seconds=1)
    ml_analysis = MLAnalysis('knn', 'python_scripts/Models/knnEmotion7')

    light_in_motion = LightInMotion(MAP_EMOTION_2_COLOR, NUM_PIXEL, BRIGHTNESS)

    base_output_file = 'output_embedded/'
    count = 0
    while True:
        current_wav = "{base}record_{num}.wav".format(base=base_output_file, num=count)
        record.record(current_wav)
        emotion = ml_analysis.get_emotion(current_wav)
        print("Emotion: " + emotion)
        light_in_motion.set_emotion(emotion)
