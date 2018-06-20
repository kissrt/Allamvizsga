from tkinter import *
import os
from tkinter import ttk
import settings as st
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn import metrics

DATASET_OPTIONS = [
        "MCYT",
        "MOBISIG"
]

FEATURES_OPTIONS = [
        "XY",
        "X'Y'",
        "XYX'Y'",
        "XYP",
        "XYX'Y'P"

]

RESULTS_OPTIONS = [
    "EER",
    "AUC"

]
class IDataset:

        def calc_signatures_directory(self): pass

        def insert_elements_in_users_listbox(self): pass

        def read_csv_file_(self): pass

        def set_label_text(self): pass

        def calculate_next_file(self): pass

        def calculate_prev_file(self): pass

        def calculate_first_file(self): pass

        def calculate_last_file(self): pass

        def list_of_directorys(self, dir):
            return [f for f in os.listdir(dir)]


class MOBISIGDataset(IDataset):
        def __init__(self):
            self.insert_elements_in_users_listbox()
            self.signature_index = 0

        def calc_signatures_directory(self):
            self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MOBISIG,
                                                 users_listbox.get(users_listbox.curselection()))
            self.signatures = os.listdir(self.current_user_dir)

        def insert_elements_in_users_listbox(self):
            for dir in self.list_of_directorys(st.DIRECTORY_PATH_MOBISIG):
                users_listbox.insert(END, dir)

        def read_csv_file_(self):
            csv_file_path = os.path.join(self.current_user_dir, self.signatures[self.signature_index])
            dataset = pd.read_csv(csv_file_path)
            x = dataset['x']
            y = dataset['y']
            x = [int(e) for e in x]
            y = [int(e) for e in y]
            return x, y

        def set_label_text(self):
            file_num = (self.signatures[self.signature_index].split("_")[4]).split(".")[0]
            if self.signatures[self.signature_index][5:8] == 'FOR':
                subplot.set_title("Forgery/" + file_num)
            else:
                subplot.set_title("Genuine/" + file_num)

        def calculate_next_file(self):
            if ((self.signature_index + 1) == scaleFOR.get()):  # jon GEN
                self.signature_index = 20
            elif (self.signature_index == (19 + scaleGEN.get())):  # jon FOR
                self.signature_index = 0
            else:
                self.signature_index += 1

        def calculate_prev_file(self):
            if (self.signature_index == 0):
                self.signature_index = 19 + scaleGEN.get()
            elif (self.signature_index == 20):
                self.signature_index = scaleFOR.get() - 1
            else:
                self.signature_index -= 1

        def calculate_first_file(self):
            self.signature_index = 0

        def calculate_last_file(self):
            self.signature_index = 19 + scaleGEN.get()


class MCYTDataset(IDataset):

        def __init__(self):
            self.insert_elements_in_users_listbox()
            self.signature_index = 0

        def calc_signatures_directory(self):
            self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MCYT,
                                                 users_listbox.get(users_listbox.curselection()))
            self.signatures = os.listdir(self.current_user_dir)
            if users_listbox.get(users_listbox.curselection()) == '0000':
                self.signatures.pop(0)

        def insert_elements_in_users_listbox(self):
            for dir in self.list_of_directorys(st.DIRECTORY_PATH_MCYT):
                users_listbox.insert(END, dir)

        def read_csv_file_(self):
            csv_file_path = os.path.join(self.current_user_dir, self.signatures[self.signature_index])
            dataset = pd.read_csv(csv_file_path)
            x = dataset[u'X']
            y = dataset[u' Y']
            x = [int(e) for e in x]
            y = [int(e) for e in y]
            return x, y

        def set_label_text(self):
            file_num = str(int(self.signatures[self.signature_index][5:7]) + 1)
            if self.signatures[self.signature_index][4:5] == 'f':
                subplot.set_title("Forgery/" + file_num)
            else:
                subplot.set_title("Genuine/" + file_num)

        def calculate_next_file(self):
            if ((self.signature_index + 1) == scaleFOR.get()):  # jon GEN
                self.signature_index = 25
            elif (self.signature_index == (24 + scaleGEN.get())):  # jon FOR
                self.signature_index = 0
            else:
                self.signature_index += 1

        def calculate_prev_file(self):
            if (self.signature_index == 0):
                self.signature_index = 24 + scaleGEN.get()
            elif (self.signature_index == 24):
                self.signature_index = scaleFOR.get() - 1
            else:
                self.signature_index -= 1

        def calculate_first_file(self):
            self.signature_index = 0

        def calculate_last_file(self):
            self.signature_index = 24 + scaleGEN.get()


