#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 21:53:28 2019

@author: emeline
"""
from superstate import *
import math
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings

def liste_joueur(state, id_team, id_player):
    return [state.player_state(id_team,id_player) for(id_team , id_player ) in state.players if id_team == self.id_team]

def ami_proche(state, id_team, id_player):
    return min(liste_joueur(state, id_team, id_player))
    #return allies
def adv_proche(state, id_team, id_player):
    return min(liste_joueur(state, id_team_adv(), id_player))

def distance(state, id_team, id_player, cible):
    dist = math.sqrt(math.pow((cible.x - state.player_state(id_team, id_player).position.x),2) + 
                     math.pow((cible.y - state.player_state(id_team, id_player).position.y),2))
    return dist 
 
    
def passe(self):
    return SoccerAction(acceleration = Vector2D(), shoot = (self.plus_proche_ami()-self.posi_joueur()))
    
def anticiper_ball(self):
    return self.posi_ball() + self.state.ball.vitesse.normalize()
    
def distanceBut(state, id_team, id_player):
    
     s = SuperState(state, id_team,id_player)
     dist = math.sqrt(math.pow((s.goal.x - state.player_state(id_team, id_player).position.x),2) +  math.pow((s.goal.y - state.player_state(id_team, id_player).position.y),2))
     return dist    


def id_team_adv(self):
    if(self.id_team ==1):
        return 2
    return 1
    
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