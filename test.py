#!/usr/bin/env python
# -*- coding: Latin-1 -*-
#
#  Programme Tkinter.py
#  Démonstration du language

from tkinter import *  #Pour python3.x Tkinter devient tkinter
 
class ApplicationBasic():
	'''Application principale'''
	def __init__(self):
		'''constructeur'''
		self.fen = Tk()
		self.fen.title('Tkinter')
 
		self.bou_action = Button(self.fen)
		self.bou_action.config(text='Action', command=self.action)
		self.bou_action.pack()
 
		self.bou_quitter = Button(self.fen)
		self.bou_quitter.config(text='Quitter', command=self.fen.destroy)
		self.bou_quitter.pack()
 
	def run(self):
                self.fen.mainloop()
 
	def action(self):
		'''Action sur un bouton'''
		self.lab = Label(self.fen)
		self.lab.config(text='Bravo!!!')
		self.lab.pack()
 
 
if __name__ == '__main__':
    app = ApplicationBasic()
    app.run()