class ConfigurePlotSignatureWindow:
        def __init__(self):
            window.title("Experiments")
            window.configure(background='white')

            frame.pack(side="left")
            Label(frame, text="Dataset", font=("Helvetica", 10), background='white', width=15).pack()

            w = OptionMenu(frame, dropDownList, *DATASET_OPTIONS)
            w.config(width=13)
            dropDownList.trace('w', settings_changed)
            dropDownList.set(DATASET_OPTIONS[0])  # default value
            w.pack()

            # scale - genuine signature number
            Label(frame, text="Genuine signatures number", font=("Helvetica", 10), background='white', width=20).pack()
            scaleGEN.pack()

            # scale - forgery signature number
            Label(frame, text="Forgery signatures number", font=("Helvetica", 10), background='white', width=20).pack()
            scaleFOR.pack()

            Label(frame, text="Users", font=("Helvetica", 14), background='white').pack()

            users_listbox.select_set(0)
            users_listbox.bind('<<ListboxSelect>>', plot)  # default selection
            users_listbox.event_generate("<<ListboxSelect>>")
            users_listbox.pack(side="left", fill="y")
            self.add_scrollbar_to_listbox()
            notebook.add(frame_plot_signature, text='PlotSignatures')
            notebook.pack(expand=1, fill="both")


        def add_scrollbar_to_listbox(self):
            scrollbar = Scrollbar(frame, orient="vertical")
            scrollbar.config(command=users_listbox.yview)
            scrollbar.pack(side="right", fill="y")
            users_listbox.config(yscrollcommand=scrollbar.set)


class ConfigureLocalFeaturesWindow:
    def __init__(self):
        dataset_label_frame = LabelFrame(frame_experiments)
        dataset_label_frame.grid(row=0, columnspan=7, sticky='W', \
                     padx=20, pady=10, ipadx=300, ipady=40)
        Label(frame_experiments, text="Dataset:", font=("Helvetica", 14)).grid(row=0, column=1, padx=5, pady=35)

        w = OptionMenu(frame_experiments, dropDownList_dataset, *DATASET_OPTIONS)
        w.config(width=20)
        dropDownList_dataset.trace('w', dataset_changed)
        dropDownList_dataset.set(DATASET_OPTIONS[0])  # default value
        w.grid(row=0, column=2, padx=5, pady=35)


        Label(frame_experiments, text="Users:", font=("Helvetica", 14),bg="white").grid(row=1, column=0,padx=20, pady=20)
        Label(frame_experiments, text="From", font=("Helvetica", 12),bg="white").grid(row=1, column=1, padx=0, pady=0)
        scaleFROM.config(length=150)
        scaleFROM.bind("<ButtonRelease-1>", scaleFrom_changed)
        scaleFROM.grid(row=1, column=2, padx=5, pady=35)

        # scale - forgery signature number
        Label(frame_experiments, text="To", font=("Helvetica", 12),bg="white").grid(row=1, column=3, padx=0, pady=0)
        scaleTO.config(length=150)
        scaleTO.grid(row=1, column=4, padx=5, pady=35)

        features_label_frame = LabelFrame(frame_experiments)
        features_label_frame.grid(row=2, columnspan=7, sticky='W', \
                                 padx=20, pady=10, ipadx=300, ipady=40)
        Label(frame_experiments, text="Features:", font=("Helvetica", 14)).grid(row=2, column=1, padx=20, pady=10)
        w = OptionMenu(frame_experiments, dropDownList_features, *FEATURES_OPTIONS)
        w.config(width=20)
        dropDownList_features.set(FEATURES_OPTIONS[0])  # default value
        w.grid(row=2, column=2,padx=5, pady=35)


        results_label_frame = LabelFrame(frame_experiments)
        results_label_frame.grid(row=3, columnspan=7, sticky='W', \
                                  padx=20, pady=10, ipadx=300, ipady=40)

        Label(frame_experiments, text="Results:", font=("Helvetica", 14)).grid(row=3, column=1, padx=5, pady=35)
        w = OptionMenu(frame_experiments, dropDownList_results, *RESULTS_OPTIONS)
        w.config(width=20)
        dropDownList_results.set(RESULTS_OPTIONS[0])  # default value
        w.grid(row=3, column=2, padx=5, pady=35)
        run_button.config(width=15)
        run_button.grid(row=4, column=4, padx=5, pady=35)

        notebook.add(frame_experiments, text='LocalFeatures')
        notebook.pack(expand=1, fill="x")
        window.mainloop()
