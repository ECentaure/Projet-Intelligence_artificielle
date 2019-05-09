
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
from Pain_de_mie import *
import math
from Selection_nati_defense import DefenseSearch
import numpy
NB_GENERATIONS = 10
from random import *


def get_random_population_list(a,b):
    L = []
    for i in range(0,100):
        L.append({"posix":(random()*(b-a)+a)})
    return L


    
class Attaquant4(Strategy):
    def __init__(self,name="Attaque"):
        Strategy.__init__(self,name)
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.action_attaquant4()
        
class Defenseur(Strategy):
    def __init__(self,posix=None):
        Strategy.__init__(self,"Defenseur")
        self.posix = posix
    def compute_strategy(self,state,idteam,idplayer):
        mystate = tools.SuperState(state,idteam,idplayer)
        myaction= tools.Action(mystate)
        return myaction.defense_opti(self.posix)

expe = DefenseSearch(strategy = Defenseur(),attaque = Attaquant4(), params = get_random_population_list(2,20))

for i in range(0,NB_GENERATIONS):
    expe.start()
    L = expe.selection()
    R = expe.reproduction()
    NewList = []
    for j in range(0,len(R)):
        NewList.append({"posix": R[j]})
    print(expe.get_res())
    expe = DefenseSearch(strategy = Defenseur(),params = NewList,attaque = Attaquant4())
    
    

#NL = sorted( (value, key) for (key,value) in expe.get_res().items()) # Liste permettant de classer les donnees en fonction de leur nombre de buts 
#print(NL)
#print(NL[0][1][0][1]) Avoir accèss à la puissance comme le type de cette liste est liste de dictionnaire de tuple...
# print(expe.get_best())  #Permet d'avoir la meilleure valeur
