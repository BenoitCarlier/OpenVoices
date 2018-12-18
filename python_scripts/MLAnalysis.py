import pickle

from python_scripts import visualisation_tools
from pprint import pformat

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


class MLAnalysis:
    # Will read data from pickle file with the name given in param and also for this named file with .more_info
    # Use global_analysis to get quick results
    def __init__(self, pickle_file_name, model_type):
        self.pickle_file_name = pickle_file_name
        self.model_type = model_type
        self.info = None
        self.more_info = None
        self.__read_file()
        self.__read_file_more_info()

    def __read_file(self):
        file_name = self.pickle_file_name
        if self.model_type != 'knn':
            file_name += 'MEANS'

        with open(file_name, 'rb') as f:
            pickle_obj = pickle.Unpickler(f)
            dump_info = MAP_DUMP_INFO.get(model_type) or MAP_DUMP_INFO['default']
            self.info = {name: pickle_obj.load() for name in dump_info}

    def __read_file_more_info(self):
        with open(self.pickle_file_name + '.more_info', 'rb') as f:
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
        data_frame.to_csv(pickle_file_name + ".csv")

        l_desc = ['bestParam', 'mt_win', 'mt_step', 'st_win', 'st_step', 'compute_beat']
        description = ', '.join(['{}: {}'.format(name, self.info[name]) for name in l_desc])
        visualisation_tools.plot_confusion_matrix(confusion_matrix, class_name_list, pickle_file_name, desc=description)


if __name__ == '__main__':
    model_type = 'knn'

    pickle_file_name = 'Models/{}Emotion7'.format(model_type)

    ml_analysis = MLAnalysis(pickle_file_name, model_type)
    ml_analysis.global_analysis()
