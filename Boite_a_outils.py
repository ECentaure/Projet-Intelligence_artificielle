from soccersimulator import Strategy, SoccerAction, Vector2D
from soccersimulator import settings
import math

GAME_WIDTH = 150
GAME_HEIGHT = 90
GAME_GOAL_HEIGHT = 10
PLAYER_RADIUS = 1.
BALL_RADIUS = 0.65
MAX_GAME_STEPS = 2000
maxPlayerSpeed = 1.
maxPlayerAcceleration = 0.2
maxBallAcceleration = 5


#Penser à trouver des fonctions de bases demander à otou-san to ane-san

but2 = Vector2D( GAME_WIDTH, GAME_HEIGHT/2. )
but1 = Vector2D( 0, GAME_HEIGHT/2 )

class fonctions(object):
    def __init__(self, state, id_team, id_player):
        self.state = state
        self.id_team = id_team
        self.id_player = id_player
        
   
    def posi_joueur(self):
        """ renvoie position joueur"""
        return self.state.player_state(self.id_team, self.id_player).position
    
    def id_adversaire(self):
        if(self.id_team ==1):
            return 2
        return 1
    
    def posi_ball(self):
        return self.state.ball.position
        
    def aller_vers(self, vecteur):
        """ renvoie le vecteur déplacement entre le joueur et le point x, y présent dans le champ vecteur"""
        return vecteur-self.posi_joueur()
    
    def distance_j_vect(self,vecteur):
        return vecteur.distance(self.posi_joueur())
        
    def Immobile(self):
        return SoccerAction(Vector2D(0,0), Vector2D(0,0))  
        
    def posi_but(self):
        """ Renvoie la position du but selon l'id de la team"""
        return Vector2D((2-self.id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
    
    def distance_j_b(self):
        return self.posi_joueur().distance(self.posi_ball())
    
    def distance_joueur_but(self):
        if (self.id_team == 1):
            but = Vector2D( 0, GAME_HEIGHT/2 )
        but = Vector2D( GAME_WIDTH, GAME_HEIGHT/2)
        
        return self.posi_joueur().distance(but)
    
    def peutShooterAttaque(self):
        if(self.id_adversaire() == 1):
            return self.posi_ball().x > 110
        return self.posi_ball().x <10
        
        
    def tirer_ou_pas(self):
        return self.distance_j_b() < PLAYER_RADIUS + BALL_RADIUS
    
    def aller_courrir(self,p):
        """if (self.posi_ball().x==settings.GAME_WIDTH/2) and (self.posi_ball().y==settings.GAME_HEIGHT/2):
            return SoccerAction(Vector2D(),Vector2D())
        else:"""
        return SoccerAction(p-self.posi_joueur(),Vector2D())
    
    def aller_marcher(self,p):                                                    
        v1=p-self.posi_joueur()
        v1.norm=0.05
        return SoccerAction(v1,Vector2D())

    def aller_courrir_marcher(self,p):
        if (self.distance_j_vect(p)<3):    
            return self.aller_marcher(p)
        return self.aller_courrir(p)
        
    def ball_34(self):
        if self.id_adversaire() == 2:
            if (self.posi_ball().x>(3*settings.GAME_WIDTH)/4):
                return 0                                                           #Attaque
            else:
                return 1                                                           #Defense
        if (self.id_adversaire() == 1):
            if (self.posi_ball().x<(settings.GAME_WIDTH)/4):
                return 0                                                           #Attaque
            else:
                return 1  
        
    def mini_shoot(self,p):
        return SoccerAction(Vector2D(),(p-self.posi_joueur())*0.03)
    
    def shoot_but(self,p):
        if (self.ball_34()==0):
            return SoccerAction(Vector2D(),(p-self.posi_joueur())*0.1)
        else:
            return self.mini_shoot(p) 
