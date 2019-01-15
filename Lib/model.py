#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -/Lib/model.py

# Imports
import numpy as np
import random as rd
import os as os

rd.seed(os.urandom(1024))


# Modélisation générale
# Classes utilsées directement dans le calcul et la modélisation du projet

# Miscelaneous functions
# Mainly used for debugging and/or coding
class Misc:
    def rK1(self, a, fa, hs):
        a1 = fa(a) * hs
        ak = a + a1 * 0.5
        a2 = fa(ak) * hs
        ak = a + a2 * 0.5
        a3 = fa(ak) * hs
        ak = a + a3
        a4 = fa(ak) * hs
        a = a + (a1 + 2 * (a2 + a3) + a4) / 6
        return a

    # Used as a base for the graphical sim
    # Runs a simulation for (end - t) seconds.
    # @param t:   Start                                       [s]
    # @param dt:  Simulation interval (the lesser the better) [s]
    # @param end: End of the simulation                       [s]
    # @param mdl: IDM model object to use
    # @param CarModel: CarModel object to use

    def finishedSim(self, t, dt, end, mdl, CarModel):
        CarArr = [mdl.Vehicle(1, 1, 100, 0, 130 / 3.6, "car"), mdl.Vehicle(1, 1, 200, 0, 130 / 3.6, "car")]
        while t < end:
            t += dt
            if rd.random() < 1 / 20:
                CarArr = [mdl.Vehicle(1, 1, 0, 0, 130 / 3.6, "car")] + CarArr
            # Last car is handled separately
            CarArr[len(CarArr) - 1].acc = CarModel.acceleration(10 ** 10, CarArr[len(CarArr) - 1].speed, 10 ** 10,
                                                                10 ** 10)
            CarArr[len(CarArr) - 1].speed = CarArr[len(CarArr) - 1].speed + CarArr[len(CarArr) - 1].acc * dt
            CarArr[len(CarArr) - 1].u = CarArr[len(CarArr) - 1].u + CarArr[len(CarArr) - 1].speed * dt + 1 / 2 * CarArr[
                len(CarArr) - 1].acc * (dt ** 2)
            for i in reversed(range(len(CarArr) - 1)):
                CarArr[i].acc = CarModel.acceleration(CarArr[i + 1].u - CarArr[i].u, CarArr[i].speed,
                                                      CarArr[i + 1].speed, CarArr[i + 1].acc)
                CarArr[i].speed = CarArr[i].speed + CarArr[i].acc * dt
                CarArr[i].u = CarArr[i].u + CarArr[i].speed * dt + 1 / 2 * CarArr[i].acc * (dt ** 2)
        # Very slow
        for car in CarArr:
            print("Position", car.u, "Vitesse", car.speed * 3.6, "km/h")


# Intelligent Driver Model
#
# @param v0:   desired speed            [m/s]
# @param T:    time headway             [s]  -> ~1.8s is a great value
# @param s0:   minimum gap              [m] -> 78 meters in France for 130km/h (A calculer automatiquement?)
# @param a:    maximum acceleration     [m/s²]
# @param b:    confortable deceleration [m/s²]

class IDM:
    def __init__(self, v0, T, s0, a, b):
        self.v0 = v0
        self.T = T
        self.s0 = s0
        self.a = a
        self.b = b

        # Consts
        self.alpha_v0 = 1
        self.speedlimit = 1000
        self.speedmax = 1000
        self.bmax = 18

    # Acceleration function
    # @param s:     actual gap           [m]
    # @param v:     actual speed         [m/s]
    # @param vl:    leading speed        [m/s]
    # @param al:    leading acceleration [m/s²] (optional)

    def acceleration(self, s, v, vl, al):
        if s < 0.0001:
            return -self.bmax

        noiseAcc = 0.3
        accRnd = noiseAcc * (rd.random() - 0.5)

        v0eff = min(self.v0, self.speedlimit, self.speedmax)
        v0eff *= self.alpha_v0

        if v < v0eff:
            accFree = self.a * (1 - np.power(v / v0eff, 4))
        else:
            accFree = self.a * (1 - v / v0eff)

        sstar = self.s0 + max(0, v * self.T + 0.5 * v * (v - vl) / np.sqrt(self.a * self.b))
        accInt = -self.a * np.power(sstar / max(s, self.s0), 2)

        if v0eff < 0.00001:
            return 0
        else:
            return max(-self.bmax, accFree + accInt + accRnd)


# Modélisation d'un véhicule selon différents paramètres

# Vehicle class
# @param length: vehicle's length          [m]
# @param width:  vehicle's width           [m]
# @param u:      vehicle's long coordinate [m]
# @param lane:   lane where the vehicle is [int]
# @param speed:  actual speed              [m/s]
# @param type:   car|truck                 [string]

class Vehicle:
    def __init__(self, length, width, u, lane, speed, Type):
        # La majorité de ces paramètres sont ici dans l'optique d'un passage à un modèle avec changement de voie
        self.length = length
        self.width = width
        self.u = u
        self.lane = lane
        self.v = lane
        self.dvdt = 0
        self.laneOld = lane
        self.speed = speed
        self.Type = Type
        self.Id = np.floor(100000 * rd.random() + 200)
        self.rpz = 0

        self.route = []
        self.divergeAhead = False
        self.toRight = False

        self.dt_lastLC = 10
        self.dt_lastPassiveLC = 10
        self.acc = 0
        self.iLead = -100
        self.iLag = -100

        self.iLeadRight = -100
        self.iLeadLeft = -100
        self.iLagRight = -100
        self.iLagLeft = -100

    def setRoute(self, route):
        self.route = route

    def isPerturbed(self):
        return self.Id >= 10 and self.Id < 200

    def isRegularVeh(self):
        # L'introduction du type "obstacle" permet de prévoir une évolution avec l'introduction d'obstacles sur la route
        return (self.isPerturbed() or self.Id >= 200)  # and (self.type !== "obstacle")
