from pyAudioAnalysis import audioTrainTest as aT
import os

emotion_list = []
emotion_list.append('angry')
emotion_list.append('calm')
emotion_list.append('neutral')
emotion_list.append('happy')
emotion_list.append('disgust')
emotion_list.append('fearful')
emotion_list.append('surprised')

input_dir = 'output_by_emotion'

path_base = os.path.join(os.path.dirname(os.getcwd()), input_dir)

dir_list = []

for emo in emotion_list:
    dir_list.append(os.path.join(path_base,emo))

for dir in dir_list:
    files = os.listdir(dir)
    print(files)

aT.featureAndTrain(dir_list, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn", "knnEmotion7")
