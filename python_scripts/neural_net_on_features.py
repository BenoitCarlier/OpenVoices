import pickle
import keras
from python_scripts import tools
import numpy as np
from keras.layers import Dense, Activation, Dropout, LSTM, Embedding
import os
import matplotlib.pyplot as plt

# confirm TensorFlow sees the GPU
from tensorflow.python.client import device_lib
print(str(device_lib.list_local_devices()))

# confirm Keras sees the GPU
from keras import backend
print((backend.tensorflow_backend._get_available_gpus()))

print("xxx")

#matrix_file = open('/home/benoit/Documents/Code/Projets/OpenVoices/output_matrix_features/features_matrix', 'rb')

input_dir = 'output_matrix_features'
input_dir_path = os.path.join(os.path.dirname(os.getcwd()), input_dir)
matrix_file = open(os.path.join(input_dir_path,'features_matrix'), 'rb')

audio_mat = pickle.load(matrix_file)

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

print(np.shape(audio_feat_list))
print(np.shape(labels))

audio_feature_set = []
for item in audio_feat_list:
    list = []
    for feature in item:
        for frame in feature:
            list.append(frame)
    audio_feature_set.append(list)

audio_feature_set = np.array(audio_feature_set)
print(np.shape(audio_feature_set))

model = keras.Sequential()
model.add(Dense(units=512, activation='relu', input_shape=(646,)))
model.add(Dropout(0.2))
model.add(Dense(units=512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(units=8, activation='softmax'))

# model = keras.Sequential();
# #model.add(Embedding((34, 19), 64))
# model.add(LSTM((34, 19), dropout=0.2, recurrent_dropout=0.2))
# model.add(Dense(8, activation='softmax'))


model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

history = model.fit(
    x=audio_feature_set,
    y=labels,
    epochs=100,
    validation_split=0.1,
    batch_size=32
)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# output_dir = 'models'
# output_dir_path = os.path.join(os.path.dirname(os.getcwd()), output_dir)
# nn_file = open('output_dir_path\\neural_net', 'wb')
#
#pickle.dump(model, nn_file, protocol=pickle.HIGHEST_PROTOCOL)

