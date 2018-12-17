import pprint

import matplotlib
import matplotlib.pyplot as plt
import numpy
import pandas as pd

pp = pprint.PrettyPrinter(indent=4)

pd.set_option('display.max_columns', None)

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
    print("{0:>7.5s}".format("TOTAL"))

    for i, c in enumerate(class_names):
        if len(c) > 4:
            c = c[0:3]
        print("{0:7s}".format(c), end="")
        for j in range(len(class_names)):
            print("{0:7.2f}".format(100.0 * cm[i][j] / numpy.sum(cm[i])), end="")
        print("{0:7.2f}".format(sum(cm[i][:])))


def print_data(params, ac_all, f1_all, precision_classes_all, recall_classes_all, f1_classes_all, class_names):
    print(" " * 6, end="")
    for i, c in enumerate(class_names):
        if i == len(class_names) - 1:
            print("{0:18s}".format(c), end="")
        else:
            print("{0:18s}".format(c), end="")
    print("{0:^15s}".format("OVERALL"))

    print("{0:^6.5s}".format("C"), end="")
    for c in class_names:
        print("{0:^6.5s}{1:^6.5s}{2:^6.5s}".format("PREC", "REC", "F1"), end="")
    print("{0:^6.5s}{1:^6.5s}".format("ACC", "f1"))
    best_ac_ind = numpy.argmax(ac_all)
    best_f1_ind = numpy.argmax(f1_all)
    for i in range(len(precision_classes_all)):
        print("{0:^6.1f}".format(params[i]), end="")
        for c in range(len(precision_classes_all[i])):
            print("{0:^6.1f}{1:^6.1f}{2:^6.1f}".format(100.0 * precision_classes_all[i][c],
                                                       100.0 * recall_classes_all[i][c],
                                                       100.0 * f1_classes_all[i][c]), end="")
        print("{0:^6.1f}{1:^6.1f}".format(100.0 * ac_all[i], 100.0 * f1_all[i]), end="")
        if i == best_f1_ind:
            print("\t best f1", end="")
        if i == best_ac_ind:
            print("\t best Acc", end="")
        print("")


def plot_confusion_matrix(cm, class_names, title, cmap=plt.cm.Blues, desc=None):
    valfmt = "{x:.2f}%"
    to_plots = [{
        'name': 'Recall',
        'fct': lambda x, y: 100 * cm[x][y] / numpy.sum(cm, 1)[y]
    },
        {
            'name': 'Precision',
            'fct': lambda x, y: 100 * cm[x][y] / numpy.sum(cm, 0)[y]
        }]

    for to_plot in to_plots:
        fig, ax = plt.subplots()

        data = numpy.array([[to_plot['fct'](i, j) for j in
                             range(len(class_names))] for i, c in enumerate(class_names)])
        im = ax.imshow(data, cmap=cmap)
        ax.set_title("{0} {1}\n{2}".format(title, to_plot['name'], desc), pad=50.0)

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, shrink=0.8)
        cbar.ax.set_ylabel("Percentage", rotation=-90, va="bottom")

        # We want to show all ticks...
        ax.set_xticks(numpy.arange(len(class_names)))
        ax.set_yticks(numpy.arange(len(class_names)))

        # ... and label them with the respective list entries
        ax.set_xticklabels(class_names)
        ax.set_yticklabels(class_names)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False,
                       labeltop=True, labelbottom=False)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
                 rotation_mode="anchor")

        # Turn spines off and create white grid.
        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_xticks(numpy.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(numpy.arange(data.shape[0] + 1) - .5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        # Set default alignment to center, but allow it to be
        # overwritten by textkw.
        kw = dict(horizontalalignment="center",
                  verticalalignment="center",
                  fontsize=8)

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        thresh = cm.max() / 2
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                im.axes.text(j, i, valfmt(data[i, j], None),
                             color="white" if cm[i, j] > thresh else "black",
                             **kw)
        fig.savefig('{0}.{1}.png'.format(title, to_plot['name']), bbox_inches='tight')

    plt.show()


def result_data_to_dataframe(params, ac_all, f1_all, precision_classes_all, recall_classes_all, f1_classes_all,
                             class_names):
    col_names_by_class = ["PREC", "REC", "F1"]

    name_overall = 'OVERALL'
    col_names_best = ["ACC", "F1"]
    best_acc_name = 'Best accuracy'
    best_name_f1 = 'Best F1'
    col_name_index = 'Param'

    col_names_total = class_names + [name_overall]
    # We regroupe the data contained in each list in a global dataframe
    data = [precision_classes_all, recall_classes_all, f1_classes_all]
    df_list = []
    for i, name in enumerate(class_names):
        df = pd.DataFrame(
            {
                col_name: [
                    round(100 * data[i_col][i_params][i], 1)
                    for i_params in range(len(params))
                ]
                for i_col, col_name in enumerate(col_names_by_class)
            }, index=params)
        df_list.append(df.T)

    best_ac_ind = numpy.argmax(ac_all)
    best_f1_ind = numpy.argmax(f1_all)
    best_name = [[best_acc_name, best_ac_ind], [best_name_f1, best_f1_ind]]
    df_best = pd.DataFrame({
        param_name: [
            '-' if i != best_name[i_best][1] else best_name[i_best][0]
            for i_best in range(len(best_name))
        ] for i, param_name in enumerate(params)
    }, index=col_names_best
    )
    df_list.append(df_best)
    result = pd.concat(df_list, keys=col_names_total).T
    result.index.name = col_name_index
    return result
