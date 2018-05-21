#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -

import Lib.model as mdl
import random as rd
import os as os

rd.seed(os.urandom(1024))

CarModel = mdl.IDM(130, 1.8, 78, 2, 2)
Util = mdl.Math()
t=0
dt=0.01
end=40

def simulation(t,dt,end):
    CarArr=[mdl.Vehicle(10, 20, 10, 0, 130, "car"), mdl.Vehicle(10, 20, 20, 0, 130, "car")]
    while t<end:
        t+=dt
        if rd.random() < 1/20:
            CarArr=[mdl.Vehicle(10, 20, 0, 0, 130, "car")] + CarArr
        for i in range(len(CarArr)-1):
            CarArr[i].acc = CarModel.acceleration(CarArr[i+1].u-CarArr[i].u, CarArr[i].speed, CarArr[i+1].speed, CarArr[i+1].acc)
            CarArr[i].speed = CarArr[i].speed + CarArr[i].acc * dt
            CarArr[i].u = CarArr[i].u + CarArr[i].speed * dt + 1/2 * CarArr[i].acc * (dt**2)
        # Handle last car separately
        CarArr[len(CarArr)-1].acc = CarModel.acceleration(10**10, CarArr[i].speed, 10**10, 10**10)
        CarArr[len(CarArr)-1].speed = CarArr[i].speed + CarArr[i].acc * dt
        CarArr[len(CarArr)-1].u = CarArr[i].u + CarArr[i].speed * dt + 1/2 * CarArr[i].acc * (dt**2)
    for car in CarArr:
        print (car.speed)

simulation(t, dt, end)
