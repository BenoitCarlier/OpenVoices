import pickle
import keras
from python_scripts import tools
import numpy as np
from keras.layers import Dense, Activation, LSTM

# confirm TensorFlow sees the GPU
from tensorflow.python.client import device_lib
assert 'GPU' in str(device_lib.list_local_devices())
print('-------------------')
print('|')
print('|')
print('|')
print('TENSORFLOW IS USING GPU')

# confirm Keras sees the GPU
from keras import backend
assert len(backend.tensorflow_backend._get_available_gpus()) > 0
print('-------------------')
print('|')
print('|')
print('|')
print('KERAS IS USING GPU')

matrix_file = open('/home/benoit/Documents/Code/Projets/OpenVoices/output_matrix_features/features_matrix', 'rb')
audio_mat = pickle.load(matrix_file)

#audio_feat_list input is of shape (34,19) for LSTM input neural networks

audio_feat_list = []
class_name_list = []
for i in range(len(audio_mat)):
    for j in range(len(audio_mat[i])):
        audio_feat_list.append(audio_mat[i][j])
        class_name_list.append(i)

print(len(audio_feat_list)),
print(len(class_name_list))

audio_feat_list = np.array(audio_feat_list)
class_name_list = np.array(class_name_list)

labels = keras.utils.to_categorical(class_name_list)

# Make the input shape (646,1) for Dense input neural networks

audio_feature_set = []
for item in audio_feat_list:
    list = []
    for feature in item:
        for frame in feature:
            list.append(frame)
    audio_feature_set.append(list)

audio_feature_set = np.array(audio_feature_set)

model = keras.Sequential()
model.add(Dense(units=64, input_shape=(646,)))
model.add(Activation('relu'))
model.add(Dense(units=8))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(
    x=audio_feature_set,
    y=labels,
    epochs=20,
    validation_split=0.2,
    batch_size=32
)

model.save('Models/neural_net_model.model')
print('modèle sauvegardé')
model.save_weights('Models/neural_net_model.weights')
print('poids sauvegardés')
