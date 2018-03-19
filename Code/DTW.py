from math import *
import os
import settings as st
import pandas as pd
import sys


def DTW_algorithm(Sig1,Sig2):
    n=len(Sig1)
    m=len(Sig2)
    DTW = [[0] * m for i in range(n)]
    for i in range (1,n):
        DTW[i][0] = inf
    for i in range (1,m):
        DTW[0][i] = inf

    DTW[0][0] = 0

    for i in range (0,n):
        for j in range (0,m):
            cost= sqrt((Sig1[i][0]-Sig2[j][0])**2 + (Sig1[i][1]-Sig2[j][1])**2 + (Sig1[i][2]-Sig2[j][2])**2 )
            DTW[i][j]=cost + min(DTW[i-1][ j], DTW[i ][ j-1], DTW[i-1][ j-1])

    return DTW[n-1][m-1]


def read_csv(csv_file_path):
        dataset = pd.read_csv(csv_file_path)
        x = dataset['X']
        y = dataset[' Y']
        p = dataset[' P']
        x = [int(e) for e in x]
        y = [int(e) for e in y]
        p = [int(e) for e in p]
        return x, y,p

def concat_parameters_matrix(x,y,p):
    sig = [[0] * 3 for i in range(len(x))]
    for i in range(0, len(x)):
        sig[i][0] = x[i];
        sig[i][1] = y[i];
        sig[i][2] = p[i];
    return sig


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
