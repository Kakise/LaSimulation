#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -

import Lib.model as mdl
import Lib.gui as gui
import random as rd
import os as os
import numpy as np

rd.seed(os.urandom(1024))

# Initialisation of the model
CarModel = mdl.IDM(130/3.6, 1.8, 78, 0.3, 2) # Uses french standard values
Util = mdl.Misc()
Window = gui.Canvas(mdl, CarModel, 0.2)

# TODO: Move everything to a python lib