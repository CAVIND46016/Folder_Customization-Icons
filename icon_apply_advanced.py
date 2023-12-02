"""
Contains logic of building GUI for the application.
"""

import os
from tkinter import Tk, ttk, messagebox
from tkinter.filedialog import askdirectory
from icon_apply import set_icon
from icon_online_search import find_and_convert


class CreateGUI:
    """
    Creates the GUI using tkinter module.
    """

    dir_name = None

    def __init__(self, root_obj):
        """
        Initializes the Tk() root object for the class
        and calls the 'construct_dialog' method.
        """

        self.root_obj = root_obj
        self.construct_dialog()

    def bulk_icon_apply(self, directory):
        """
        Walks recursively through the directory and its
        subdirectories and sets icons to each respective folder
        fetched by the 'get_ico_file' method.
        :param directory:
        :return:
        """

        cnt = 0
        root, name = os.path.split(directory)
        main_directory_icon = self.get_ico_file(root, name)
        if main_directory_icon:
            set_icon(directory, main_directory_icon, 0)
            cnt += 1

        for root, dirs, _ in os.walk(directory):
            for name in dirs:
                subdir_icon = self.get_ico_file(root, name)
                if subdir_icon:
                    set_icon(os.path.join(root, name), subdir_icon, 0)
                    cnt += 1

        messagebox.showinfo("Success", f"Icons applied successfully to {cnt} folders.")

    def get_directory(self):
        """
        Validates the entered directory name and calls
        the 'bulk_icon_apply' method.
        :return:
        """

        self.dir_name = askdirectory(title="Choose directory")
        if self.dir_name:
            if os.path.isdir(self.dir_name):
                try:
                    self.bulk_icon_apply(self.dir_name)
                except IOError as err:
                    messagebox.showerror("Error", err)
            else:
                messagebox.showerror("Error", "Invalid directory.")

    @staticmethod
    def get_ico_file(root, name):
        """
        Fetches the icon to be applied to the folder.
        :param root:
        :param name:
        :return:
        """

        ico_file = find_and_convert(root, name)
        return ico_file if os.path.isfile(ico_file) else None

    def construct_dialog(self):
        """
        Constructs the GUI dialog form.
        :return:
        """

        self.root_obj.title("Icon apply - advanced")
        self.root_obj.geometry("{}x{}".format(250, 60))
        label = ttk.Label(self.root_obj, text="Search and apply icons", font=("Arial", 10))
        label.pack()
        button = ttk.Button(self.root_obj, text="Select directory", command=self.get_directory)
        button.pack()


def main():
    root = Tk()
    CreateGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