#
# def read_csv_file_(file):
#     dataset = pd.read_csv(file)
#     if dropDownList_dataset.get()=='MCYT':
#         x = dataset['X']
#         y = dataset[' Y']
#         p = dataset[' P']
#     else:
#          x = dataset['x']
#          y = dataset['y']
#          p = dataset['pressure']
#
#     x = [int(e) for e in x]
#     y = [int(e) for e in y]
#     p=[int(e) for e in p]
#     return x, y,p

def settings_changed(*args):
        users_listbox.delete(0, END)
        global dataset
        if (dropDownList.get() == "MCYT"):
            dataset = MCYTDataset()
            scaleFOR.config(to=25)
            scaleGEN.config(to=25)
        else:
            dataset = MOBISIGDataset()
            scaleFOR.config(to=20)
            scaleGEN.config(to=45)
        users_listbox.select_set(0)
        refresh_window()

def scaleFrom_changed(*args):
    scaleTO.config(from_=scaleFROM.get()+1)

def dataset_changed(*args):
    if (dropDownList_dataset.get() == "MCYT"):
        scaleFROM.config(to=25)
        scaleTO.config(to=25)
    else:
        scaleFROM.config(to=20)
        scaleTO.config(to=45)

def concat_features_to_matrix(x,y,p):
    sig = [[0] * 3 for i in range(len(x))]
    for i in range(0, len(x)):
        sig[i][0] = x[i];
        sig[i][1] = y[i];
        sig[i][2] = p[i];

    features = np.array([])
    return features

def ComputeScores(genuines, forgerys,dataset_path):
    signature_template = genuines[:st.TEMPLATE_SIZE]
    scores = []
    # Positive score list
    for i in range(0,st.NUM_GENUINE):
        signature1= read_csv_file_to_matrix(os.path.join(dataset_path,genuines[15+i]))
        signature1=standardize_signature(signature1)
        sumDist=0
        for j in range(0,st.TEMPLATE_SIZE):
            signature2 = read_csv_file_to_matrix(os.path.join(dataset_path,signature_template[j]))
            signature2=standardize_signature(signature2)
            d = DTW_algorithm(signature1,signature2)
            if d == np.nan:
                d=0
            sumDist = sumDist + d
        positive_score = 1 / ((1 + sumDist) / st.TEMPLATE_SIZE)
        scores= scores + [[1,positive_score]]
    #Negative score list
    for i in range(0, st.NUM_FORGERIES):
            signature1= read_csv_file_to_matrix(os.path.join(dataset_path, forgerys[i]))
            signature1=standardize_signature(signature1)
            sumDist = 0
            for j in range(0, st.TEMPLATE_SIZE):
                signature2=read_csv_file_to_matrix(os.path.join(dataset_path, signature_template[j]))
                signature2=standardize_signature(signature2)
                d = DTW_algorithm(signature1, signature2)
                sumDist = sumDist + d
            negative_score = 1/((1 + sumDist)/ st.TEMPLATE_SIZE)
            scores = scores + [[0,negative_score]]

    data_frame = pd.DataFrame(scores,dtype=float)
    data_frame.to_csv(st.CSV_FILENAME, index=False,header=None,mode='a')
    return scores

