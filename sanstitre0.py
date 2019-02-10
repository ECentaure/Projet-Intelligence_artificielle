#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 18:00:28 2019
@author: 3701195
"""
# coding: utf-8
#from actions import *
#from superstate import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
from Boite_a_outils import *
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
        dist = distance(state, id_team, id_player, s.ball)
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goal - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
     
class Gardien_v2(Strategy):
    """_/!\_ adapter pour du deux contre deux"""
    def __init__(self):
        Strategy.__init__(self, "Gardien")

    def compute_strategy(self, state, id_team, id_player):
        # id_team is 1 or 2
        # id_player starts at 0
        position_ball = state.ball.position
        position_joueur = state.player_state(id_team,id_player).position
        but1 = Vector2D(3, GAME_HEIGHT/2)
        but2 = Vector2D(GAME_WIDTH-3, GAME_HEIGHT/2)
        if (id_team == 2):
            new_position_joueur = but2 - position_joueur
        else:
            new_position_joueur = but1 - position_joueur
        w = position_ball - new_position_joueur
        if( id_team == 2 and w.norm < 5 or (state.ball.position+5*state.ball.vitesse).x>110):
            tir =(but1-position_ball)
            tir.angle -= 0.7853
            return SoccerAction(acceleration = (position_ball-position_joueur)*maxPlayerAcceleration,shoot=tir*3)
      
        if( id_team == 1 and w.norm < 5 or state.ball.position.x<40):
            tir=(but2-position_ball)
            tir.angle -= 0.7853
            return SoccerAction(acceleration = (position_ball-position_joueur)*maxPlayerAcceleration,shoot=tir*3)
        else:
            return SoccerAction(acceleration = new_position_joueur)

			
class Attaquant_v2(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Attaquantv_2")
        
    def compute_strategy(self,state,id_team,id_player):
        fct = fonctions(state,id_team,id_player)
        ball = state.ball.position
        but = fct.posi_but()
        if (fct.tirer_ou_pas()):
            return fct.aller_courrir_marcher(ball + 5*state.ball.vitesse) + fct.shoot_but(but)
        else:
            return fct.aller_courrir_marcher(ball)  


        
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team1.add("kiwi", RandomStrategy())  # Random strategy
team1.add("bobby", GardienStrategy()) 

team2.add("Fonceur", FonceurStrategy())   # Static strategy
#team2.add("nemo", FonceurStrategy()) 

team2.add("jimmy", GardienStrategy()) 

# Create a match
simu = Simulation(team1, team2)
# Simulate and display the match
#show_simu(simu)
