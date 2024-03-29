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
        dist = s.distance(s.ball)
        
        if(dist < 10):
            if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
                return SoccerAction(shoot = s.goalAdv - s.player)
                #return SoccerAction(shoot = allieProche(state, id_team, id_player))
            else:
                return SoccerAction(acceleration = s.ball - s.player)
        else:
             return SoccerAction(acceleration = s.goal - s.player)
         


    
class Defenseur(Strategy):
    def __init__(self,name="defense"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.defense()
    
class Campeur(Strategy):
    def __init__(self,name="campeur"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.action_campeur()
    
class Milieu(Strategy):
    def __init__(self,name="defense"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.action_milieu()
		
class Defenseur2(Strategy):
    def __init__(self,name="defense"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.defense2()
		
class Attaquant4(Strategy):
    def __init__(self,name="Attaque"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.action_attaquant4()
   


class Strat_switch(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Switch")
            
    def compute_strategy_def(self, state, id_team, id_player):
        mystate = tools.SuperState(state,id_team,id_player)
        myaction= tools.Action(mystate)
        return myaction.defense()
         
    def compute_strategy_attack(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
            
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goalAdv - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
        
    def compute_strategy(self, state, id_team, id_player):
       
        s = SuperState(state, id_team, id_player)
        if(s.ball.distance(s.goal) < 10 or (s.ball.x == GAME_WIDTH/2 and s.ball.y == GAME_HEIGHT/2)):
           return self.compute_strategy_def( state, id_team, id_player)
        else:
           return self.compute_strategy_attack( state, id_team, id_player)
        
# Create teams
team1 = SoccerTeam(name="Team 1")
team2 = SoccerTeam(name="Team 2")

# Add players
team2.add("kiwi",Defenseur2()) 
team2.add("Fonceur", Defenseur()) 
team1.add("Defenseur", Defenseur())   
team2.add("Attaquant", Attaquant4())
team1.add("kiwi",Defenseur2())  
team2.add("Fonceur", FonceurStrategy())  
team1.add("strat",Strat_switch()) 
 

# Create a match
simu = Simulation(team1, team2)
# Simulate and display the match
#show_simu(simu)
