#!/usr/bin/python
import Tkinter as tk
import csv
import os
import sys
import tkMessageBox
import ttk
import webbrowser
import logging
import time
import re
from tkFileDialog import *


class SingletonClass(type):
    """Meta class to satisfy singleton implementation."""
    __instance_dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instance_dict:
            cls.__instance_dict[cls] = super(SingletonClass, cls).__call__(*args, **kwargs)
        return cls.__instance_dict[cls]


class LoggingHandler:
    """class for logging variables """
    __metaclass__ = SingletonClass

    def __init__(self):
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler("log.log")
        self.handler.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        self.logger.info(
            "New session started at " + time.asctime() + "\n-------------------------------------------------")
        self.formatter = logging.Formatter("%(asctime)s: %(message)s")
        self.handler.setFormatter(self.formatter)


class AppFrameWork:
    """Class contain Tkinter widgets for the GUI application"""
    __metaclass__ = SingletonClass

    def __init__(self):
        """initialization of Tkinter widgets."""
        # Create the root window
        self.__root = tk.Tk()
        # Set window title
        self.__root.title('name')
        # Set window size
        self.__root.geometry("445x325")
        self.__root.resizable(width=False, height=False)
        self.__font_type = "Times 9"
        self.bg_col = '#666666'
        self.bg_col2 = '#b4b4b4'
        self.pb1 = ttk.Progressbar(self.__root, orient='horizontal', mode='determinate', length=100, value=0)
        self.pb2 = ttk.Progressbar(self.__root, orient='horizontal', mode='determinate', length=100, value=0)
        self.folder_open = tk.IntVar()
        self.cb = tk.Checkbutton(self.__root, text="Open folder after operation", variable=self.folder_open,
                                 font=self.__font_type, bg=self.bg_col2)
        self.lb1 = tk.Label(self.__root, text="File path", font=self.__font_type, bg=self.bg_col2)
        self.bt1 = tk.Button(self.__root, text="Browse Files", command=self.__browse_file_name, font=self.__font_type,
                             bg=self.bg_col2)
        self.lb2 = tk.Label(self.__root, text="Folder path", font=self.__font_type, bg=self.bg_col2)
        self.bt2 = tk.Button(self.__root, text="Browse Files", command=self.__browseFolder, font=self.__font_type,
                             bg=self.bg_col2)
        self.bt3 = tk.Button(self.__root, text="Start", width=10, height=1, font=self.__font_type, bg=self.bg_col2)
        self.__minibar = tk.Menu(self.__root)
        self.__help = tk.Menu(self.__minibar, font=self.__font_type, tearoff=0)
        self.__help.add_command(label="Help", command=self.__Help_message, font=self.__font_type)
        self.__minibar.add_cascade(label="Help", menu=self.__help)
        self.__info = tk.Menu(self.__minibar, font=self.__font_type, tearoff=0)
        self.__info.add_command(label="About", command=self.__Tool_info, font=self.__font_type)
        self.__minibar.add_cascade(label="About", menu=self.__info)
        self.__root.config(menu=self.__minibar)
        self.logo = tk.Label(self.__root, text="Name of Company", font="Times 19 bold", fg="orange", bg=self.bg_col,
                             padx=5)
        self.sup_file_format = ["txt"]
        self.key_path = {}

    @property
    def root(self):
        """allows the private TK root variable to access through object"""
        return self.__root

    def __browse_file_name(self):
        """Function to browse csv file from file manager. It is called from browse button corresponds to file path label """
        self.__cwd = os.getcwd()
        self.__filename = askopenfilename(initialdir="/",
                                          title="Select File",
                                          filetypes=(("files",
                                                      "*.*"),
                                                     ))
        os.chdir(self.__cwd)

        if self.__filename:
            tkMessageBox.showinfo("File path", self.__filename)
            self.key_path['csv_path'] = self.__filename
            self.pb1['value'] = 100

    def __browseFolder(self):
        """Function to browse scripts folder from file manager. It is called from browse button corresponds to  folder path label """
        self.__cwd = os.getcwd()
        self.__filename = askdirectory(initialdir="/",
                                       title="Select folder")
        os.chdir(self.__cwd)

        if self.__filename:
            if not filter(lambda f_name: len(f_name.split(".")) >= 2 and f_name.split(".")[1] in self.sup_file_format,
                          os.listdir(self.__filename)):
                print "Input Error : Not found any  txt,.....  files"
                tkMessageBox.showinfo("Error",
                                      "Not found any  txt,.....  files\n Please Give correct common folder path")
            else:
                tkMessageBox.showinfo("Folder", self.__filename)
                self.key_path['Common'] = self.__filename
                self.pb2['value'] = 100
        else:
            tkMessageBox.showinfo("Error", "Give valid folder path")

    @staticmethod
    def __Help_message():
        """Menu bar help message"""
        tkMessageBox.showinfo("Help",
                              " content")

    @staticmethod
    def __Tool_info():
        """Menu bar tool information"""
        tkMessageBox.showinfo("Tool info",
                              "Name 1.0 \n\n\n created by : Amal Poulose\n contact : amalpoulose1995@gmail.com, 9446047003\n\n"
                              "Objective : _____.")


