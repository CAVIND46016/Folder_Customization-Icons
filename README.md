# Folder customization (Advanced)
The Python script takes a directory name as input. It then searches for suitable images (size = 256x256) related to the folder name on https://images.google.com/. The script downloads 'n' images (where n is a parameter, n <= 100), selects one randomly, and converts it into an .ico file.

The value of 'n' is customizable, but it's important to note that a higher 'n' will increase the execution time, and the icons may or may not be appropriate for the folder, similar to the manual image search on Google.

The chosen image is converted to the .ico format and saved in the relevant subdirectory. Subsequently, it is applied as the folder's icon.

### Before:
![alt text](https://github.com/CAVIND46016/Folder_Customization-Icons/blob/master/data/friends_before.png)
### After:
![alt text](https://github.com/CAVIND46016/Folder_Customization-Icons/blob/master/data/friends_after.png)

# Folder customization (Basic)
In this process, the icons must be manually created and saved in their respective directory or subdirectory. The Python script is responsible for applying these pre-created icons to the corresponding folders.

### Before:
![alt text](https://github.com/CAVIND46016/Bulk-Icon-Apply/blob/master/data/before.png)
### After:
![alt text](https://github.com/CAVIND46016/Bulk-Icon-Apply/blob/master/data/after.png)

You can easily create a Windows Application (.exe) file by following the steps outlined on the website: https://mborgerson.com/creating-an-executable-from-a-python-script/.

To generate the executable, you can use the following commands:

```bash
pyinstaller.exe --onefile --windowed app.py
pyinstaller.exe --onefile --windowed --icon=app.ico app.py
```

Explanation of options:

- _--onefile_: Packages everything into a single executable. Without this option, libraries, etc., will be distributed as separate files alongside the main executable.
- _--windowed_: Prevents a console window from being displayed when the application is run. Useful for graphical applications; for non-graphical (console) applications, this option is not necessary.
- _app.py_: The main source file of the application. The basename of this script will be used to name the executable. You can specify an alternative name using the --name option.

##### For more details, you can refer to the [LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:6372596933311156224).
