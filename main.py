#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -

import Lib.model as mdl

CarModel = mdl.IDM(130, 1.8, 78, 2, 2)

# Fill an array with n cars:
def CarFiller(n):
    CarArr = []
    for i in range(n):
        CarArr += [mdl.Vehicle(10,20,0,0,130,"Car")]
    return CarArr

