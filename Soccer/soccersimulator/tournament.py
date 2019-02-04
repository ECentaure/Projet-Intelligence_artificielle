#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:21:19 2019

@author: emeline
"""

from main import *
from soccersimulator import SoccerTeam

def get_team(nb_players ):
    team = SoccerTeam ( name = "equipe 3701195" )
    if nb_players == 1:
        team . add ( " Striker " , FonceurStrategy(Strategy))
    if nb_players == 2:
        team.add (" Fonceur " , FonceurStrategy(Strategy))
        team.add (" Random " ,RandomStrategy(Strategy))
        return team