#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -/Lib/gui.py

import tkinter as tk
import numpy as np
import random as rd
import os as os
import time

rd.seed(os.urandom(1024))


# This Class is defining every single function related to the graphical feedback.
class Canvas:
    # This function takes no arguments and is only used to initialize the canvas.
    def __init__(self, mdl, CarModel, dt):
        self.mdl = mdl
        self.CarModel = CarModel
        self.dt = dt

        self.fen = tk.Tk()
        self.can = tk.Canvas(self.fen, bg='darkgreen', height=600, width=800)
        self.can.pack()  # ajuste la fenêtre

        self.can.create_rectangle(0, 250, 1439, 500, fill='grey')  # route grise

        self.can.create_line(0, 325, 100, 325, fill='white')  # délimitation voie 1, voie 2
        self.can.create_line(140, 325, 240, 325, fill='white')
        self.can.create_line(280, 325, 380, 325, fill='white')
        self.can.create_line(420, 325, 520, 325, fill='white')
        self.can.create_line(560, 325, 660, 325, fill='white')
        self.can.create_line(700, 325, 800, 325, fill='white')
        self.can.create_line(840, 325, 940, 325, fill='white')
        self.can.create_line(980, 325, 1080, 325, fill='white')
        self.can.create_line(1120, 325, 1220, 325, fill='white')
        self.can.create_line(1260, 325, 1360, 325, fill='white')
        self.can.create_line(1400, 325, 1500, 325, fill='white')

        self.can.create_line(0, 415, 110, 415, fill='white')  # délimitation voie 2, voie 3
        self.can.create_line(140, 415, 240, 415, fill='white')
        self.can.create_line(280, 415, 380, 415, fill='white')
        self.can.create_line(420, 415, 520, 415, fill='white')
        self.can.create_line(560, 415, 660, 415, fill='white')
        self.can.create_line(700, 415, 800, 415, fill='white')
        self.can.create_line(840, 415, 940, 415, fill='white')
        self.can.create_line(980, 415, 1080, 415, fill='white')
        self.can.create_line(1120, 415, 1220, 415, fill='white')
        self.can.create_line(1260, 415, 1360, 415, fill='white')
        self.can.create_line(1400, 415, 1500, 415, fill='white')

        # Define a list to store the cars
        self.CarArr = [self.mdl.Vehicle(20, 15, 100, 0, 130 / 3.6, "car"),
                       self.mdl.Vehicle(20, 15, 200, 0, 130 / 3.6, "car")]
        self.CarArr[0].rpz = self.can.create_rectangle(self.CarArr[0].u, 375, self.CarArr[0].u + self.CarArr[0].length,
                                                       375 + self.CarArr[0].width, fill='red')
        self.CarArr[1].rpz = self.can.create_rectangle(self.CarArr[1].u, 375, self.CarArr[1].u + self.CarArr[1].length,
                                                       375 + self.CarArr[1].width, fill='red')

        # self.can.create_text(450, 475, text="mon texte ici", font="Arial 12")
        self.fen.after(10, self.update())
        self.fen.mainloop()

    def update(self):
        # Adds a vehicle
        if rd.random() < 1 / 20:
            self.CarArr = [self.mdl.Vehicle(20, 15, 0, 0, 130 / 3.6, "car")] + self.CarArr
            self.CarArr[0].rpz = self.can.create_rectangle(self.CarArr[0].u, 375,
                                                           self.CarArr[0].u + self.CarArr[0].length,
                                                           375 + self.CarArr[0].width, fill='red')
        # Handles the last car seperately to avoid any problem
        if len(self.CarArr) != 0:
            self.CarArr[len(self.CarArr) - 1].acc = self.CarModel.acceleration(10 ** 10,
                                                                               self.CarArr[len(self.CarArr) - 1].speed,
                                                                               10 ** 10, 10 ** 10)
            self.CarArr[len(self.CarArr) - 1].speed = self.CarArr[len(self.CarArr) - 1].speed + self.CarArr[
                len(self.CarArr) - 1].acc * self.dt
            self.CarArr[len(self.CarArr) - 1].u = self.CarArr[len(self.CarArr) - 1].u + self.CarArr[
                len(self.CarArr) - 1].speed * self.dt + 1 / 2 * self.CarArr[len(self.CarArr) - 1].acc * (self.dt ** 2)
        # Updates the position of each vehicles
        for i in reversed(range(len(self.CarArr) - 1)):
            self.CarArr[i].acc = self.CarModel.acceleration(self.CarArr[i + 1].u - self.CarArr[i].u,
                                                            self.CarArr[i].speed, self.CarArr[i + 1].speed,
                                                            self.CarArr[i + 1].acc)
            self.CarArr[i].speed = self.CarArr[i].speed + self.CarArr[i].acc * self.dt /1000
            self.CarArr[i].u = self.CarArr[i].u + self.CarArr[i].speed * self.dt + 1 / 2 * self.CarArr[i].acc * (
                (self.dt / 1000) ** 2)
        # Updates the graphical output
        for car in self.CarArr:
            print(self.can.coords(car.rpz))
            self.can.move(car.rpz, car.u - self.can.coords(car.rpz)[2], 0)
            if car.u >= 1600:
                self.CarArr.remove(car)
        # Loop
        self.fen.after(10, self.update)
