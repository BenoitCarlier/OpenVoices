import os
import pickle
import time

from pyAudioAnalysis import audioTrainTest as aT

from python_scripts import tools
from python_scripts import visualisation_tools

MAP_DUMP_INFO = {
    'knn': [
        'X',
        'Y',
        'MEAN',
        'STD',
        'classNames',
        'bestParam',
        'mt_win',
        'mt_step',
        'st_win',
        'st_step',
        'compute_beat'
    ],
    'default': [
        'MEAN',
        'STD',
        'classNames',
        'bestParam',
        'mt_win',
        'mt_step',
        'st_win',
        'st_step',
        'compute_beat',
    ]
}

MAP_DUMP_MORE_INFO = [
    'Params',
    'ac_all',
    'f1_all',
    'precision_classes_all',
    'recall_classes_all',
    'f1_classes_all',
    'confusion_matrix'
]

MODEL_TYPES = ['knn',
               'svm',
               'svm_rbf',
               'randomforest',
               'gradientboosting',
               'extratrees']

EMOTION_LIST = tools.MAP_EMOTION.values()


class MLAnalysis:
    # Will read data from pickle file with the name given in param and also for this named file with .more_info
    # Use global_analysis to get quick results
    def __init__(self, output_path, model_type):
        self.output_path = output_path
        self.model_type = model_type
        self.info = None
        self.more_info = None
        self.__read_file()
        self.__read_file_more_info()

    def __read_file(self):
        file_name = self.output_path
        if self.model_type != 'knn':
            file_name += 'MEANS'

        with open(file_name, 'rb') as f:
            pickle_obj = pickle.Unpickler(f)
            dump_info = MAP_DUMP_INFO.get(model_type) or MAP_DUMP_INFO['default']
            self.info = {name: pickle_obj.load() for name in dump_info}

    def __read_file_more_info(self):
        with open(self.output_path + '.more_info', 'rb') as f:
            pickle_obj = pickle.Unpickler(f)
            self.more_info = {name: pickle_obj.load() for name in MAP_DUMP_MORE_INFO}

    def global_analysis(self):
        class_name_list = self.info['classNames']
        params = self.more_info['Params']
        ac_all = self.more_info['ac_all']
        f1_all = self.more_info['f1_all']
        precision_classes_all = self.more_info['precision_classes_all']
        recall_classes_all = self.more_info['recall_classes_all']
        f1_classes_all = self.more_info['f1_classes_all']
        confusion_matrix = self.more_info['confusion_matrix']
        data_frame = visualisation_tools.result_data_to_dataframe(params, ac_all, f1_all, precision_classes_all,
                                                                  recall_classes_all,
                                                                  f1_classes_all, class_name_list)
        data_frame.to_csv(self.output_path + ".csv")

        l_desc = ['bestParam', 'mt_win', 'mt_step', 'st_win', 'st_step', 'compute_beat']
        description = ', '.join(['{}: {}'.format(name, self.info[name]) for name in l_desc])
        visualisation_tools.plot_confusion_matrix(confusion_matrix, class_name_list, self.output_path, desc=description)

def make_model(input_dir, output_path):
    path_base = os.path.join(os.path.dirname(os.getcwd()), input_dir)
    dir_list = [os.path.join(path_base, emo) for emo in EMOTION_LIST]

    begin = time.time()
    aT.featureAndTrain(dir_list, 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, model_type,
                       output_path)

    end = time.time()
    print("Duration : {}".format(end - begin))


if __name__ == '__main__':
    input_dir = 'output_by_emotion'
    output_dir = 'Models'
    model_name = 'Emotion7NewParam'
    model_type = MODEL_TYPES[2]
    output_name = model_type + model_name
    model_to_create_path = os.path.join(output_dir, output_name)

    make_model(input_dir, model_to_create_path)
    ml_analysis = MLAnalysis(model_to_create_path, model_type)

    ml_analysis.global_analysis()
