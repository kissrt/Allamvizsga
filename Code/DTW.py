from math import *
import os
import settings as st
import pandas as pd
import sys

from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn import metrics
import matplotlib.pyplot as plt

# def DTW_algorithm(Sig1,Sig2):
#     n=len(Sig1[0])
#     m=len(Sig2[0])
#     DTW = [[0] * (m+1) for i in range(n+1)]
#     for i in range (1,n):
#         DTW[i][0] = inf
#     for i in range (1,m):
#         DTW[0][i] = inf
#
#     DTW[0][0] = 0
#
#     for i in range (1,n+1):
#         for j in range (1,m+1):
#             cost= sqrt((Sig1[i-1][0]-Sig2[j-1][0])**2 + (Sig1[i-1][1]-Sig2[j-1][1])**2 + (Sig1[i-1][2]-Sig2[j-1][2])**2 )
#             DTW[i][j]=cost + min(DTW[i-1][ j], DTW[i ][ j-1], DTW[i-1][ j-1])
#
#     return DTW[n][m]

def DTW_algorithm(Sig1,Sig2):
    n=len(Sig1[0])
    m=len(Sig2[0])
    DTW = [[0] * (m+1) for i in range(n+1)]
    for i in range (1,n):
        DTW[i][0] = inf
    for i in range (1,m):
        DTW[0][i] = inf

    DTW[0][0] = 0

    for i in range (1,n+1):
        for j in range (1,m+1):
            distance()
            DTW[i][j]=cost + min(DTW[i-1][ j], DTW[i ][ j-1], DTW[i-1][ j-1])

    return DTW[n][m]


def read_csv(csv_file_path):
        dataset = pd.read_csv(csv_file_path)
        x = dataset['X']
        y = dataset[' Y']
        p = dataset[' P']
        x = [int(e) for e in x]
        y = [int(e) for e in y]
        p = [int(e) for e in p]
        return x,y,p

def concat_parameters_matrix(x,y,p):
    sig = [[0] * 3 for i in range(len(x))]
    for i in range(0, len(x)):
        sig[i][0] = x[i];
        sig[i][1] = y[i];
        sig[i][2] = p[i];
    return sig
def concat_parameters_matrix2(x,y):
    sig = [[0] * 2 for i in range(len(x))]
    for i in range(0, len(x)):
        sig[i][0] = x[i];
        sig[i][1] = y[i];
    return sig
def concat_parameters_matrix4(x,y,x1,y1):
    sig = [[0] * 4 for i in range(len(x))]
    for i in range(0, len(x)):
        sig[i][0] = x[i];
        sig[i][1] = y[i];
        sig[i][2] = x1[i];
        sig[i][3] = y1[i];
    return sig
def concat_parameters_matrix5(x,y,x1,y1,p):
    sig = [[0] * 5 for i in range(len(x))]
    for i in range(0, len(x)):
        sig[i][0] = x[i];
        sig[i][1] = y[i];
        sig[i][2] = x1[i];
        sig[i][3] = y1[i];
        sig[i][4] = p[i];
    return sig
def plotAUC(scorefilename ):
    data_no = pd.read_csv(scorefilename, names=['label','score'])
    labels_no = data_no['label']
    scores_no = data_no['score']
    labels_no = [int(e)   for e in labels_no]
    scores_no = [float(e) for e in scores_no]
    auc_value_no =   metrics.roc_auc_score(pd.np.array(labels_no), pd.np.array(scores_no))

    fpr_no, tpr_no, thresholds_no = metrics.roc_curve(labels_no, scores_no, pos_label=1)
    eer_no = brentq(lambda x: 1. - x - interp1d(fpr_no, tpr_no)(x), 0., 1.)
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
def calculate_eer(scorefilename ):
    data_no = pd.read_csv(scorefilename, names=['label','score'])
    labels_no = data_no['label']
    scores_no = data_no['score']
    labels_no = [int(e)   for e in labels_no]
    scores_no = [float(e) for e in scores_no]
    auc_value_no =   metrics.roc_auc_score(pd.np.array(labels_no), pd.np.array(scores_no))

    fpr_no, tpr_no, thresholds_no = metrics.roc_curve(labels_no, scores_no, pos_label=1)
    eer_no = brentq(lambda x: 1. - x - interp1d(fpr_no, tpr_no)(x), 0., 1.)
    return eer_no
def main(argv, mlpy=None):

    current_user_dir = os.path.join(st.DIRECTORY_PATH_MCYT, '0001')
    signatures = os.listdir(current_user_dir)
    for k in range (0,24):
        for l in range (0,24):
            csv_file_path = os.path.join(current_user_dir, signatures[k])
            x,y,p = read_csv(csv_file_path)
            csv_file_path = os.path.join(current_user_dir, signatures[l])
            x1, y1, p1 = read_csv(csv_file_path)

            sig1 = concat_parameters_matrix(x,y,p)
            sig2 = concat_parameters_matrix(x1,y1,p1)

            print(DTW_algorithm(sig1,sig2))


if __name__ == "__main__":
    main(sys.argv)
