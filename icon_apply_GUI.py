from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from IconApply import seticon
from os.path import isfile, join
import os

class CreateGUI():
    dir_name = None
    
    def __init__(self, root_obj):
        self.root_obj = root_obj;
        self.construct_dialog()
        
    def bulk_icon_apply(self, directory):
        main_directory_icon = self.get_ico_file(directory);
        if(main_directory_icon):
            seticon(directory, main_directory_icon, 0)
        
        for root, dirs, files in os.walk(directory):
            for name in dirs:
                subdir = os.path.join(root, name)
                subdir_icon = self.get_ico_file(subdir);
                if(subdir_icon):
                    seticon(subdir, subdir_icon, 0)

        messagebox.showinfo("Success","Icons applied successfully.")
        
    def get_directory(self):
        self.dir_name = askdirectory(title = "Choose directory" )
        if(self.dir_name):
            if(os.path.isdir(self.dir_name)):
                try:
                    self.bulk_icon_apply(self.dir_name)
                except IOError as e:
                    messagebox.showerror("Error", e)
            else:
                messagebox.showerror("Error", "Invalid directory.")
                
    def get_ico_file(self, directory):
        for f in os.listdir(directory):
            f_path = join(directory, f)
            if(isfile(f_path) and f.endswith(".ico")):
                return f_path
            
        return None;
        
    def construct_dialog(self):
        self.root_obj.title("Batch Icon Changer")
        self.root_obj.geometry('{}x{}'.format(175, 60))
        
        label = ttk.Label(self.root_obj, text ="Batch Icon Changer", font=("Arial", 10))
        label.pack()
        
        button = ttk.Button(self.root_obj, text = 'Select directory', command = self.get_directory);
        button.pack()


def main():
    root = Tk()
    CreateGUI(root);
    root.mainloop()
    
if(__name__ == "__main__"):
    main();
