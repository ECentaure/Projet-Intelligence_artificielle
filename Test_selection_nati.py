
import tools



from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
"""from Pain_de_mie import *"""
import math
from Selection_nati import GoalSearch
from tools import SuperState
import numpy
from random import *


def get_random_population_list(a,b):
    L = []
    for i in range(0,100):
        L.append({"power":(random()*(b-a)+a)})
    return L


class Attaquant_v2(Strategy):
    def __init__(self,power=None):
        Strategy.__init__(self,"Attaquant")
        self.power = power
        
    def compute_strategy(self,state,id_team,id_player):
        fct = SuperState(state,id_team,id_player)
        ball = state.ball.position
        but = fct.goalAdv
        if (fct.tirer_ou_pas()):
            return fct.aller_courrir_marcher(ball + 5*state.ball.vitesse) + fct.shoot(but,self.power)
        else:
            return fct.aller_courrir_marcher(ball)  


expe = GoalSearch(strategy = Attaquant_v2(),params = get_random_population_list(0,2))
expe.start()
print(expe.get_res())
print(expe.get_best())