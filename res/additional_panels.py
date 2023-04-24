import tkinter as tk
import config
import numpy as np
from count_plot_array import count_wave

class ChRB_panel(tk.Frame):
    def __init__(self, master, var, command):
        self.master = master
        super().__init__(master)

        self.ch_lb = tk.Label(self, text="Настройка умного курсора")
        self.ch_lb.grid(row=0, column=0, columnspan=2)
        self.print_U = tk.Radiobutton(self, text="Первый", value=0, variable=var, command=command)
        self.print_U.grid(row=1, column=0, sticky="W")

        self.print_I = tk.Radiobutton(self, text="Второй", value=1, variable=var, command=command)
        self.print_I.grid(row=1, column=1, sticky="W")


class Intence_panel(tk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(master)

        self.IntenceVar = tk.StringVar()
        self.int_lb = tk.Label(self, text="Полная интенсивность: ")
        self.int_lb.grid(column=0, row=0, sticky="W")
        self.crdX_lb = tk.Label(self, textvariable=self.IntenceVar)  # , background="#777")
        self.crdX_lb.grid(column=1, row=0, sticky="W")