def compute_local_features(x,y):
    n = len(x)
    x1 = np.zeros((n))
    y1 = np.zeros((n))
    for i in range(1,n):
        x1[i] = x[i] - x[i - 1]
        y1[i] = y[i] - y[i - 1]
    return x1,y1


def read_csv_file_to_matrix(file):
    feature=dropDownList_features.get()
    if dropDownList_dataset.get() == 'MCYT':
        col_x = 'X'
        col_y = ' Y'
        col_p = ' P'
    else:
        col_x = 'x'
        col_y = 'y'
        col_p = 'pressure'
    dataset = pd.read_csv(file)
    x = dataset[col_x]
    y = dataset[col_y]
    if feature == 'XY':
        a = np.zeros((len(x), 1))
        a = np.column_stack((x, y))
    if feature == "X'Y'":
        x1, y1 = compute_local_features(x, y)
        a = np.zeros((len(x), 1))
        a = np.column_stack((x1, y1))
    if feature == "XYX'Y'":
        x1, y1 = compute_local_features(x, y)
        a = np.zeros((len(x), 1))
        a = np.column_stack((x, y, x1, y1))
    if feature == "XYX'Y'P":
        p = dataset[col_p]
        x1, y1 = compute_local_features(x, y)
        a = np.zeros((len(x), 1))
        a = np.column_stack((x, y, x1, y1, p))
    if feature == "XYP":
        p = dataset[col_p]
        x1, y1 = compute_local_features(x, y)
        a = np.zeros((len(x), 1))
        a = np.column_stack((x, y, p))
    return a

def standardize_signatureP(p):
    n = len(p)
    mp = np.mean(p)
    sdp = np.std(p)
    p1 = np.zeros((n))
    for i in range(0, n):
        p1[i] = (p[i] - mp)/sdp
    return p1

def standardize_signatureXY_or_X1Y1(x,y):
    n = len(x)
    mx = np.mean(x)
    sdx = np.std(x)
    my = np.mean(y)
    sdy = np.std(y)
    x1=np.zeros((n))
    y1=np.zeros((n))
    for i in range(0,n):
        x1[i]=(x[i]-mx)/sdx
        y1[i]=(y[i]-my)/sdy
    return x1,y1

def standardize_signature(signature):
    feature = dropDownList_features.get()
    if feature == 'XY':
        signature[:, 0], signature[:, 1]=standardize_signatureXY_or_X1Y1(signature[:, 0],signature[:,1])
    if feature == "X'Y'":
        signature[:, 0], signature[:, 1] = standardize_signatureXY_or_X1Y1(signature[:, 0], signature[:, 1])
    if feature == "XYX'Y'":
        signature[:, 0], signature[:, 1] = standardize_signatureXY_or_X1Y1(signature[:, 0], signature[:, 1])
        signature[:, 2], signature[:, 3] = standardize_signatureXY_or_X1Y1(signature[:, 2], signature[:, 3])
    if feature == "XYX'Y'P":
        signature[:, 0], signature[:, 1] = standardize_signatureXY_or_X1Y1(signature[:, 0], signature[:, 1])
        signature[:, 2], signature[:, 3] = standardize_signatureXY_or_X1Y1(signature[:, 2], signature[:, 3])
        signature[:, 4] = standardize_signatureP(signature[:, 4])
    if feature == "XYP":
        signature[:, 0], signature[:, 1] = standardize_signatureXY_or_X1Y1(signature[:, 0], signature[:, 1])
        signature[:, 2] = standardize_signatureP(signature[:, 2])
    return signature

