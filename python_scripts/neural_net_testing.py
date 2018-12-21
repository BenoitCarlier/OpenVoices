# testing the new and fresh model we just created

import os
import keras
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import numpy as np


def print_max_index(L):
    m = max(L)
    for i in range(len(L)):
        if m == L[i]:
            return (i)
    return (-1)


model_file_path = 'Models/neural_net_model.model'
model_weigths_path = 'Models/neural_net_model.weights'

model = keras.models.load_model(model_file_path)

out_audio_for_test_path = 'output_audio_for_testing'

dir_to_test = os.path.join(os.path.dirname(os.getcwd()), out_audio_for_test_path)

file_list = os.listdir(dir_to_test)

feat_list = []

for file in file_list:
    file_path = os.path.join(dir_to_test, file)
    [Fs, x] = audioBasicIO.readAudioFile(file_path)
    F, f_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.200 * Fs, 0.150 * Fs)
    feat_list.append(F)

# Make the input shape (646,1) for Dense input neural networks

audio_feature_set = []
for item in feat_list:
    list = []
    for feature in item:
        for frame in feature:
            list.append(frame)
    audio_feature_set.append(list)

feat_list = np.array(feat_list)
audio_feature_set = np.array(audio_feature_set)



def show_acc(input_list, files):
    predicted_list = model.predict(input_list)
    acc = 0
    for i in range(len(input_list)):
        print('fichier traité :', files[i])
        actual_class = files[i].split('-')[2]
        class_predict = print_max_index(predicted_list[i])
        print('qui est de la classe ', actual_class)
        print('classe selon le réseau de neurones :', class_predict)
        if int(class_predict) == int(actual_class):
            acc += 1
        print('-----------------------------')

    print('accuracy : ', acc / len(file_list), ', which means', acc, ' out of ', len(file_list), ' files')


#change the input_list if the neural networks starts with a Dense or a LSTM layer
show_acc(audio_feature_set, file_list)