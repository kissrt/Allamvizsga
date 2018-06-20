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


class ConfigurePlotSignaturesTab():
    def __init__(self):
        window = Tk()
        frame = Frame(window, background='white')
        dropDownList = StringVar(frame)
        scaleGEN = Scale(frame, from_=1, to=25, orient=HORIZONTAL)
        scaleGEN.bind("<ButtonRelease-1>", self.settings_changed)
        scaleFOR = Scale(frame, from_=1, to=20, orient=HORIZONTAL)
        scaleFOR.bind("<ButtonRelease-1>", self.settings_changed)
        users_listbox = Listbox(frame, selectmode=SINGLE, font=("Helvetica", 12), width=15, height=17)
        figure = Figure(figsize=(5, 5))
        subplot = figure.add_subplot(111)
        figure_canvas = FigureCanvasTkAgg(figure, master=window)
        btnnext = Button(window, text=u"\u23F5", command=self.next, font=("Helvetica", 15))
        btnnext.pack()
        btnnext.place(x=420, y=490)
        btnprev = Button(window, text=u"\u23F4", command=self.prev, font=("Helvetica", 15))
        btnprev.pack()
        btnprev.place(x=370, y=490)
        btnfirst = Button(window, text=u"\u23EA", command=self.first, font=("Helvetica", 15))
        btnfirst.pack()
        btnfirst.place(x=320, y=490)
        btnlast = Button(window, text=u"\u23E9", command=self.last, font=("Helvetica", 15))
        btnlast.pack()
        btnlast.place(x=470, y=490)

        dataset = MCYTDataset()

    def start_page(self):
        self.window.title("Plot Signatures")
        self.window.title("Plot Signatures")
        self.window.resizable(False, False)
        self.window.configure(background='white')

        self.frame.pack(side="left")
        Label(self.frame, text="Dataset", font=("Helvetica", 10), background='white', width=15).pack()

        w = OptionMenu(self.frame, self.dropDownList, *DATASET_OPTIONS)
        w.config(width=13)
        self.dropDownList.trace('w', self.settings_changed)
        self.dropDownList.set(DATASET_OPTIONS[0])  # default value
        w.pack()

        # scale - genuine signature number
        Label(self.frame, text="Genuine signatures number", font=("Helvetica", 10), background='white', width=20).pack()
        self.scaleGEN.pack()

        # scale - forgery signature number
        Label(self.frame, text="Forgery signatures number", font=("Helvetica", 10), background='white', width=20).pack()
        self.scaleFOR.pack()

        Label(self.frame, text="Users", font=("Helvetica", 14), background='white').pack()

        self.users_listbox.select_set(0)
        self.users_listbox.bind('<<ListboxSelect>>', plot)  # default selection
        self.users_listbox.event_generate("<<ListboxSelect>>")
        self.users_listbox.pack(side="left", fill="y")
        self.add_scrollbar_to_listbox();


    def add_scrollbar_to_listbox(self):
        scrollbar = Scrollbar(self.frame, orient="vertical")
        scrollbar.config(command=self.users_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.users_listbox.config(yscrollcommand=scrollbar.set)

    def settings_changed(self):
        self.users_listbox.delete(0, END)
        global dataset
        if (self.dropDownList.get() == "MCYT"):
            dataset = MCYTDataset()
            self.scaleFOR.config(to=25)
            self.scaleGEN.config(to=25)
        else:
            dataset = self.MOBISIGDataset()
            self.scaleFOR.config(to=20)
            self.scaleGEN.config(to=45)
        self.users_listbox.select_set(0)
        self.refresh_window()

    def refresh_window(self):
        dataset.calc_signatures_directory()
        self.subplot.clear()
        dataset.set_label_text()
        [x, y] = dataset.read_csv_file_()
        self.subplot.plot(x, y, marker='.', linestyle='none')
        if (self.dropDownList.get() == "MOBISIG"):
            self.subplot.invert_yaxis()
        self.figure_canvas.get_tk_widget().pack()
        self.figure_canvas.draw()

    def plot(self):
        dataset.calc_signatures_directory()
        self.subplot.clear()
        dataset.set_label_text()
        [x, y] = dataset.read_csv_file_()
        self.subplot.plot(x, y, marker='.', linestyle='none')
        if (self.dropDownList.get() == "MOBISIG"):
            self.subplot.invert_yaxis()
        self.figure_canvas.get_tk_widget().pack()
        self.figure_canvas.draw()

    def next(self):
        dataset.calculate_next_file()
        self.refresh_window()

    def prev(self):
        dataset.calculate_prev_file()
        self.refresh_window()

    def first(self):
        dataset.calculate_first_file()
        self.refresh_window()

    def last(self):
        dataset.calculate_last_file()
        self.refresh_window()

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
        self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MOBISIG, plotSignatures_tab.users_listbox.get(plotSignatures_tab.users_listbox.curselection()))
        self.signatures = os.listdir(self.current_user_dir)

    def insert_elements_in_users_listbox(self):
        for dir in self.list_of_directorys(st.DIRECTORY_PATH_MOBISIG):
            plotSignatures_tab.users_listbox.insert(END, dir)

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
            plotSignatures_tab.subplot.set_title("Forgery/" + file_num)
        else:
            plotSignatures_tab.subplot.set_title("Genuine/" + file_num)

    def calculate_next_file(self):
        if((self.signature_index +1) == plotSignatures_tab.scaleFOR.get()) : #jon GEN
            self.signature_index = 20
        elif(self.signature_index == (19+plotSignatures_tab.scaleGEN.get())):#jon FOR
            self.signature_index = 0
        else:
            self.signature_index +=1

    def calculate_prev_file(self):
        if(self.signature_index == 0):
            self.signature_index = 19+plotSignatures_tab.scaleGEN.get()
        elif(self.signature_index == 20):
            self.signature_index = plotSignatures_tab.scaleFOR.get() - 1
        else:
            self.signature_index -=1

    def calculate_first_file(self):
        self.signature_index = 0

    def calculate_last_file(self):
        self.signature_index = 19+plotSignatures_tab.scaleGEN.get()




