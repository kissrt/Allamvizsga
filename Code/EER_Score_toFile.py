import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn import model_selection
from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def plotAUC(scorefilename ):
    data_no = pd.read_csv(scorefilename, names=['label','score'])
    labels_no = data_no['label']
    scores_no = data_no['score']
    labels_no = [int(e)   for e in labels_no]
    scores_no = [float(e) for e in scores_no]
    auc_value_no =   metrics.roc_auc_score(np.array(labels_no), np.array(scores_no) )

    fpr_no, tpr_no, thresholds_no = metrics.roc_curve(labels_no, scores_no, pos_label=1)
    eer_no = brentq(lambda x: 1. - x - interp1d(fpr_no, tpr_no)(x), 0., 1.)
    print(eer_no)
    # thresh_no = interp1d(fpr_no, thresholds_no)(eer_no)

    plt.figure()
    lw = 2
    plt.plot(fpr_no,     tpr_no,     color='black', lw=lw, label='AUC = %0.4f' % auc_value_no)
    plt.plot([0, 1], [0, 1], color='darkorange', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('AUC')
    plt.legend(loc="lower right")
    plt.show()
    return

plotAUC("scores.csv")