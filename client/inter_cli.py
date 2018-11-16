#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import tkinter as tk

class InterProjeto:
	def __init__(self, master=None):
		self.main_window = tk.Tk()
		self.label1 = tk.Label(self.main_window, text='Hello World')
		self.label2 = tk.Label(self.main_window, text='Mr. Robot - Fuck the world!')

		self.label1.grid()
		self.label2.grid()

		tk.mainloop()

# Cria a instancia
if __name__ == '__main__': InterProjeto()
