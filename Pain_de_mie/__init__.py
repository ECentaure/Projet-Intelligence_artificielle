from .tools import *
from .Strategies import *

def get_team(nb_players ):
    team = SoccerTeam ( name = "equipe 3701195" )
    if nb_players == 1:
        team.add(" Striker " , Strat_switch())
    if nb_players == 2:
        team.add(" Gardien " , Defenseur())
        team.add(" Attaquant " ,Attaquant4())
    if nb_players == 4:
        team.add(" Pomme " , Defenseur())
        team.add(" Orange " ,Attaquant4())
        team.add(" Banane " , Defenseur2())
        team.add("Kiwi",Campeur())
    return team
