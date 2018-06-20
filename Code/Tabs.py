import os
from tkinter import *
from tkinter.ttk import Notebook

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import settings as st
import pandas as pd

class ConfigureWindow:
    def __init__(self):
        self.win = Tk()
        self.win.title("Python GUI App")
        self.win.resizable(False, False)
        self.win.title("Plot Signatures")
        self.win.configure(background='white')
        tabControl = Notebook(self.win)
        plotSignatures=PlotSignaturesWindow(self.win)
        tab1=plotSignatures.frame
        tabControl.add(tab1, text='Plot Signatures')
        tabControl.pack(expand=1, fill="both")


        experiments = ExperimentsWindow(self.win)
        tab2 = experiments.frame
        tabControl.add(tab2, text='Experiments')
        tabControl.pack(expand=1, fill="both")

        # tabControl.add(tab1, text='Tab 1')
        # # Tab1
        # tab1 = Frame(tabControl)
        # tabControl.add(tab1, text='Tab 1')
        # # Tab2
        # tab2 =Frame(tabControl)
        # tabControl.add(tab2, text='Tab 2')
        # tabControl.pack(expand=1, fill="both")

class ExperimentsWindow:

    def __init__(self, window):
        Features = [
            "DTW"
        ]

        Results = [
            "XY",
            "X1Y1",
            "XYX1Y1"
        ]
        self.frame = Frame(window, background='white')
        self.frame.pack()
        Label(self.frame, text="Users", font=("Helvetica", 10), background='white').pack()
        self.users_from= Scale(self.frame, from_=1, to=25, orient=HORIZONTAL, command=self.settings_changed)
        self.users_from.bind("<ButtonRelease-1>", self.settings_changed)
        self.users_to = Scale(self.frame, from_=1, to=20, orient=HORIZONTAL, command=self.settings_changed)
        self.users_to.bind("<ButtonRelease-1>", self.settings_changed)

        Label(self.frame, text="From", font=("Helvetica", 10), background='white').pack()
        self.users_from.pack()

        Label(self.frame, text="To", font=("Helvetica", 10), background='white').pack()
        self.users_to.pack()

        Label(self.frame, text="Features", font=("Helvetica", 10), background='white').pack()
        self.dropDownList = StringVar(self.frame)
        w = OptionMenu(self.frame, self.dropDownList, *Features)
        w.config(width=13)
        self.dropDownList.trace('w', self.settings_changed)
        self.dropDownList.set(Features[0])  # default value
        w.pack()
        Label(self.frame, text="Results", font=("Helvetica", 10), background='white').pack()
        self.dropDownList = StringVar(self.frame)
        w = OptionMenu(self.frame, self.dropDownList, *Results)
        w.config(width=13)
        self.dropDownList.trace('w', self.settings_changed)
        self.dropDownList.set(Results[0])  # default value
        w.pack()

    def settings_changed(self,*args):
        print(self.users_to.get())



