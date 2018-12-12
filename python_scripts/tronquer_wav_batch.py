'''

Tronque tous les fichiers wav pour qu'ils fassent la même taille : la taille du fichier wav le plus petit
sert a avoir des inputs de meme dimensions

TODO : faire en sorte de ne pas tronquer mais de sous echantilloner

'''

import os
import glob
from pyAudioAnalysis import audioBasicIO
import scipy.io.wavfile as sc_wav

dirname = os.path.dirname(os.getcwd())
outputdir = 'output_tronque'
audio_src_name = 'Audio_Speech_Actors_01-24'
audio_speech_path = os.path.join(dirname, audio_src_name)

out_dir_path = os.path.join(dirname, outputdir)
if (not os.path.isdir(out_dir_path)):
    print('output directory non existant, il a été créé')
    os.mkdir(out_dir_path)

filename_wildcard = os.path.join(audio_speech_path, 'Actor_*/*')
path_list = glob.glob(filename_wildcard)

[Fs0, x0] = audioBasicIO.readAudioFile(path_list[0])
min_len = len(x0)

for path in path_list:
    # On détermine la longueur minimum sur tous les fichiers audio pour qu'ils soient tous de la même taille
    [Fs, x] = audioBasicIO.readAudioFile(path)
    l = len(x)
    if l < min_len:
        min_len = l

for path in path_list:
    dir_names = path.split('/')
    filename = dir_names[-1]
    actor_name = dir_names[-2]
    out_path = os.path.join(dirname, outputdir, actor_name, filename)
    if (not os.path.isdir(os.path.join(dirname, outputdir, actor_name))):
        os.mkdir(os.path.join(dirname, outputdir, actor_name))
        print('directory ' + actor_name + ' créé ')
    new_x = x[0:min_len]
    sc_wav.write(out_path,Fs0,new_x)

