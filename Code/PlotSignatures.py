from tkinter import *
import os
import settings as st
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

DATASET_OPTIONS = [
"MCYT",
"MOBISIG"
]

class IDataset:

    def calc_signatures_directory(self): pass

    def insert_elements_in_users_listbox(self): pass

    def read_csv_file_(self):pass

    def set_label_text(self): pass

    def calculate_next_file(self):pass

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
        self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MOBISIG, users_listbox.get(users_listbox.curselection()))
        self.signatures = os.listdir(self.current_user_dir)

    def insert_elements_in_users_listbox(self):
        for dir in self.list_of_directorys(st.DIRECTORY_PATH_MOBISIG):
            users_listbox.insert(END, dir)

    def read_csv_file_(self):
        csv_file_path=os.path.join(self.current_user_dir,self.signatures[self.signature_index])
        dataset = pd.read_csv(csv_file_path)
        x = dataset['x']
        y = dataset['y']
        x = [int(e) for e in x]
        y = [int(e) for e in y]
        return x,y

    def set_label_text(self):
        file_num = (self.signatures[self.signature_index].split("_")[4]).split(".")[0]
        if self.signatures[self.signature_index][5:8] == 'FOR':
            subplot.set_title("Forgery/" + file_num)
        else:
            subplot.set_title("Genuine/" + file_num)

    def calculate_next_file(self):
        if((self.signature_index +1) == scaleFOR.get()) : #jon GEN
            self.signature_index = 20
        elif(self.signature_index == (19+scaleGEN.get())):#jon FOR
            self.signature_index = 0
        else:
            self.signature_index +=1

    def calculate_prev_file(self):
        if(self.signature_index == 0):
            self.signature_index = 19+scaleGEN.get()
        elif(self.signature_index == 20):
            self.signature_index = scaleFOR.get() - 1
        else:
            self.signature_index -=1

    def calculate_first_file(self):
        self.signature_index = 0

    def calculate_last_file(self):
        self.signature_index = 19+scaleGEN.get()




class MCYTDataset(IDataset):

    def __init__(self):
        self.insert_elements_in_users_listbox()
        self.signature_index = 0

    def calc_signatures_directory(self):
        self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MCYT, users_listbox.get(users_listbox.curselection()))
        self.signatures = os.listdir(self.current_user_dir)
        if users_listbox.get(users_listbox.curselection()) == '0000':
            self.signatures.pop(0)

    def insert_elements_in_users_listbox(self):
        for dir in self.list_of_directorys(st.DIRECTORY_PATH_MCYT) :
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
        if((self.signature_index +1) == scaleFOR.get()) : #jon GEN
            self.signature_index = 25
        elif(self.signature_index == (24+scaleGEN.get())):#jon FOR
            self.signature_index = 0
        else:
            self.signature_index +=1

    def calculate_prev_file(self):
        if(self.signature_index == 0):
            self.signature_index = 24+scaleGEN.get()
        elif(self.signature_index == 24):
            self.signature_index = scaleFOR.get() - 1
        else:
            self.signature_index -=1

    def calculate_first_file(self):
        self.signature_index = 0

    def calculate_last_file(self):
        self.signature_index = 24+scaleGEN.get()

class ConfigureWindowProperty:
    def __init__(self):
        window.title("Plot Signatures")
        window.title("Plot Signatures")
        window.resizable(False, False)
        window.configure(background='white')

        frame.pack(side="left")
        Label(frame, text="Dataset", font=("Helvetica", 10), background='white', width=15).pack()

        w = OptionMenu(frame, dropDownList, *DATASET_OPTIONS)
        w.config(width=13)
        dropDownList.trace('w', settings_changed)
        dropDownList.set(DATASET_OPTIONS[0])  # default value
        w.pack()

        # scale - genuine signature number
        Label(frame, text="Genuine signatures number", font=("Helvetica", 10), background='white',width=20).pack()
        scaleGEN.pack()

        # scale - forgery signature number
        Label(frame, text="Forgery signatures number", font=("Helvetica", 10), background='white',width=20).pack()
        scaleFOR.pack()

        Label(frame, text="Users", font=("Helvetica", 14), background='white').pack()

        users_listbox.select_set(0)
        users_listbox.bind('<<ListboxSelect>>', plot)  # default selection
        users_listbox.event_generate("<<ListboxSelect>>")
        users_listbox.pack(side="left", fill="y")
        self.add_scrollbar_to_listbox();
        window.mainloop()

    def add_scrollbar_to_listbox(self):
        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.config(command=users_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        users_listbox.config(yscrollcommand=scrollbar.set)

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
    subplot.plot(x,y,marker = '.',linestyle = 'none')
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



def main(argv):
    ConfigureWindowProperty()


if __name__ == "__main__":
    window = Tk()
    frame = Frame(window,background='white')
    dropDownList = StringVar(frame)
    scaleGEN = Scale(frame,from_=1, to=25, orient=HORIZONTAL)
    scaleGEN.bind("<ButtonRelease-1>", settings_changed)
    scaleFOR = Scale(frame,from_=1, to=20, orient=HORIZONTAL)
    scaleFOR.bind("<ButtonRelease-1>", settings_changed)
    users_listbox = Listbox(frame,selectmode=SINGLE, font=("Helvetica", 12), width=15, height=17)
    figure = Figure(figsize=(5, 5))
    subplot = figure.add_subplot(111)
    figure_canvas = FigureCanvasTkAgg(figure, master=window)
    btnnext = Button(window, text=u"\u23F5", command=next, font=("Helvetica", 15))
    btnnext.pack()
    btnnext.place(x=420, y=490)
    btnprev = Button(window, text=u"\u23F4", command=prev, font=("Helvetica", 15))
    btnprev.pack()
    btnprev.place(x=370, y=490)
    btnfirst = Button(window, text=u"\u23EA", command=first, font=("Helvetica", 15))
    btnfirst.pack()
    btnfirst.place(x=320, y=490)
    btnlast = Button(window, text=u"\u23E9", command=last, font=("Helvetica", 15))
    btnlast.pack()
    btnlast.place(x=470, y=490)

    dataset = MCYTDataset()
    main(sys.argv)