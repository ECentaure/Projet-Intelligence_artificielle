#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 16:29:24 2019

@author: 3701195
"""

# coding: utf-8
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam
from soccersimulator import VolleySimulation, volley_show_simu
from Pain_de_mie import *

class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Echauffement")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        v = adv_position - s.player
        v.normalize()
        dist_players = distance(state, id_team, id_player, adv_position)
        v.norm = dist_players
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = v)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
         
class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        v = adv_position - s.player
        v.normalize()
        dist_players = distance(state, id_team, id_player, adv_position)
        v.norm = dist_players
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = v)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
            
       
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        return SoccerAction(acceleration=Vector2D.create_random(-1, 1),
                            shoot=Vector2D.create_random(-1, 1))

# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("Player 1", Echauffement())  # Random strategy
team2.add("Player 2", Echauffement())   # Random strategy

# Create a match
simu = VolleySimulation(team1, team2)

# Simulate and display the match
volley_show_simu(simu)
