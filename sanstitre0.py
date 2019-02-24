#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 18:00:28 2019
@author: 3701195
"""
# coding: utf-8
#from actions import *
#from superstate import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation,show_simu, settings
from Pain_de_mie import *
import math


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
        dist = s.distance(s.ball)
             
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goalAdv - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
        
class GardienStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Gardien")

    def compute_strategy(self, state, id_team, id_player):
        
        s = SuperState(state, id_team, id_player)
        dist = s.distance(s.ball)
        
        if(dist < 10):
            if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
                return SoccerAction(shoot = s.goalAdv - s.player)
                #return SoccerAction(shoot = allieProche(state, id_team, id_player))
            else:
                return SoccerAction(acceleration = s.ball - s.player)
        else:
             return SoccerAction(acceleration = s.goal - s.player)
         
class DefenseurStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Defenseur")
        
    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(s.ball)
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goal - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
            
            
     
class Attaquant_v2(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Attaquantv_2")
        
    def compute_strategy(self,state,id_team,id_player):
        fct = SuperState(state,id_team,id_player)
        ball = state.ball.position
        if (fct.tirer_ou_pas()):
            return fct.aller_courrir_marcher(ball + 5*state.ball.vitesse)+fct.shoot_but(fct.goalAdv)
        else:
            return fct.aller_courrir_marcher(ball + 5*state.ball.vitesse)
 
class Gardien_v2(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Attaquantv_2")
        
    def compute_strategy(self,state,id_team,id_player):
        fct = SuperState(state,id_team,id_player)
        ball = state.ball.position 
        if (fct.tirer_ou_pas()):
            return fct.aller_gardien(ball + 5*state.ball.vitesse)+fct.shoot(fct.ally_position()+fct.ally_vitesse())    
        else:
            if fct.je_suis_dans_mon_camp():
                if (ball.distance(fct.player)<10):
                    return fct.aller_courrir_marcher(ball)
                else:
                    return fct.aller_gardien(ball + 5*state.ball.vitesse)   
            else:
                return fct.aller_gardien(ball + 5*state.ball.vitesse)+fct.shoot(fct.ally_position()+fct.ally_vitesse())   


        
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players # Random strategy
team1.add("bobby", GardienStrategy()) 
  # Static strategy
#team2.add("nemo", FonceurStrategy()) 

team2.add("jimmy", Attaquant_v2()) 

# Create a match
simu = Simulation(team1, team2)
# Simulate and display the match
#show_simu(simu)
