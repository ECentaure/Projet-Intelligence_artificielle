#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 18:00:28 2019

@author: 3701195
"""

# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
import math

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(),
                            Vector2D.create_random())

class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        dist = math.sqrt(math.pow((state.ball.position.x - state.player_state(id_team, id_player).position.x),2) + 
                         math.pow((state.ball.position.y - state.player_state(id_team, id_player).position.y),2))
    
        VectPos = state.ball.position - state.player_state(id_team, id_player).position
        
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS):
            vitesse = Vector2D (1 ,1)
            shoot = Vector2D (1 ,1)
            act1 = SoccerAction ( vitesse , shoot )
            act2 = SoccerAction (2* vitesse ,2* shoot )
            act_new = SoccerAction ( act1 . acceleration + act2 . acceleration ,act1 . shoot + act2 . shoot )
            return act_new
        else:
            return SoccerAction(VectPos, Vector2D())


# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Random", RandomStrategy())  # Random strategy
team2.add("Fonceur", FonceurStrategy())   # Static strategy

# Create a match
simu = Simulation(team1, team2)

# Simulate and display the match
show_simu(simu)