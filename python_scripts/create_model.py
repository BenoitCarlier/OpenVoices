import os

from pyAudioAnalysis import audioTrainTest as aT

from python_scripts import tools
import time

MODEL_TYPES = ['knn',
               'svm',
               'svm_rbf',
               'randomforest',
               'gradientboosting',
               'extratrees',
               'Emotion7']

EMOTION_LIST = tools.MAP_EMOTION.values()

input_dir = 'output_by_emotion'
output_dir = 'Models'
model_name = 'Emotion7'
model_type = MODEL_TYPES[1]
output_name = model_type + model_name

path_base = os.path.join(os.path.dirname(os.getcwd()), input_dir)
dir_list = [os.path.join(path_base, emo) for emo in EMOTION_LIST]

begin = time.time()
aT.featureAndTrain(dir_list, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, model_type,
                   os.path.join(output_dir, output_name))

end = time.time()
print("Duration : {}".format(end - begin))