def Backend_decorator(function):
    """Decorator to main_program function"""

    def Backend_wrapper(*args, **kwargs):
        """check all inputs and avoid multiple clicks on start button as pre check before executing main code.And post strap to reset inputs"""
        app = AppFrameWork()
        if app.key_path["click"] != 0:
            tkMessageBox.showinfo("Error", "Wait till current operation is finished")
            return 0
        if len(app.key_path.items()) <= 2:
            tkMessageBox.showinfo("Error", "Input missing")
            return 0
        app.key_path["click"] += 1
        print app.key_path
        rtn = function(*args, **kwargs)
        app.key_path["click"] = 0
        del app.key_path['Common']
        del app.key_path['csv_path']
        app.pb1['value'] = 0
        app.pb2['value'] = 0
        return rtn

    return Backend_wrapper


@Backend_decorator
def main_program():
    """Backend code to do the  main operation"""
    app = AppFrameWork()
    log = LoggingHandler()
    xl_path = app.key_path['csv_path']
    common_folder = app.key_path['Common']
    log.logger.info("Execution Started.....")

    log.logger.info("Execution Ended.....")
    if app.folder_open.get():
        webbrowser.open(common_folder + "update")


def App_close_event():
    """Event to execute before closing the Tkinter window"""
    log = LoggingHandler()
    app = AppFrameWork()
    log.logger.info("Closing GUI........\n\n")
    app.root.destroy()


def Frame_Work():
    """GUI frame work configuration"""
    app = AppFrameWork()
    log = LoggingHandler()
    app.key_path["click"] = 0
    app.root.configure(background=app.bg_col)
    app.root.protocol("WM_DELETE_WINDOW", App_close_event)
    app.pb1.grid(row=3, column=2)
    app.pb2.grid(row=4, column=2)
    app.cb.grid(row=7, column=0)
    app.lb1.grid(row=3, column=0)
    app.bt1.grid(row=3, column=1)
    tk.Label(app.root, background=app.bg_col).grid(row=0)
    tk.Label(app.root, background=app.bg_col).grid(row=1)
    app.lb2.grid(row=4, column=0)
    app.bt2.grid(row=4, column=1)
    tk.Label(app.root, background=app.bg_col).grid(row=5)
    tk.Label(app.root, background=app.bg_col).grid(row=6)
    tk.Label(app.root, background=app.bg_col).grid(row=8)
    tk.Label(app.root, background=app.bg_col).grid(row=9)
    app.bt3.grid(row=10, column=1)
    tk.Label(app.root, background=app.bg_col).grid(row=11)
    tk.Label(app.root, background=app.bg_col).grid(row=12)
    app.logo.grid(row=13, column=2)
    app.bt3["command"] = main_program
    try:
        app.root.iconbitmap(False, os.getcwd() + "\\icon.ico")
    except tk.TclError as err:
        log.logger.error("icon file missing from exe folder")
        log.logger.error(err)
    app.root.mainloop()


if __name__ == "__main__":
    Frame_Work()