def DTW_algorithm(Sig1,Sig2):
    n=len(Sig1[0])
    m=len(Sig2[0])
    DTW = [[0] * (m+1) for i in range(n+1)]
    for i in range (1,n):
        DTW[i][0] = np.inf
    for i in range (1,m):
        DTW[0][i] = np.inf

    DTW[0][0] = 0

    for i in range (1,n+1):
        for j in range (1,m+1):
            cost = distance(Sig1[i],Sig2[j])
            DTW[i][j]=cost + min(DTW[i-1][ j], DTW[i ][ j-1], DTW[i-1][ j-1])

    return DTW[n][m]



def distanceXY(x,y,x1,y1):
    return np.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
def distanceXYP(x,y,x1,y1,pa,pb):
    return np.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1)+ (pa - pb) * (pa - pb))

def distanceXYX1Y1(xa,ya,xb,yb,x1a,y1a,x1b,y1b):
    return np.sqrt((xa - xb) * (xa - xb) + (ya - yb) * (ya - yb) + (x1a - x1b)*(x1a - x1b) + (y1a - y1b) *(y1a - y1b))

def distanceXYX1Y1P(xa,ya,xb,yb,x1a,y1a,x1b,y1b,pa,pb):
    return np.sqrt((xa - xb) * (xa - xb) + (ya - yb) * (ya - yb) + (x1a - x1b)*(x1a - x1b) + (y1a - y1b) *(y1a - y1b) + (pa - pb) * (pa - pb))

def distance(sig1,sig2):
    feature = dropDownList_features.get()
    if feature == 'XY':
        d=distanceXY(sig1[0],sig1[1],sig2[0],sig2[1])
    if feature == "X'Y'":
        d=distanceXY(sig1[0], sig1[1], sig2[0], sig2[1])
    if feature == "XYX'Y'":
        d=distanceXYX1Y1(sig1[0], sig1[1], sig2[0], sig2[1],sig1[2],sig1[3],sig2[2],sig2[3])
    if feature == "XYX'Y'P":
        d=distanceXYX1Y1P(sig1[0], sig1[1], sig2[0], sig2[1], sig1[2], sig1[3], sig2[2], sig2[3],sig1[4],sig2[4])
    if feature == "XYP":
        d=distanceXYP(sig1[0], sig1[1], sig2[0], sig2[1],sig1[2],sig2[2])
    return d

def calculate_eer(scores):
    label = [e[0] for e in scores]
    scores = [e[1] for e in scores]
    fpr_no, tpr_no, thresholds_no = metrics.roc_curve(label, scores, pos_label=1)
    eer = brentq(lambda x: 1. - x - interp1d(fpr_no, tpr_no)(x), 0., 1.)
    return eer

def run_local_features(*args):
    scores=[]
    data_frame = pd.DataFrame(scores, dtype=float)
    data_frame.to_csv(st.CSV_FILENAME, index=False, header=None)
    directorys = []
    if (dropDownList_dataset.get() == "MCYT"):
        dir_route = st.DIRECTORY_PATH_MCYT
        directorys = [f for f in os.listdir(st.DIRECTORY_PATH_MCYT)][scaleFROM.get()-1:scaleTO.get()]
    else:
        directorys = [f for f in os.listdir(st.DIRECTORY_PATH_MOBISIG)][scaleFROM.get()-1:scaleTO.get()]
        dir_route = st.DIRECTORY_PATH_MOBISIG
    n = len(directorys)
    eers = []
    for dir in directorys:
        directory = os.path.join(dir_route,dir)
        signatures = os.listdir(directory)
        if (dropDownList_dataset.get() == "MCYT"):
            genuines = [os.path.join(dir,f) for f in signatures if (f[4:5]=='v')]
            forgerys = [os.path.join(dir,f) for f in signatures if (f[4:5]=='f')]
        else:
            genuines = [os.path.join(dir, f) for f in signatures if (f[5:6] == 'G')]
            forgerys = [os.path.join(dir, f) for f in signatures if (f[5:6] == 'F')]
        score = ComputeScores(genuines,forgerys,dir_route)
        print(dir + '- user eer:')
        eer = calculate_eer(score)
        print("{0:.2f}".format(eer))
        eers.append(eer)

    if dropDownList_results.get()  == 'EER':
        print('Errs mean:' )
        print("{0:.2f}".format(np.mean(eers)))
    else:
        dtw.plotAUC(st.CSV_FILENAME)

