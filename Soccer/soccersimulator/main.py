#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 18:00:28 2019

@author: 3701195
"""
# coding: utf-8
from tools import *
from actions import *
from superstate import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
import math

def passe(state):
    allies = [ self . state . player_state ( id_team , id_player ). position
                 for ( id_team , id_player ) in self . state . players
                 if id_team != self . id_team ]
    allieProche = min([(self.player.distance(player),player) for player in allies])

class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        return SoccerAction(Vector2D.create_random(), Vector2D.create_random())

class FonceurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Fonceur")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        
       
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goalAdv - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
        
class GardienStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Gardien")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        if(dist < 50 and distance(state, id_team, id_player, s.goal) < 10):
            if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
                return SoccerAction(shoot = s.goalAdv - s.player)
            else:
                return SoccerAction(acceleration = s.ball - s.player)
        else:
             return SoccerAction(acceleration = s.goal - s.player)
class DefenseurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defenseur")
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goal - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
        
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("kiwi", RandomStrategy())  # Random strategy
team1.add("bobby", GardienStrategy()) 

#team2.add("Fonceur", FonceurStrategy())   # Static strategy
team1.add("gregory", FonceurStrategy()) 
team2.add("nemo", FonceurStrategy()) 
team2.add("nemo", FonceurStrategy()) 
team2.add("mon enfant", GardienStrategy()) 

# Create a match
simu = Simulation(team1, team2)
# Simulate and display the match
show_simu(simu)
