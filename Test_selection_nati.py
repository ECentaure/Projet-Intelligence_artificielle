
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
from Pain_de_mie import *
import math
from Selection_nati import GoalSearch
import numpy
NB_GENERATIONS = 10
from random import *


def get_random_population_list(a,b):
    L = []
    for i in range(0,50):
        L.append({"power":(random()*(b-a)+a)})
    return L


    

class Attaquant_v2(Strategy):
    def __init__(self,power=None):
        Strategy.__init__(self,"Attaquant")
        self.power = power
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.action_attaquant4_opti(mystate.goalAdv,self.power)
        
class Defenseur(Strategy):
    def __init__(self,name="defense"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.defense()

expe = GoalSearch(strategy = Attaquant_v2(),defense = Defenseur(),ballx = 105,bally = random()*90,params = get_random_population_list(0.09,0.1))

for i in range(0,NB_GENERATIONS):
    expe.start()
    L = expe.selection()
    R = expe.reproduction()
    NewList = []
    for j in range(0,len(R)):
        NewList.append({"power": R[j]})
    print(expe.get_res())
    expe = GoalSearch(strategy = Attaquant_v2(),defense = Defenseur(),ballx = 105,bally = random()*90,params = NewList)
    
    

#NL = sorted( (value, key) for (key,value) in expe.get_res().items()) # Liste permettant de classer les donnees en fonction de leur nombre de buts 
#print(NL)
#print(NL[0][1][0][1]) Avoir accèss à la puissance comme le type de cette liste est liste de dictionnaire de tuple...
# print(expe.get_best())  #Permet d'avoir la meilleure valeur