class PlotSignaturesWindow:
    DATASET_OPTIONS = [
        "MCYT",
        "MOBISIG"
    ]

    def __init__(self,window):
        self.frame = Frame(window, background='white')
        self.frame.pack(side="left")

        self.dropDownList = StringVar(self.frame)
        w = OptionMenu(self.frame, self.dropDownList, *self.DATASET_OPTIONS)
        w.config(width=13)
        self.dropDownList.trace('w', self.settings_changed)
        self.dropDownList.set(self.DATASET_OPTIONS[0])  # default value
        w.pack()
        self.scaleGEN = Scale(self.frame, from_=1, to=25, orient=HORIZONTAL,command=self.settings_changed)
        self.scaleGEN.bind("<ButtonRelease-1>", self.settings_changed)
        self.scaleFOR = Scale(self.frame, from_=1, to=20, orient=HORIZONTAL,command=self.settings_changed)
        self.scaleFOR.bind("<ButtonRelease-1>", self.settings_changed)
        # scale - genuine signature number
        Label(self.frame, text="Genuine signatures number", font=("Helvetica", 10), background='white', width=20).pack()
        self.scaleGEN.pack()

        # scale - forgery signature number
        Label(self.frame, text="Forgery signatures number", font=("Helvetica", 10), background='white', width=20).pack()
        self.scaleFOR.pack()

        Label(self.frame, text="Dataset", font=("Helvetica", 10), background='white', width=15).pack()
        Label(self.frame, text="Users", font=("Helvetica", 14), background='white').pack()
        self.users_listbox = Listbox(self.frame, selectmode=SINGLE, font=("Helvetica", 12), width=15, height=17)
        self.users_listbox.select_set(0)
        self.users_listbox.bind('<<ListboxSelect>>', self.plot)  # default selection
        self.users_listbox.event_generate("<<ListboxSelect>>")
        self.users_listbox.pack(side="left", fill="y")
        self.add_scrollbar_to_listbox()
        self.figure = Figure(figsize=(5, 5))
        self.subplot = self.figure.add_subplot(111)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=window)
        self.btnnext = Button(window, text=u"\u23F5", command=self.next, font=("Helvetica", 15))
        self.btnnext.pack()
        self.btnnext.place(x=420, y=490)
        self.btnprev = Button(window, text=u"\u23F4", command=self.prev, font=("Helvetica", 15))
        self.btnprev.pack()
        self.btnprev.place(x=370, y=490)
        self.btnfirst = Button(window, text=u"\u23EA", command=self.first, font=("Helvetica", 15))
        self.btnfirst.pack()
        self.btnfirst.place(x=320, y=490)
        self.btnlast = Button(window, text=u"\u23E9", command=self.last, font=("Helvetica", 15))
        self.btnlast.pack()
        self.btnlast.place(x=470, y=490)
        self.dataset = MCYTDataset(self.users_listbox)

    def add_scrollbar_to_listbox(self):
        scrollbar = Scrollbar(self.frame, orient="vertical")
        scrollbar.config(command=self.users_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.users_listbox.config(yscrollcommand=scrollbar.set)

    def settings_changed(self,*args):
        self.users_listbox.delete(0, END)
        if (self.dropDownList.get() == "MCYT"):
            self.dataset = MCYTDataset(self.users_listbox)
            self.scaleFOR.config(to=25)
            self.scaleGEN.config(to=25)
        else:
            self.dataset = MOBISIGDataset(self.users_listbox)
            self.scaleFOR.config(to=20)
            self.scaleGEN.config(to=45)
        self.users_listbox.select_set(0)
        self.refresh_window()

    def refresh_window(self):
        self.dataset.calc_signatures_directory(self.users_listbox)
        self.subplot.clear()
        self.dataset.set_label_text(self.subplot)
        [x, y] = self.dataset.read_csv_file_()
        self.subplot.plot(x, y, marker='.', linestyle='none')
        if (self.dropDownList.get() == "MOBISIG"):
            self.subplot.invert_yaxis()
        self.figure_canvas.get_tk_widget().pack()
        self.figure_canvas.draw()

    def plot(self,*args):
        self.dataset.calc_signatures_directory(self.users_listbox)
        self.subplot.clear()
        self.dataset.set_label_text(self.subplot)
        [x, y] = self.dataset.read_csv_file_()
        self.subplot.plot(x, y, marker='.', linestyle='none')
        if (self.dropDownList.get() == "MOBISIG"):
            self.subplot.invert_yaxis()
        self.figure_canvas.get_tk_widget().pack()
        self.figure_canvas.draw()

    def next(self):
        self.dataset.calculate_next_file(self.scaleFOR,self.scaleGEN)
        self.refresh_window()

    def prev(self):
        self.dataset.calculate_prev_file(self.scaleFOR,self.scaleGEN)
        self.refresh_window()

    def first(self):
        self.dataset.calculate_first_file()
        self.refresh_window()

    def last(self):
        self.dataset.calculate_last_file(self.scaleGEN)
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
    def __init__(self,listbox):
        self.insert_elements_in_users_listbox(listbox)
        self.signature_index = 0

    def calc_signatures_directory(self,listbox):
        self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MOBISIG, listbox.get(listbox.curselection()))
        self.signatures = os.listdir(self.current_user_dir)

    def insert_elements_in_users_listbox(self,listbox):
        for dir in self.list_of_directorys(st.DIRECTORY_PATH_MOBISIG):
            listbox.insert(END, dir)

    def read_csv_file_(self):
        csv_file_path=os.path.join(self.current_user_dir,self.signatures[self.signature_index])
        dataset = pd.read_csv(csv_file_path)
        x = dataset['x']
        y = dataset['y']
        x = [int(e) for e in x]
        y = [int(e) for e in y]
        return x,y

    def set_label_text(self,subplot):
        file_num = (self.signatures[self.signature_index].split("_")[4]).split(".")[0]
        if self.signatures[self.signature_index][5:8] == 'FOR':
            subplot.set_title("Forgery/" + file_num)
        else:
            subplot.set_title("Genuine/" + file_num)

    def calculate_next_file(self,scaleFOR,scaleGEN):
        if((self.signature_index +1) == scaleFOR.get()) : #jon GEN
            self.signature_index = 20
        elif(self.signature_index == (19+scaleGEN.get())):#jon FOR
            self.signature_index = 0
        else:
            self.signature_index +=1

    def calculate_prev_file(self,scaleFOR,scaleGEN):
        if(self.signature_index == 0):
            self.signature_index = 19+scaleGEN.get()
        elif(self.signature_index == 20):
            self.signature_index = scaleFOR.get() - 1
        else:
            self.signature_index -=1

    def calculate_first_file(self):
        self.signature_index = 0

    def calculate_last_file(self,scaleGEN):
        self.signature_index = 19+scaleGEN.get()