def refresh_window():
        dataset.calc_signatures_directory()
        subplot.clear()
        dataset.set_label_text()
        [x, y] = dataset.read_csv_file_()
        subplot.plot(x, y, marker='.', linestyle='none')
        if (dropDownList.get() == "MOBISIG"):
            subplot.invert_yaxis()
        figure_canvas.get_tk_widget().pack()
        figure_canvas.draw()


def plot(*args):
        dataset.calc_signatures_directory()
        subplot.clear()
        dataset.set_label_text()
        [x, y] = dataset.read_csv_file_()
        subplot.plot(x, y, marker='.', linestyle='none')
        if (dropDownList.get() == "MOBISIG"):
            subplot.invert_yaxis()
        figure_canvas.get_tk_widget().pack()
        figure_canvas.draw()


def next():
        dataset.calculate_next_file()
        refresh_window()


def prev():
        dataset.calculate_prev_file()
        refresh_window()

def first():
        dataset.calculate_first_file()
        refresh_window()

def transform():
    subplot.invert_yaxis()
    subplot.invert_xaxis()
    figure_canvas.get_tk_widget().pack()
    figure_canvas.draw()

def last():
        dataset.calculate_last_file()
        refresh_window()

if __name__ == "__main__":
        window = Tk()
        window.resizable(width=False, height=False)
        notebook = ttk.Notebook(window)

        frame_plot_signature = Frame(notebook, background='white')
        frame = Frame(frame_plot_signature, background='white')
        dropDownList = StringVar(frame)
        scaleGEN = Scale(frame, from_=1, to=25, orient=HORIZONTAL)
        scaleGEN.bind("<ButtonRelease-1>", settings_changed)
        scaleFOR = Scale(frame, from_=1, to=20, orient=HORIZONTAL)
        scaleFOR.bind("<ButtonRelease-1>", settings_changed)
        users_listbox = Listbox(frame, selectmode=SINGLE, font=("Helvetica", 12), width=15, height=17)
        figure = Figure(figsize=(5, 5))

        subplot = figure.add_subplot(111)
        figure_canvas = FigureCanvasTkAgg(figure, master=frame_plot_signature)
        btnnext = Button(frame_plot_signature, text=u"\u23F5", command=next, font=("Helvetica", 15))
        btnnext.pack()
        btnnext.place(x=420, y=490)
        btnprev = Button(frame_plot_signature, text=u"\u23F4", command=prev, font=("Helvetica", 15))
        btnprev.pack()
        btnprev.place(x=370, y=490)
        btnfirst = Button(frame_plot_signature, text=u"\u23EA", command=first, font=("Helvetica", 15))
        btnfirst.pack()
        btnfirst.place(x=320, y=490)
        btnlast = Button(frame_plot_signature, text=u"\u23E9", command=last, font=("Helvetica", 15))
        btnlast.pack()
        btnlast.place(x=470, y=490)
        btnlast = Button(frame_plot_signature, text=u"\u27f2", command=transform, font=("Helvetica", 15))
        btnlast.pack()
        btnlast.place(x=600, y=490)
        dataset = MCYTDataset()
        ConfigurePlotSignatureWindow()

        frame_experiments = Frame(notebook, background='white')
        dropDownList_dataset = StringVar(frame_experiments)

        scaleFROM = Scale(frame_experiments, from_=1, to=25, orient=HORIZONTAL)
        scaleTO = Scale(frame_experiments, from_=1, to=20, orient=HORIZONTAL)
        dropDownList_features= StringVar(frame_experiments)
        dropDownList_results = StringVar(frame_experiments)
        run_button = Button(frame_experiments, text="RUN",command = run_local_features)

        ConfigureLocalFeaturesWindow()







