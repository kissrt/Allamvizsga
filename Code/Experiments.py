from tkinter import *
import os
from tkinter import ttk

import settings as st
import DTW as dtw
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

DATASET_OPTIONS = [
        "MCYT",
        "MOBISIG"
]

FEATURES_OPTIONS = [
        "X",
        "Y",
        "X'",
        "Y'",
        "P"

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
        Label(frame_experiments, text="Dataset", font=("Helvetica", 14), background='white').grid(row=0, column=1, padx=5, pady=35)

        w = OptionMenu(frame_experiments, dropDownList_dataset, *DATASET_OPTIONS)
        w.config(width=20)
        dropDownList_dataset.trace('w', dataset_changed)
        dropDownList_dataset.set(DATASET_OPTIONS[0])  # default value
        w.grid(row=0, column=2, padx=5, pady=35)

        Label(frame_experiments, text="Users", font=("Helvetica", 14), background='white').grid(row=1, column=0,padx=5, pady=35)
        Label(frame_experiments, text="From", font=("Helvetica", 12), background='white').grid(row=1, column=1, padx=5, pady=35)
        scaleFROM.config(length=150)
        scaleFROM.bind("<ButtonRelease-1>", scaleFrom_changed)
        scaleFROM.grid(row=1, column=2, padx=5, pady=35)

        # scale - forgery signature number
        Label(frame_experiments, text="To", font=("Helvetica", 12), background='white').grid(row=1, column=3, padx=5, pady=35)
        scaleTO.config(length=150)
        scaleTO.grid(row=1, column=4, padx=5, pady=35)

        Label(frame_experiments, text="Features", font=("Helvetica", 14), background='white').grid(row=2, column=1, padx=5, pady=35)
        w = OptionMenu(frame_experiments, dropDownList_features, *FEATURES_OPTIONS)
        w.config(width=20)
        dropDownList_features.set(FEATURES_OPTIONS[0])  # default value
        w.grid(row=2, column=2,padx=5, pady=35)

        Label(frame_experiments, text="Results", font=("Helvetica", 14), background='white').grid(row=3, column=1, padx=5, pady=35)
        w = OptionMenu(frame_experiments, dropDownList_results, *RESULTS_OPTIONS)
        w.config(width=20)
        dropDownList_results.set(RESULTS_OPTIONS[0])  # default value
        w.grid(row=3, column=2, padx=5, pady=35)
        run_button.config(width=30)
        run_button.grid(row=4, column=4, padx=5, pady=35)

        notebook.add(frame_experiments, text='LocalFeatures')
        notebook.pack(expand=1, fill="x")
        window.mainloop()

def read_csv_file_(file):
    dataset = pd.read_csv(file)
    x = dataset['X']
    y = dataset[' Y']
    p=dataset[' P']
    x = [int(e) for e in x]
    y = [int(e) for e in y]
    p=[int(e) for e in p]
    return x, y,p

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


def ComputeScores(genuines, forgerys):
    signature_template = genuines[:st.TEMPLATE_SIZE]
    # Positive score list
    positive_scores = []
    for i in range(0,st.NUM_GENUINE):
        x1,y1,p1= read_csv_file_(os.path.join(st.DIRECTORY_PATH_MCYT,genuines[15+i]))
        sumDist=0
        positive_scores = []
        for j in range(0,st.TEMPLATE_SIZE):
            x,y,p = read_csv_file_(os.path.join(st.DIRECTORY_PATH_MCYT,signature_template[j]))
            sign1 = dtw.concat_parameters_matrix(x,y,p)
            sign2= dtw.concat_parameters_matrix(x1,y1,p1)
            d = dtw.DTW_algorithm(sign1,sign2)
            sumDist += d
            positive_scores = positive_scores+[1 / (1 + sumDist / st.TEMPLATE_SIZE)]
        print(positive_scores)
    #Negative score list
    negative_scores = []
    for i in range(0, st.NUM_FORGERIES):
            x1, y1, p1 = read_csv_file_(os.path.join(st.DIRECTORY_PATH_MCYT, forgerys[i]))
            sumDist = 0
            negative_scores = []
            for j in range(0, st.TEMPLATE_SIZE):
                x, y, p = read_csv_file_(os.path.join(st.DIRECTORY_PATH_MCYT, signature_template[j]))
                sign1 = dtw.concat_parameters_matrix(x, y, p)
                sign2 = dtw.concat_parameters_matrix(x1, y1, p1)
                d = dtw.DTW_algorithm(sign1, sign2)
                sumDist += d
                negative_scores = negative_scores + [1 / (1 + sumDist / st.TEMPLATE_SIZE)]
            print(negative_scores)
def run_local_features(*args):
    directorys = []
    if (dropDownList_dataset.get() == "MCYT"):
        dir_route = st.DIRECTORY_PATH_MCYT
        directorys = [f for f in os.listdir(st.DIRECTORY_PATH_MCYT)][scaleFROM.get()-1:scaleTO.get()]
    else:
        directorys = [f for f in os.listdir(st.DIRECTORY_PATH_MOBISIG)][scaleFROM.get()-1:scaleTO.get()]
        dir_route = st.DIRECTORY_PATH_MOBISIG
    for dir in directorys:
        directory = os.path.join(dir_route,dir)
        signatures = os.listdir(directory)
        genuines = [os.path.join(dir,f) for f in signatures if (f[4:5]=='v')]
        forgerys = [os.path.join(dir,f) for f in signatures if (f[4:5]=='f')]

        ComputeScores(genuines,forgerys)


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


def last():
        dataset.calculate_last_file()
        refresh_window()


if __name__ == "__main__":
        window = Tk()
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

        dataset = MCYTDataset()
        ConfigurePlotSignatureWindow()

        frame_experiments = Frame(notebook, background='white')
        dropDownList_dataset = StringVar(frame_experiments)

        scaleFROM = Scale(frame_experiments, from_=1, to=25, orient=HORIZONTAL)
        scaleTO = Scale(frame_experiments, from_=2, to=20, orient=HORIZONTAL)
        dropDownList_features= StringVar(frame_experiments)
        dropDownList_results = StringVar(frame_experiments)
        run_button = Button(frame_experiments, text="RUN",command = run_local_features)

        ConfigureLocalFeaturesWindow()







