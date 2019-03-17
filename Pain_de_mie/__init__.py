from .tools import *
from .Strategies import *

def get_team(nb_players ):
    team = SoccerTeam ( name = "equipe 3701195" )
    if nb_players == 1:
        team.add(" Striker " , Strat_switch())
    if nb_players == 2:
        team.add(" Gardien " , Gardien_v2())
        team.add(" Attaquant " ,Attaquant_v2())
    if nb_players == 4:
        team.add(" Gardien " , Gardien_v2())
        team.add(" Attaquant " ,Attaquant_v2())
        team.add(" Striker " , Strat_switch())
        team.add("Go",FonceurStrategy())
    return team
