# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Project: -

import numpy as np
import random as rd
from Lib.car import *
from Lib.misc import *

# Definition des paramètres principaux.

Vehicles = [] # Liste des véhicules existants
Types = ["Car", "Truck"] # Types de véhicules existants
StartX, StartY = (0, 0) # Position de départ
NVeh = 1200 # Nombre de véhicules
Speed_m, Speed_M = (110, 130) # Vitesse minimale et vitesse maximale (resp.)

# Instanciation des véhicules:

for i in range(NVeh):
    vel = rd.randint(Speed_m, Speed_M)
    type = Types[rd.randint(0,1)]
    Vehicles.append(Vehicle(vel, type))

while(1):
    cls()
    print("----------------------------------------")
    print("|                                       ")
    print("|                                       ")
    print("|                                       ")
    print("|                                       ")
    print("|                                       ")
    print("|                                       ")
    print("|                                       ")
    print("----------------------------------------")