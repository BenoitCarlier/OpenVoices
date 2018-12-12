from pyAudioAnalysis import audioTrainTest as aT
import os

from python_scripts import tools

emotion_list = tools.MAP_EMOTION.values()
# emotion_list = []
# emotion_list.append('angry')
# emotion_list.append('calm')
# emotion_list.append('neutral')
# emotion_list.append('happy')
# emotion_list.append('disgust')
# emotion_list.append('fearful')
# emotion_list.append('surprised')

input_dir = 'output_by_emotion'

output_dir = 'Models'
output_model_name = 'knnEmotion7'

path_base = os.path.join(os.path.dirname(os.getcwd()), input_dir)
dir_list = [os.path.join(path_base, emo) for emo in emotion_list]

aT.featureAndTrain(dir_list, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "knn",
                   os.path.join(output_dir, output_model_name))
