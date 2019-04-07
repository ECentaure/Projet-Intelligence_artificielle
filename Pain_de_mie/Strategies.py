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
   
class Gardien(Strategy):
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
        fct = SuperState(state,id_team,id_player)
        ball = state.ball.position
        but = fct.goalAdv
        if (fct.tirer_ou_pas()):
            return fct.aller_courrir_marcher(ball + 5*state.ball.vitesse) + fct.shoot_but(but)
        else:
            return fct.aller_courrir_marcher(ball)   
 
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


class Strat_switch(Strategy):
    def __init__(self):
        Strategy.__init__(self, "Switch")
            
    def compute_strategy_def(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)

        if(dist < 50 and distance(state, id_team, id_player, s.goal) < 10):
            if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
               # return SoccerAction(shoot = s.goalAdv - s.player)
                return SoccerAction(shoot = Vector2D(ami_proche_pos(state, id_team, id_player))) #le gardien renvoie le ballon vers son allié le plus proche
                   
            else:
                return SoccerAction(acceleration = s.ball - s.player)
        else:
             return SoccerAction(acceleration = s.goal - s.player)
         
    def compute_strategy_attack(self, state, id_team, id_player):
        s = SuperState(state, id_team, id_player)
        dist = distance(state, id_team, id_player, s.ball)
            
        if( dist < settings.PLAYER_RADIUS + settings.BALL_RADIUS): 
            return SoccerAction(shoot = s.goalAdv - s.player)
        else:
            return SoccerAction(acceleration = s.ball - s.player)
        
    def compute_strategy(self, state, id_team, id_player):
       
        s = SuperState(state, id_team, id_player)
        if(joueur_proche_objet(state,id_team,id_player,state.ball.position))>30 and joueur_proche_objet(state,id_team_adv(id_team),id_player,s.goal)<10 and joueur_proche_objet(state,id_team,id_player,s.goal)<20:
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
team1.add("Defenseur", Attaquant_v2())
 

# Create a match
simu = Simulation(team1, team2)
# Simulate and display the match
#show_simu(simu)