class MCYTDataset(IDataset):

    def __init__(self):
        self.insert_elements_in_users_listbox()
        self.signature_index = 0

    def calc_signatures_directory(self):
        self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MCYT, plotSignatures_tab.users_listbox.get(plotSignatures_tab.users_listbox.curselection()))
        self.signatures = os.listdir(self.current_user_dir)
        if plotSignatures_tab.users_listbox.get(plotSignatures_tab.users_listbox.curselection()) == '0000':
            self.signatures.pop(0)

    def insert_elements_in_users_listbox(self):
        for dir in self.list_of_directorys(st.DIRECTORY_PATH_MCYT) :
            plotSignatures_tab.users_listbox.insert(END, dir)

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
            plotSignatures_tab.subplot.set_title("Forgery/" + file_num)
        else:
            plotSignatures_tab.subplot.set_title("Genuine/" + file_num)

    def calculate_next_file(self):
        if((self.signature_index +1) == plotSignatures_tab.scaleFOR.get()) : #jon GEN
            self.signature_index = 25
        elif(self.signature_index == (24+plotSignatures_tab.scaleGEN.get())):#jon FOR
            self.signature_index = 0
        else:
            self.signature_index +=1

    def calculate_prev_file(self):
        if(self.signature_index == 0):
            self.signature_index = 24+plotSignatures_tab.scaleGEN.get()
        elif(self.signature_index == 24):
            self.signature_index = plotSignatures_tab.scaleFOR.get() - 1
        else:
            self.signature_index -=1

    def calculate_first_file(self):
        self.signature_index = 0

    def calculate_last_file(self):
        self.signature_index = 24+plotSignatures_tab.scaleGEN.get()


if __name__ == '__main__':
    plotSignatures_tab=ConfigurePlotSignaturesTab()
    plotSignatures_tab.window.mainloop()