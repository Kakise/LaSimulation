# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Project: -/Lib/car.py -> This file is used to define classes related to the cars themselves

class Vehicle:
    # Class définissant tout les types de véhicules
    # Liste de paramètres : 
    #  - "Velocity" (int): Paramètre représentant la vitesse -> Expected to receive an int between 110 and 130
    #  - "Type" (str): Paramètre représentant le type du véhicule (implementés: "Car" et "Truck")
    #    -> Le type du véhicule va gérer des choses standards telles que la taille du véhicule()
    Velocity = 0
    Type = ""
    def __init__(self, vel, type):
        self.Type = type if type else "Car"
        self.Velocity = (vel - 45) if self.Type == "Truck" else vel 