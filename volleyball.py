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

GAME_WIDTH = 180
GAME_HEIGHT = 90

class Echauffement(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Echauffement")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        dist_players = distance(state, id_team, id_player, adv_position)
        v = adv_position - s.player
        v.norm = dist_players
      
        vector = Vector2D(x =  adv_position.x, y =  adv_position.y ,angle = v.angle, norm = dist_players)
        
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = vector)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
         
class Attaque(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        
        if(id_team_adv(id_team) == 2):
            y_plus = adv_position.y + max(abs(GAME_HEIGHT - adv_position.y  ), abs( adv_position.y ) )
            x_plus =  adv_position.x + max(abs((GAME_WIDTH/2 ) - adv_position.x ), abs((GAME_WIDTH ) - adv_position.x ))
            v_plusloin = Vector2D(x_plus, y_plus)
        else : 
            y_plus = adv_position.y + max(abs(adv_position.y - GAME_HEIGHT ), abs(GAME_HEIGHT - adv_position.y )) 
            x_plus = adv_position.x -  max(abs((GAME_WIDTH/2 ) - adv_position.x ), abs( adv_position.x ))
            
            v_plusloin = Vector2D(x_plus, y_plus)
            
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = v_plusloin - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
            
class Defense(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Attaque")

    def compute_strategy(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        
        if(id_team_adv(id_team) == 2):
            y_plus = adv_position.y + max(abs(GAME_HEIGHT - adv_position.y  ), abs( adv_position.y ) )
            x_plus =  adv_position.x + max(abs((GAME_WIDTH/2 ) - adv_position.x ), abs((GAME_WIDTH ) - adv_position.x ))
            v_plusloin = Vector2D(x_plus, y_plus)
        else : 
            y_plus = adv_position.y + max(abs(adv_position.y - GAME_HEIGHT ), abs(GAME_HEIGHT - adv_position.y )) 
            x_plus = adv_position.x -  max(abs((GAME_WIDTH/2 ) - adv_position.x ), abs( adv_position.x ))
            
            v_plusloin = Vector2D(x_plus, y_plus)
            
        if(balle_dans_mon_camp(state, id_team, id_player) == True ):  
            if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
                return SoccerAction(shoot = v_plusloin - s.player)
            return SoccerAction(acceleration = s.ball - s.player)
        else:
            return SoccerAction(acceleration = v_plusloin - s.player)
     
class Strat_Switch(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Switch")
            
    def compute_strategy_def(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        
        y_plus = max(abs(adv_position.y - GAME_HEIGHT ), abs(GAME_HEIGHT - adv_position.y )) % GAME_HEIGHT
        x_plus = max(abs(adv_position.x - (GAME_WIDTH/2 ) ), abs((GAME_WIDTH/2 ) - adv_position.x )) % GAME_WIDTH
        v_plusloin = Vector2D(x_plus, y_plus)

        
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = v_plusloin - s.player)
        elif(dist * pow(-1, id_team) > GAME_HEIGHT/2 * pow(-1, id_team)):  
            return SoccerAction(acceleration = s.ball - s.player)
        else:
            return SoccerAction(acceleration = v_plusloin - s.player)
    def compute_strategy_attack(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
        adv_position = state.player_state(id_team_adv(id_team),id_player).position
        en_fonction_de_team = pow(-1,id_team)
        if(id_team_adv(id_team) == 2):
            y_plus = max(abs(adv_position.y - GAME_HEIGHT ), abs(GAME_HEIGHT - adv_position.y )) % GAME_HEIGHT
            x_plus = max(abs((GAME_WIDTH/2 ) - adv_position.x ), abs((GAME_WIDTH ) - adv_position.x )) % GAME_WIDTH
            v_plusloin = Vector2D(x_plus, y_plus)
        else : 
            y_plus = max(abs(adv_position.y - GAME_HEIGHT ), abs(GAME_HEIGHT - adv_position.y )) % GAME_HEIGHT
            x_plus = max(abs((GAME_WIDTH/2 ) - adv_position.x ), abs((GAME_WIDTH ) - adv_position.x ))% GAME_WIDTH
            v_plusloin = Vector2D(x_plus, y_plus)
            
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = v_plusloin - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
        
    def compute_strategy(self, state, id_team, id_player):
       
        s = SuperState(state, id_team, id_player)
    
        
        if (balle_dans_mon_camp(state, id_team, id_player) == True):
           return self.compute_strategy_def( state, id_team, id_player)
        else:
           return self.compute_strategy_attack( state, id_team, id_player)
        
       
class RandomStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Random")

    def compute_strategy(self, state, id_team, id_player):
        return SoccerAction(acceleration=Vector2D.create_random(-1, 1),
                            shoot=Vector2D.create_random(-1, 1))


def balle_dans_mon_camp(state, id_team, id_player):
    s = SuperState(state, id_team, id_player)
    if (id_team == 1):
        if(s.ball.x < (GAME_WIDTH/2)):
            return True
        return False
    if (id_team == 2):
        if(s.ball.x > (GAME_WIDTH/2)):
            return True
        return False
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
