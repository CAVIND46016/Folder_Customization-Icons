import os
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askdirectory
from icon_apply import set_icon


class CreateGUI:
    dir_name = None

    def __init__(self, root_obj):
        self.root_obj = root_obj
        self.construct_dialog()

    @staticmethod
    def bulk_icon_apply(directory):
        main_directory_icon = CreateGUI.get_ico_file(directory)
        if main_directory_icon:
            set_icon(directory, main_directory_icon, 0)

        for root, dirs, files in os.walk(directory):
            for name in dirs:
                subdir = os.path.join(root, name)
                subdir_icon = CreateGUI.get_ico_file(subdir)
                if subdir_icon:
                    set_icon(subdir, subdir_icon, 0)

        messagebox.showinfo("Success", "Icons applied successfully.")

    def get_directory(self):
        self.dir_name = askdirectory(title="Choose directory")
        if self.dir_name:
            if os.path.isdir(self.dir_name):
                try:
                    CreateGUI.bulk_icon_apply(self.dir_name)
                except IOError as e:
                    messagebox.showerror("Error", e)
            else:
                messagebox.showerror("Error", "Invalid directory.")

    @staticmethod
    def get_ico_file(directory):
        for f in os.listdir(directory):
            f_path = os.path.join(directory, f)
            if os.path.isfile(f_path) and f.endswith(".ico"):
                return f_path

        return None

    def construct_dialog(self):
        self.root_obj.title("Batch Icon Changer")
        self.root_obj.geometry("{}x{}".format(175, 60))

        label = ttk.Label(
            self.root_obj,
            text="Batch Icon Changer",
            font=("Arial", 10)
        )
        label.pack()

        button = ttk.Button(
            self.root_obj,
            text="Select directory",
            command=self.get_directory
        )
        button.pack()


def main():
    root = Tk()
    CreateGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
