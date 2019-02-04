#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 21:53:28 2019

@author: emeline
"""
from superstate import *
import math
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings

def distance(state, id_team, id_player):
    dist = math.sqrt(math.pow((state.ball.position.x - state.player_state(id_team, id_player).position.x),2) + 
                     math.pow((state.ball.position.y - state.player_state(id_team, id_player).position.y),2))
    return dist 
 
    
def distanceBut(state, id_team, id_player):
    
     s = SuperState(state, id_team,id_player)
     dist = math.sqrt(math.pow((s.goal.x - state.player_state(id_team, id_player).position.x),2) +  math.pow((s.goal.y - state.player_state(id_team, id_player).position.y),2))
     return dist    
    
def deplaceVers(A, id_joueur):
    player = state.player_state(id_team, id_player).position
    return SoccerAction(acceleration = A - player)
    
def shooterVersBut(goal,id_team, id_player): 
    player = state.player_state(id_team, id_player).position
    return SoccerAction(shoot = goal - player)    

def advProchePos(id_team):
    L_adv = [state.player_state(it,ip).position for (it, ip)in state.player if it != id_team]
    return min(L_adv)

def gogetter(state):
    if state.player.distance( state.ball ) < PLAYER_RADIUS + BALL_RADIUS :
        return SoccerAction (shoot = state.goal - state.player )
    else :
        return SoccerAction (acceleration = state.ball - state.player )    