### Classifies one file with our knn from 'knn_on_emotions.py'

from pyAudioAnalysis import audioTrainTest as aT

print(aT.fileClassification("../output_by_emotion/test_input/03-01-01-01-01-01-22.wav", "Models/knnEmotion7","knn"))