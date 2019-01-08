# Implementation of a Keras neural network to classify
# our audio files (output_by_emotion_tronque)

import os
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from python_scripts import tools
import pickle

input_dir = 'output_by_emotion_tronque'
input_dir_path = os.path.join(os.path.dirname(os.getcwd()), input_dir)

# Liste des dossiers par émotion
emotion_list = tools.MAP_EMOTION.values()
emotion_path_list = []
for emo in emotion_list:
    emotion_path_list.append(os.path.join(input_dir_path,emo))

audio_mat = []

for dir in emotion_path_list:
    audio_list = []
    for file in os.listdir(dir):
        file_path = os.path.join(dir,file)
        [Fs, x] = audioBasicIO.readAudioFile(file_path)
        F, f_names = audioFeatureExtraction.stFeatureExtraction(audioBasicIO.stereo2mono(x), Fs, 0.200 * Fs, 0.150 * Fs)
        audio_list.append(F)
    audio_mat.append(audio_list)

output_dir = 'output_matrix_features'
output_dir_path = os.path.join(os.path.dirname(os.getcwd()), output_dir)

if not os.path.isdir(output_dir_path):
    os.mkdir(output_dir_path)

filename = 'features_matrix'
matrix_file_path = os.path.join(output_dir_path, filename)
filehandler = open(matrix_file_path, 'wb') # création du fichier d'output
pickle.dump(audio_mat, filehandler) # on dump l'objet dans le fichier avec pickle