class MCYTDataset(IDataset):

    def __init__(self,listbox):
        self.insert_elements_in_users_listbox(listbox)
        self.signature_index = 0

    def calc_signatures_directory(self,listbox):
        self.current_user_dir = os.path.join(st.DIRECTORY_PATH_MCYT, listbox.get(listbox.curselection()))
        self.signatures = os.listdir(self.current_user_dir)
        if listbox.get(listbox.curselection()) == '0000':
            self.signatures.pop(0)

    def insert_elements_in_users_listbox(self,listbox):
        for dir in self.list_of_directorys(st.DIRECTORY_PATH_MCYT) :
            listbox.insert(END, dir)

    def read_csv_file_(self):
        csv_file_path = os.path.join(self.current_user_dir, self.signatures[self.signature_index])
        dataset = pd.read_csv(csv_file_path)
        x = dataset[u'X']
        y = dataset[u' Y']
        x = [int(e) for e in x]
        y = [int(e) for e in y]
        return x, y

    def set_label_text(self,subplot):
        file_num = str(int(self.signatures[self.signature_index][5:7]) + 1)
        if self.signatures[self.signature_index][4:5] == 'f':
            subplot.set_title("Forgery/" + file_num)
        else:
            subplot.set_title("Genuine/" + file_num)

    def calculate_next_file(self,scaleFOR,scaleGEN):
        if((self.signature_index +1) == scaleFOR.get()) : #jon GEN
            self.signature_index = 25
        elif(self.signature_index == (24+scaleGEN.get())):#jon FOR
            self.signature_index = 0
        else:
            self.signature_index +=1

    def calculate_prev_file(self,scaleFOR,scaleGEN):
        if(self.signature_index == 0):
            self.signature_index = 24+scaleGEN.get()
        elif(self.signature_index == 24):
            self.signature_index = scaleFOR.get() - 1
        else:
            self.signature_index -=1

    def calculate_first_file(self):
        self.signature_index = 0

    def calculate_last_file(self,scaleGEN):
        self.signature_index = 24+scaleGEN.get()





def mainn():
    window=ConfigureWindow()
    window.win.mainloop()


if __name__ == "__main__":
    mainn()

# # import tkinter as tk
# #
# # #create window & frames
# # class App:
# #     def __init__(self):
# #         self.root = tk.Tk()
# #         self._job = None
# #         self.slider = tk.Scale(self.root, from_=0, to=256,
# #                                orient="horizontal",
# #                                command=self.updateValue)
# #         self.slider.pack()
# #         self.root.mainloop()
# #
# #     def updateValue(self, event):
# #         if self._job:
# #             self.root.after_cancel(self._job)
# #         self._job = self.root.after(500, self._do_something)
# #
# #     def _do_something(self):
# #         self.job = None
# #         print("new value:", self.slider.get())
# #
# # app=App()