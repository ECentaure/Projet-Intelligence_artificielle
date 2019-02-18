#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 14:38:45 2019

@author: emeline
"""



GAME_WIDTH = 150
GAME_HEIGHT = 90
GAME_GOAL_HEIGHT = 10
PLAYER_RADIUS = 1.
BALL_RADIUS = 0.65
MAX_GAME_STEPS = 2000
maxPlayerSpeed = 1.
maxPlayerAcceleration = 0.2
maxBallAcceleration = 5 

from soccersimulator import *
from math import *

class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player ):
        self . state = state
        self . id_team = id_team
        self . id_player = id_player
        
    @property
    def ball ( self ):
        return self.state.ball.position
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
    @property
    def goalAdv ( self ):
        return Vector2D((2 - self.id_team )*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
    @property
    def goal(self):
        return Vector2D((self.id_team - 1)*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
    
    def liste_joueur(state, id_team, id_player):
        return [state.player_state(id_team,id_player) for(id_team , id_player ) in state.players if id_team == self.id_team]

    def ami_proche(state, id_team, id_player):
        return min(liste_joueur(state, id_team, id_player))
    #return allies
    def adv_proche(state, id_team, id_player):
        return min(liste_joueur(state, id_team_adv(), id_player))

    def distance(self, cible):
        dist = math.sqrt(math.pow((cible.x - self.state.player_state(self.id_team, self.id_player).position.x),2) + 
                     math.pow((cible.y - self.state.player_state(self.id_team, self.id_player).position.y),2))
        return dist 
 
    
    def passe(self):
        return SoccerAction(acceleration = Vector2D(), shoot = (self.plus_proche_ami()-self.player))
    
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
    
        
    def aller_vers(self, vecteur):
        """ renvoie le vecteur déplacement entre le joueur et le point x, y présent dans le champ vecteur"""
        return vecteur-self.player
    
    def distance_j_vect(self,vecteur):
        return vecteur.distance(self.player)
        
    def Immobile(self):
        return SoccerAction(Vector2D(0,0), Vector2D(0,0))  

    def distance_joueur_but(self):
        if (self.id_team == 1):
            but = Vector2D( 0, GAME_HEIGHT/2 )
        else:
            but = Vector2D( GAME_WIDTH, GAME_HEIGHT/2)
        
        return self.player.distance(but)
    
    
    def distance_j_b(self):
        return self.player.distance(self.ball)
     
        
    def tirer_ou_pas(self):
        return self.distance_j_b() < PLAYER_RADIUS + BALL_RADIUS
    
    def aller_courrir(self,p):
        """if (self.posi_ball().x==settings.GAME_WIDTH/2) and (self.posi_ball().y==settings.GAME_HEIGHT/2):
            return SoccerAction(Vector2D(),Vector2D())
        else:"""
        return SoccerAction(acceleration = p-self.player,shoot = Vector2D())
    
    def aller_marcher(self,p):                                                    
        v1=p-self.player
        v1.norm=0.05
        return SoccerAction(acceleration = v1,shoot =Vector2D())

    def aller_courrir_marcher(self,p):
        if (self.distance_j_vect(p)<3):    
            return self.aller_marcher(p)
        return self.aller_courrir(p)
        
    def ball_34(self):
        if self.id_team_adv() == 2:
            if (self.ball.x>(3*settings.GAME_WIDTH)/4):
                return 0                                                           #Attaque
            else:
                return 1                                                           #Defense
        if (self.id_team_adv() == 1):
            if (self.ball.x<(settings.GAME_WIDTH)/4):
                return 0                                                           #Attaque
            else:
                return 1  
        
    def mini_shoot(self,p):
        return SoccerAction(Vector2D(),(p-self.player)*0.03)
    
    def shoot_but(self,p):
        if (self.ball_34()==0):
            return SoccerAction(Vector2D(),(p-self.player)*0.1)
        else:
            return self.mini_shoot(p) 

        
    def decoupage_terrain(self):
        j = self.player
        X_case = math.floor(((j.x)/(150))*4)
        Y_case = math.floor(((j.y)/(90))*3)
        return (X_case,Y_case)

