from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
import matplotlib.pyplot as plt
import numpy as np

[Fs, x] = audioBasicIO.readAudioFile("/home/benoit/Documents/Code/Projets/OpenVoices/output_by_emotion_tronque/happy/03-01-03-01-01-01-02.wav");
F, f_names = audioFeatureExtraction.stFeatureExtraction(x, Fs, 0.200*Fs, 0.150*Fs);
plt.subplot(2,1,1); plt.plot(F[12,:]); plt.xlabel('Frame no'); plt.ylabel(f_names[0]);
plt.subplot(2,1,2); plt.plot(F[1,:]); plt.xlabel('Frame no'); plt.ylabel(f_names[1]); plt.show()

print(len(x))

print(np.shape(F))