#!/usr/bin/env python

# -*- coding: utf-8 -*-

from tkinter import *


# ----------------------------------------------------------------

# Fonctions

# ----------------------------------------------------------------

def modification():

    if (monCanvas.itemcget(pacman_1, 'state')== HIDDEN) :

        monCanvas.itemconfig(pacman_1, state=NORMAL)

        monCanvas.itemconfig(pacman_2, state=HIDDEN)

    else:

        monCanvas.itemconfig(pacman_2, state=NORMAL)

        monCanvas.itemconfig(pacman_1, state=HIDDEN)

    fen_princ.after(300,modification)


def temporisation():

    fen_princ.after(500,modification)


# ----------------------------------------------------------------

# Corps du programme

# ----------------------------------------------------------------


fen_princ = Tk()

fen_princ.title("ESSAI AVEC CANVAS")

fen_princ.geometry("600x600")


monCanvas = Canvas(fen_princ, width=500, height=600, bg='ivory', bd=0, highlightthickness=0)

monCanvas.grid(row=0,column=0, padx=10,pady=10)

pacman_1 = monCanvas.create_arc(50,50,150,150,fill="yellow",start=15,extent=330, state=NORMAL)

pacman_2 = monCanvas.create_arc(50,50,150,150,fill="yellow",start=30,extent=300, state=HIDDEN)


zone2 = Frame(fen_princ, bg='#777777')

zone2.grid(row=0,column=1,ipadx=5)

Button(zone2, text="Couleurs", fg="yellow", bg="black", command=modification).pack(fill=X)

Button(zone2, text="Tempo", fg="yellow", bg="black", command=temporisation).pack(fill=X)


fen_princ.mainloop()