import matplotlib.pyplot as plt
import pprint
import numpy

pp = pprint.PrettyPrinter(indent=4)
import pickle

# cPickle.dump(X, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(Y, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(MEAN, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(STD, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(classNames, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(bestParam, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(mt_win, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(mt_step, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(st_win, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(st_step, fo, protocol=cPickle.HIGHEST_PROTOCOL)
# cPickle.dump(compute_beat, fo, protocol=cPickle.HIGHEST_PROTOCOL)

pickle_file_name = 'Models/knnEmotion7'
model_type = 'knn'

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

MAP_DUMP_MORE_INFO = {
    'knn': [
        'Params',
        'ac_all',
        'f1_all',
        'precision_classes_al',
        'recall_classes_all',
        'f1_classes_all',
        'confusion_matrix'
    ]
}

def printConfusionMatrix(cm, class_names):
    '''
    This function prints a confusion matrix for a particular classification task.
    ARGUMENTS:
        cm:            a 2-D numpy array of the confusion matrix
                       (cm[i,j] is the number of times a sample from class i was classified in class j)
        class_names:    a list that contains the names of the classes
    '''

    if cm.shape[0] != len(class_names):
        print("printConfusionMatrix: Wrong argument sizes\n")
        return

    print("{:7s}".format(" "), end="")
    for c in class_names:
        print("{0:>7.5s}".format(c), end="")
    print("")

    for i, c in enumerate(class_names):
        if len(c) > 4:
            c = c[0:3]
        print("{0:7s}".format(c), end="")
        for j in range(len(class_names)):
            print("{0:7.2f}".format(100.0 * cm[i][j] / numpy.sum(cm)), end="")
        print("")

def print_data(params, ac_all, f1_all, precision_classes_all, recall_classes_all, f1_classes_all, class_names):
    print(" " * 5, end="")
    for i, c in enumerate(class_names):
        if i == len(class_names) - 1:
            print("{0:^15s}".format(c), end="")
        else:
            print("{0:^15s}".format(c), end="")
    print("{0:^15s}".format("OVERALL"))

    print("{0:^5s}".format("C"), end="")
    for c in class_names:
        print("{0:^5s}{1:^5s}{2:^5s}".format("PREC", "REC", "F1"), end="")
    print("{0:^5s}{1:s}".format("ACC", "f1"))
    best_ac_ind = numpy.argmax(ac_all)
    best_f1_ind = numpy.argmax(f1_all)
    for i in range(len(precision_classes_all)):
        print("{0:^5.3f}".format(params[i]), end="")
        for c in range(len(precision_classes_all[i])):
            print("{0:^5.1f}{1:^5.1f}{2:^5.1f}".format(100.0 * precision_classes_all[i][c],
                                                       100.0 * recall_classes_all[i][c],
                                                       100.0 * f1_classes_all[i][c]), end="")
        print("{0:^5.1f}{1:^5.1f}".format(100.0 * ac_all[i], 100.0 * f1_all[i]), end="")
        if i == best_f1_ind:
            print("\t best f1", end="")
        if i == best_ac_ind:
            print("\t best Acc", end="")
        print("")

if __name__ == '__main__':
    with open(pickle_file_name, 'rb') as f:
        pickle_obj = pickle.Unpickler(f)
        infos = {name: pickle_obj.load() for name in MAP_DUMP_INFO[model_type]}
        # pp.pprint(infos)

    class_name_list = infos['classNames']
    print("class_name_list: {}".format(class_name_list))
    

    with open(pickle_file_name + '.more_info', 'rb') as f:
        pickle_obj = pickle.Unpickler(f)
        more_infos = {name: pickle_obj.load() for name in MAP_DUMP_MORE_INFO[model_type]}
        # pp.pprint(more_infos)

    confusion_matrix = more_infos['confusion_matrix']
    pp.pprint(confusion_matrix)
    pp.pprint(numpy.sum(confusion_matrix, 1))

    printConfusionMatrix(confusion_matrix, class_name_list)


