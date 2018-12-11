import os
from shutil import copyfile
import glob
from python_scripts.tools import get_emotion

dirname = os.path.dirname(os.getcwd())
outputdir = 'output_by_emotion'
audio_src_name = 'Audio_Speech_Actors_01-24'
audio_speech_path = os.path.join(dirname, audio_src_name)


filename_wildcard = os.path.join(audio_speech_path, 'Actor_*/*')
path_list = glob.glob(filename_wildcard)

for path in path_list:
    filename = os.path.basename(path)
    emo = get_emotion(filename)
    output_dir_name = os.path.join(dirname, outputdir)
    output_dir_emotion = os.path.join(output_dir_name, emo)
    if not os.path.isdir(output_dir_name):
        os.mkdir(output_dir_name)
    if not os.path.isdir(output_dir_emotion):
        os.mkdir(output_dir_emotion)

    copyfile(path, os.path.join(output_dir_emotion, filename))
