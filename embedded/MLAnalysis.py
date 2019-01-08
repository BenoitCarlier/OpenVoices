import pickle

from pyAudioAnalysis import audioTrainTest as aT

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
    'neural_net': [
        'model'
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



class MLAnalysis:
    def __init__(self, model_type, model_path, verbose=False):
        self.model_type = model_type
        self.model_path = model_path
        self.info = None
        self.verbose = verbose
        self.__read_file()

    def __read_file(self):
        with open(self.model_path, 'rb') as f:
            pickle_obj = pickle.Unpickler(f)
            dump_info = MAP_DUMP_INFO.get(self.model_type) or MAP_DUMP_INFO['default']
            self.info = {name: pickle_obj.load() for name in dump_info}

    @property
    def emotions(self):
        return self.info['classNames']

    def get_emotion(self, file_path):
        """
        :param file_path:
        :return: emotion (str)
        """
        (result_index, P, classNames) = aT.fileClassification(file_path,
                                                              self.model_path,
                                                              self.model_type)
        if self.verbose:
            print("\nresult_index : {}\nP : {}\nclassNames : {}".format(result_index, P, classNames))
        return classNames[result_index]
