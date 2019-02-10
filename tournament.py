#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 16:21:19 2019

@author: emeline
"""
from sanstitre0 import *

from soccersimulator import SoccerTeam

def get_team(nb_players ):
    team = SoccerTeam ( name = "equipe 3701195" )
    if nb_players == 1:
        team.add(" Striker " , Attaquant_v2())
    if nb_players == 2:
        team.add(" Gardien " , Gardien_v2())
        team.add(" Attaquant " ,Attaquant_v2())
        return team
    
if __name__ == "__main__":
    from soccersimulator import Simulation , show_simu
    # Check teams with 1 player and 2 players
    team1 = get_team(1)
    team2 = get_team(2)
    # Create a match
    simu = Simulation(team1 , team2 )
