# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Project: -

import numpy as np
import random as rd
import curses
import Lib.car
import Lib.misc as misc
import Lib.gui as gui

stdscr = curses.initscr()

# Definition des paramètres principaux.

Vehicles = [] # Liste des véhicules existants
Types = ["Car", "Truck"] # Types de véhicules existants
StartX, StartY = (0, 0) # Position de départ
NVeh = 1200 # Nombre de véhicules
Speed_m, Speed_M = (110, 130) # Vitesse minimale et vitesse maximale (resp.)

gui.main(stdscr)
misc.cls()
