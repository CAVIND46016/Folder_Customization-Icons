from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from IconApply import seticon
import os

class CreateGUI():
    dir_name = None
    
    def __init__(self, root_obj):
        self.root_obj = root_obj;
        self.construct_dialog()
        
    def set_icon(self, directory):
        subdirs = []
        for filename in os.listdir(directory):
            a = os.path.join(directory, filename)
            if(os.path.isdir(a)):
                subdirs.append(a)
                
        for i in subdirs:
            for filename in os.listdir(i):     
                icofile = None;
                for ico_file in os.listdir(i):
                    if(ico_file.endswith(".ico")):
                        icofile = i + "\\" + ico_file
                        break;
                    
                if(icofile != None):   
                    seticon(i + "\\", icofile, 0)
        
        messagebox.showinfo("Success","Icons applied successfully.")
        
    def get_directory(self):
        self.dir_name = askdirectory(title = "Choose directory" )
        if(self.dir_name):
            if(os.path.isdir(self.dir_name)):
                try:
                    self.set_icon(self.dir_name)
                except IOError as e:
                    messagebox.showerror("Error", e)
            else:
                messagebox.showerror("Error", "Invalid directory.")
        
    def construct_dialog(self):
        self.root_obj.title("Batch Folder Icon Changer")
        self.root_obj.geometry('{}x{}'.format(150, 50))
        self.root_obj.resizable(width=False, height=False)
        label = ttk.Label(self.root_obj, text ="Batch Icon Changer",font=("Arial", 10))
        label.pack()
        
        button = ttk.Button(self.root_obj, text = 'Select directory', command = self.get_directory);
        button.pack()
        
        self.root_obj.mainloop()


def main():
    root = Tk()
    CreateGUI(root);
    
if(__name__ == "__main__"):
    main();
