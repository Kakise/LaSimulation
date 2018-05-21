#!/usr/bin/env python
#-*- coding: utf-8 -*-

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

# Intelligent Driver Model
#
# @param v0: desired speed
# @param T: time headway -> ~1.8s is a great value
# @param s0: minimum gap -> 78 meters in France
# @param a: maximum acceleration
# @param b: confortable deceleration

# Fourth order Runge-Kutta method
class Math:
    def rK1(self, a, fa, hs):
        a1 = fa(a)*hs
        ak = a + a1*0.5
        a2 = fa(ak)*hs
        ak = a + a2*0.5
        a3 = fa(ak)*hs
        ak = a + a3
        a4 = fa(ak)*hs
        a = a + (a1 + 2*(a2 + a3) + a4)/6
        return a

class IDM:
    def __init__(self, v0, T, s0, a, b):
        self.v0 = v0
        self.T = T
        self.s0 = s0
        self.a = a
        self.b = b
        
        # Consts
        self.alpha_v0=1
        self.speedlimit=1000
        self.speedmax=1000
        self.bmax=18

    # Acceleration function
    # @param s:     actual gap [m]
    # @param v:     actual speed [m/s]
    # @param vl:    leading speed [m/s]
    # @param al:    leading acceleration [m/s^2] (optional al=0 if 3 args)

    def acceleration(self, s, v, vl, al):
        if s<0.0001:
            return -self.bmax
        
        noiseAcc = 0.3
        accRnd = noiseAcc*(rd.random()-0.5)

        v0eff = min(self.v0, self.speedlimit, self.speedmax)
        v0eff *= self.alpha_v0

        if v < v0eff:
            accFree = self.a*(1-np.power(v/v0eff,4))
        else:
            accFree = self.a*(1-v/v0eff)

        sstar = self.s0 + max(0, v*self.T+0.5*v*(v-vl)/np.sqrt(self.a*self.b))
        accInt = -self.a*np.power(sstar/max(s,self.s0),2)

        if v0eff<0.00001:
            return 0
        else:
            return max(-self.bmax, accFree + accInt + accRnd)

# Modélisation d'un véhicule selon différents paramètres

# Vehicle class
# @param length: vehicle's length
# @param width: vehicle's width
# @param u: vehicle's long coordinate
# @param lane: lane where the vehicle is
# @param speed: actual speed
# @param type: Car|Truck

class Vehicle:
    def __init__(self, length, width, u, lane, speed, type):
        self.length=length
        self.width=width
        self.u=u
        self.lane=lane
        self.v=lane
        self.dvdt=0
        self.laneOld=lane
        self.speed=speed
        self.type=type
        self.id=np.floor(100000*rd.random()+200)

        self.route=[]
        self.divergeAhead=False 
        self.toRight=False 

        self.dt_lastLC=10
        self.dt_lastPassiveLC=10
        self.acc=0
        self.iLead=-100
        self.iLag=-100

        self.iLeadRight=-100
        self.iLeadLeft=-100
        self.iLagRight=-100
        self.iLagLeft=-100
    
    def setRoute(self, route):
        self.route = route
    
    def isPerturbed(self):
        return self.id>=10 and self.id<200
    
    def isRegularVeh(self):
        # L'introduction du type "obstacle" permet de prévoir une évolution avec l'introduction d'obstacles sur la route
        return (self.isPerturbed() or self.id >= 200) # and (self.type !== "obstacle")