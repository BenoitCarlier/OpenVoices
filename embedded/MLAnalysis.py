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
    ]
}


class MLAnalysis:
    def __init__(self, model_type, model_path):
        self.model_type = model_type
        self.model_path = model_path
        self.info = None
        self.__read_file()

    def __read_file(self):
        with open(self.model_path, 'rb') as f:
            pickle_obj = pickle.Unpickler(f)
            self.info = {name: pickle_obj.load() for name in MAP_DUMP_INFO[self.model_type]}

    @property
    def emotions(self):
        return self.info['classNames']

    def get_emotion(self, file_path):
        """
        :param file_path:
        :return: (Result, P, classNames)
        """
        results = aT.fileClassification(file_path,
                                        self.model_path,
                                        self.model_type)
        print("Results : {}".format(results))
        return results
