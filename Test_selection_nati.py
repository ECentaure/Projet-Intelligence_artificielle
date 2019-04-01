
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
from Pain_de_mie import *
import math
from Selection_nati import GoalSearch
import numpy
from random import *


def get_random_population_list(a,b):
    L = []
    for i in range(0,10):
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
        return fct.shoot_opti(but,self.power)
        


expe = GoalSearch(strategy = Attaquant_v2(),params = get_random_population_list(0,2))

for i in range(0,11):
    expe.start()
    L = expe.selection()
    R = expe.reproduction()
    NewList = []
    for j in range(0,len(R)):
        NewList.append({"power": R[j]})
    expe = GoalSearch(strategy = Attaquant_v2(),params = NewList)
    
print(expe.get_res())
#NL = sorted( (value, key) for (key,value) in expe.get_res().items()) # Liste permettant de classer les donner en fonction de leur nombre de buts 
#print(NL)
#print(NL[0][1][0][1]) Avoir accèss à la puissance comme le type de cette liste est liste de dictionnaire de tuple...
# print(expe.get_best())  #Permet d'avoir la meilleure valeur
