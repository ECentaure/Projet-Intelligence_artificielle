

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
        
#####################################################################################
#Tout ce qui retourne des positions, ou vitesses (position des joueurs, ballons, ...)
#####################################################################################
        
        
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
    
    def id_team_adv(self):
        if(self.id_team ==1):
            return 2
        return 1
    
    @property
    def goal_deux_coin_bas(self):
        """Position du coin bas du goal1"""
        poteau_bas = self.goalAdv;
        poteau_bas.y += 1.5;
        return poteau_bas

    @property
    def goal_deux_coin_haut(self):
        """Position du coin haut du goal1"""
        poteau_haut = self.goalAdv;
        poteau_haut.y -= 1.5;
        return poteau_haut
    
    def je_suis_dans_mon_camp(self):
        if (self.id_team==1) and (self.player.x<=settings.GAME_WIDTH/2):
            return True
        else:
            return False
        if (self.id_team==2) and (self.player.x>=settings.GAME_WIDTH/2):
            return True
        else:
            return False  
        
    def distance(state, id_team, id_player, cible):
        dist = math.sqrt(math.pow((cible.x - state.player_state(id_team, id_player).position.x),2) + 
                     math.pow((cible.y - state.player_state(id_team, id_player).position.y),2))
        return dist

    def ally_vitesse(self):
        if (self.id_team==1):
            if (self.id_player==0):
                return self.state.player_state(1,1).vitesse
            if (self.id_player==1):
                return self.state.player_state(1,0).vitesse
        if (self.id_team ==2):
            if (self.id_player==0):
                return self.state.player_state(2,1).vitesse
            if (self.id_player ==1):
                return self.state.player_state(2,0).vitesse  
            
    def ally_position(self):
        if (self.id_team==1):
            if (self.id_player==0):
                return self.state.player_state(1,1).position
            if (self.id_player==1):
                return self.state.player_state(1,0).position
        if (self.id_team==2):
            if (self.id_player==0):
                return self.state.player_state(2,1).position
            if (self.id_player==1):
                return self.state.player_state(2,0).position
    
        
    def liste_joueur(state, id_team): #donne une liste de state de tout les joueurs
        return [(it , ip) for (it, ip) in state.players if it == id_team]


    def ami_proche_pos(state, id_team, id_player):
        L = state.liste_joueur(self.id_team_adv()) 
        liste_position = [state.player_state(it,ip).position for (it,ip) in L if ip != id_player]
        L_distance = [distance(state,id_team,id_player,joueur) for joueur in liste_position] #on recupère la position de chaque joeurs 
        return min(L_distance)
        
    def adv_proche_pos(state, id_team, id_player):
        L = state.liste_joueur(self.id_team_adv())
        liste_position = [state.player_state(it,ip).position for (it,ip) in L if ip != id_player]
        L_distance = [distance(state,id_team,id_player,joueur) for joueur in liste_position] #on recupère la position de chaque joeurs 
        return min(L_distance)

    def joueur_proche_objet(self, id_team, id_player,objet):
        Ladv = self.liste_joueur(self.id_team_adv())
        Lami = self.liste_joueur(id_team) 
        Ljoueurs = Ladv+Lami
        L_distance = [distance(state,it,ip,objet) for (it,ip) in Ljoueurs] #on recupère la position de chaque joeurs 
        return min(L_distance)

    def distance2(self, cible):
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



