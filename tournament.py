#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:21:19 2019

@author: emeline
"""
from sanstitre0 import *
from Pain_de_mie import *
from soccersimulator import SoccerTeam


    
if __name__ == "__main__":
	from soccersimulator import Simulation, show_simu
	team1 = get_team(1)
	team2 = get_team(2)
	simu = Simulation(team1,team2)
	show_simu(simu)
