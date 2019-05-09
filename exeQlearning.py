#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:16:19 2019

@author: emeline
"""
import random
import pickle as pkl
from Qlearning import *
from QStrategy import *
from Pain_de_mie import *
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings


class FrappeStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Frappe")
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        if mystate.peut_frapper():
            return myaction.shoot_but()
        else :
            return myaction.aller_vers_balle()
        
        

class DribbleStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Dribble")
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        if (mystate.peut_frapper()):
            return myaction.pousse_ball()
        else :    
            return myaction.aller_vers_balle()
            

class PasseStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Passe")
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        if (mystate.peut_frapper()):
            return myaction.passe_2v2()
        else :    
            return myaction.aller_vers_balle()

class Replacement_attaquant_Strategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Replacement offensif")
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.replacement_attaquant4()

class Replacement_defense_Strategy(Strategy):
    def __init__(self):
        Strategy.__init__(self,"Replacement defensif")
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.replacement_defense2()




# Strategy
QTestStrategy = QStrategy()
QTestStrategy.add ( " Frappe " , FrappeStrategy())
QTestStrategy.add ( " Dribble " , DribbleStrategy())
QTestStrategy.add ( " Replacement_Attaque " , Replacement_attaquant_Strategy())
# Learning
expe = QLearning(strategy = QTestStrategy)
expe.start()
with open ('qstrategy.txt','wb') as fo :
    QTestStrategy.qtable = expe.qtable
    pkl.dump(QTestStrategy , fo )
    print(fo)
    
# Tes
with open ( 'qstrategy.pkl','rb') as fi :
    QStrategy = pkl.load(fi)
    print(QStrategy)
    #simu = random.choice(QStrategy.strategy())
    #simu.start()