#####################################################################################
#Toutes les fonctions de shoot, de passe ou de running
#####################################################################################
    @property
    def aller_vers_ball(self):
        """Fonce vers la balle"""
        return SoccerAction(self.position_ball - self.player)
    
    
    def shoot(self,p):
        return SoccerAction(Vector2D(),p-self.player)

    @property
    def foncer_but_adv(self):
        """Cours avec la ball vers le goal deux"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball).normalize().scale(2))
        return self.fonce_ball

    @property
    def foncer_but(self):
        """Cours avec la ball vers le goal un (son propre goal)"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (self.goal_un - self.position_ball).normalize().scale(2))
        return self.fonce_ball

    @property
    def shoot_ball(self):
        """Shoot la balle"""
        if self.distance_player_ball < self.rayon_player_ball:
            if self.position_ball.x >= THREE_QUARTER_WIDTH:
                return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball).norm_max(4))
            else:
                return SoccerAction(Vector2D(), (self.goal_deux - self.position_ball))
        return self.fonce_ball

    @property
    def shoot_ball_coin_bas(self):
        """Shoot la balle au coin bas, c'est à dire au premier poto du goal_deux"""
        return SoccerAction(Vector2D(), (self.goal_deux_coin_bas - self.position_ball).norm_max(4))
    
    @property
    def shoot_ball_coin_haut(self):
        """Shoot la balle au coin haut, c'est à dire au deuxième poto du goal_deux"""
        return SoccerAction(Vector2D(), (self.goal_deux_coin_haut - self.position_ball).norm_max(4))

    @property
    def shoot_ball_smart(self):
        """Choisi quand shooter au premier ou au deuxième poto ou sur l'un des deux côtés s'il se trouve au beau milieu """
        if self.distance_player_ball < self.rayon_player_ball:
            if (self.position_ball.y <= GAME_HEIGHT - 46) and (self.position_ball.x >= MEDIUM_WIDTH - 5):
                return self.shoot_ball_coin_bas
            elif (self.position_ball.y >= GAME_HEIGHT - 44) and (self.position_ball.x >= MEDIUM_WIDTH - 5):
                return self.shoot_ball_coin_haut
            L = [self.shoot_ball_coin_bas, self.shoot_ball_coin_haut]
            return choice(L)
        return self.fonce_ball

    #Pas de "@property" car pass_proche prend des paramètres
    def pass_proche(self, qui=1):
        """Passe la ball au joueur le plus proche"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (self.proche(qui) - self.position_ball).norm_max(5))
        return self.fonce_ball
    
    def pass_proche_goal_adv(self, qui=1):
        """Donne la ball au joueur le plus proche du goal adverse"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = self.tic_tac(qui).x + 10, y = self.tic_tac(qui).y) - self.position_ball).norm_max(2.5))
        return self.fonce_ball
    
    @property
    def passe_g(self):
        """Shoot la balle vers la gauche avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH, y = THREE_QUARTER_HEIGHT) - self.position_ball))
        return self.fonce_ball
    
    @property
    def passe_g_normalize(self):
        """Shoot la balle vers la gauche avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH - 5, y = THREE_QUARTER_HEIGHT - 5) - self.position_ball).normalize().scale(3))
        return self.fonce_ball

    @property 
    def passe_d(self):
        """Shoot la balle vers la droite avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH, y = QUARTER_HEIGHT) - self.position_ball))
        return self.fonce_ball

    @property 
    def passe_d_normalize(self):
        """Shoot la balle vers la droite avec un angle de 45 dégré"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = THREE_QUARTER_WIDTH - 5, y = QUARTER_HEIGHT + 5) - self.position_ball).normalize().scale(3))
        return self.fonce_ball

    @property
    def defense_shoot_g(self):
        """Shoot la balle vers la gauche avec un x qui est le centre du terrain"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), Vector2D(x = MEDIUM_WIDTH + 30, y = GAME_HEIGHT - 20) - self.position_ball)
        return self.fonce_ball

    @property
    def defense_shoot_d(self):
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), Vector2D(x = MEDIUM_WIDTH + 30, y = 20) - self.position_ball)
        return self.fonce_ball

    @property
    def keeper_shoot_g(self):
        """Shoot vers la gauche du milieu du terrain"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = MEDIUM_WIDTH, y = GAME_HEIGHT - 10) - self.position_ball).norm_max(6))
        return self.fonce_ball

    @property
    def keeper_shoot_d(self):
        """Shoot vers la droite du milieu du terrain"""
        if self.distance_player_ball < self.rayon_player_ball:
            return SoccerAction(Vector2D(), (Vector2D(x = MEDIUM_WIDTH, y = 10) - self.position_ball).norm_max(6))
        return self.fonce_ball    
    
    def deplaceVers(A, id_joueur):
        player = state.player_state(id_team, id_player).position
        return SoccerAction(acceleration = A - player)
    
    def shooterVersBut(goal,id_team, id_player): 
        player = state.player_state(id_team, id_player).position
        return SoccerAction(shoot = goal - player)    

   

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
    
    def aller_gardien(self,p):
        if (self.id_team==1):
            if (self.ball.x+self.state.ball.vitesse.x>=(settings.GAME_WIDTH)/3) :
                v3=self.ball-self.goalAdv
                v3.norm=8.5
                v2= Vector2D(0,settings.GAME_HEIGHT/2)
                return self.aller_courrir_marcher(v2+v3)       
            else:
                return self.aller_courrir_marcher(p) 
        if (self.id_team==2):
            if(self.ball.x+self.state.ball.vitesse.x<=(2*settings.GAME_WIDTH)/3):
                v3=self.ball-self.goalAdv
                v3.norm=8.5
                v2= Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHT/2)
                return self.aller_courrir_marcher(v2+v3) 
            else:  
                return self.aller_courrir_marcher(p)

