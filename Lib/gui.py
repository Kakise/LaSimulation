#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -/Lib/gui.py

import tkinter as tk

# This Class is defining every single function related to the graphical feedback.
class Canvas:
    # This function takes no arguments and is only used to initialize the canvas.
    def __init__(self, mdl, CarModel):
        fen = tk.Tk()
        can = tk.Canvas(fen,bg='darkgreen',height=899,width=1439)
        can.pack() #ajuste la fenêtre
        
        can.create_rectangle(0,250,1439,500, fill='grey') #route grise
        
        can.create_line(0,325,100,325,fill='white') #délimitation voie 1, voie 2
        can.create_line(140,325,240,325,fill='white')
        can.create_line(280,325,380,325,fill='white')
        can.create_line(420,325,520,325,fill='white')
        can.create_line(560,325,660,325,fill='white')
        can.create_line(700,325,800,325,fill='white')
        can.create_line(840,325,940,325,fill='white')
        can.create_line(980,325,1080,325,fill='white')
        can.create_line(1120,325,1220,325,fill='white')
        can.create_line(1260,325,1360,325,fill='white')
        can.create_line(1400,325,1500,325,fill='white')
        
        can.create_line(0,415,110,415,fill='white') #délimitation voie 2, voie 3
        can.create_line(140,415,240,415,fill='white')
        can.create_line(280,415,380,415,fill='white')
        can.create_line(420,415,520,415,fill='white')
        can.create_line(560,415,660,415,fill='white')
        can.create_line(700,415,800,415,fill='white')
        can.create_line(840,415,940,415,fill='white')
        can.create_line(980,415,1080,415,fill='white')
        can.create_line(1120,415,1220,415,fill='white')
        can.create_line(1260,415,1360,415,fill='white')
        can.create_line(1400,415,1500,415,fill='white')
        
        #can.create_text(450, 475, text="mon texte ici", font="Arial 12")
        fen.after(0.01, self.update)
        fen.mainloop()
        
    def update(self):
        