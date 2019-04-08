GAME_WIDTH = 150
GAME_QUARTER = GAME_WIDTH/4
GAME_HALF = GAME_WIDTH/2
GAME_THREE_QUARTER = GAME_WIDTH*3/4
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

class SINGLETON():
    class __SINGLETON:
        def __init__(self, id_team,id_player):
            self.id_team = id_team
            self.id_player = id_player
        def __str__(self):
            return repr(self) + self.val
    instance = None 
    def __init__(self,id_team,id_player):
        if not SINGLETON.instance:
            SINGLETON.instance = SINGLETON.__SINGLETON(id_team,id_player)
        else:
            SINGLETON.instance.id_team = id_team
            SINGLETON.instance.id_player = id_player
    def __getattr__(self, name):
        return getattr(self.instance,name)        


class SuperState ( object ):
    def __init__ ( self , state , id_team , id_player ):
        self . state = state
        self . id_team = id_team
        self . id_player = id_player
	
    @property
    def ball(self):
        return self.state.ball.position
    @property
    def ball_vitesse(self):
        return self.state.ball.vitesse
		
    @property
    def player(self):
        return self.state.player_state(self.id_team, self.id_player).position
		
    @property
    def goalAdv ( self ):
        return Vector2D((2 - self.id_team )*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
		
    @property
    def goal(self):
        return Vector2D((self.id_team - 1)*settings.GAME_WIDTH , settings.GAME_HEIGHT / 2)
	
    @property
    def position_defenseur(self):
        if self.id_team == 2 :
            return Vector2D(GAME_WIDTH*(15.0/16),GAME_HEIGHT/2)
        return Vector2D(GAME_WIDTH/16.0,GAME_HEIGHT/2)
    
    def frappe_position(self):
        return abs((self.ball-self.goalAdv).x)<=45
    
    @property
    def aller_vect(self):
        return SoccerAction(self.vect_anticipe-self.player,Vector2D())
    @property	
    def vect_anticipe(self):    
        return (self.ball+ 5.75*self.state.ball.vitesse)
   
    @property              
    def vect_anticipe_att(self):    
        return self.state.ball + 4.5*self.state.ball.vitesse 

    def id_team_adv(self):
        if(self.id_team ==1):
            return 2
        return 1
    
    
    def distance_j_b(self):
        return self.player.distance(self.ball)
     
    def attaquant4_position_dribble(self):
        return abs((self.ball-self.goal).x)>70
        
    def tirer_ou_pas(self):
        return self.distance_j_b() < PLAYER_RADIUS + BALL_RADIUS
    
    def aller_courrir(self,p):
        return SoccerAction(acceleration = p-self.player,shoot = Vector2D())
    
    def vers_but(self,p):
        if(self.player.distance(self.ennemi_proche(self.id_team,self.id_player)) < 8):
            return self.contourne()
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
            
        
            
    def get_dir_jeu(self):
        return  (self.goalAdv-self.goal).normalize()
    
    
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
    @property
    def can_def(self):
        if self.id_team == 1 :
            if self.ball.x<(GAME_WIDTH/4.0)+10 :
                return True
            return False
        if self.ball.x>(GAME_WIDTH*(3.0/4))-10 :
            return True
        return False
    
    def can_def2(self):
        if self.id_team == 1 :
            if self.ball.x < GAME_HALF-10 and self.ball.x> GAME_WIDTH*(2/10):
                return True
            return False
        if self.ball.x > (GAME_HALF+10) and self.ball.x < GAME_WIDTH*(8/10):
            return True
        return False
        
    
    def ball_position_future(self):
        if self.ball_vitesse.norm > 2 or self.ball_vitesse.norm < -2:
            return self.ball+self.ball_vitesse*10
        else :
            return self.ball
        
        
    def shoot(self,p):
        return SoccerAction(Vector2D(),(p-self.player))
    
    def peut_frapper(self):
        return (self.ball-self.player).norm <= settings.PLAYER_RADIUS + settings.BALL_RADIUS 
    
    def je_suis_dans_mon_camp(self):
        if (self.id_team==1) and (self.player.x<=settings.GAME_WIDTH/2):
            return True
        else:
            return False
        if (self.id_team==2) and (self.player.x>=settings.GAME_WIDTH/2):
            return True
        else:
            return False 
    @property    
    def ball_camp(self):
        if (pow(-1 ,self.id_team) * self.ball.x) >= (pow(-1 ,self.id_team) *settings.GAME_WIDTH/2):
            return True
        else:
            return False
    
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
    
    def est_proche_adv(self,p):
        opponents = [self.state.player_state(id_team, id_player).position for (id_team, id_player) in self.state.players if ( id_team != self.id_team)]
        for i in range(0, len(opponents)):
            if(p.distance(opponents[i]) < 3):
                return True
        return False
    
 
    def ennemi_proche(self, id_team, id_player):
        opponents = [self.state.player_state(id_team, id_player) for (id_team, id_player) in self.state.players if (id_team != self.id_team)]
        return min([(self.player.distance(player_p.position), player_p.position) for player_p in opponents])[1]
    
    def joueur_proche_rang(self, rang):
        """ Classe tous les joueurs de l'équipe du player du  plus proche au plus loin et renvoie le joueur corresponsant au rang"""
        LP= [self.state.player_state(it,ip).position for (it,ip) in self.state.players if it == self.id_team and ip != self.id_player]
        L_distance = [(self.player.distance(player_p), player_p) for player_p in LP]#on recupère la position de chaque joeurs 
        L_distance.sort()
        return L_distance[rang-1][1]
        
			
			
class Action(object):
    def __init__(self,state):
        self.state = state   
    
    def aller(self,p):
        return SoccerAction((p-self.state.player),Vector2D())
    
    def aller_vers_balle(self):
        return self.aller(self.state.ball+self.state.ball_vitesse)
    
    def shoot(self,p):
        return SoccerAction(Vector2D(),0.1*(p-self.state.player))
    
    def shoot_but(self):
        return self.shoot(self.state.goalAdv) 
        
    def pousse_ball(self):
        return SoccerAction(Vector2D(),(self.state.goalAdv- self.state.ball_position_future())*0.015) # 0.02 constante pour le dribble

    def pousse_ball_centre(self):
        if self.state.domicile():
            return SoccerAction(Vector2D(),(Vector2D(0,10)))
        else :
            return SoccerAction(Vector2D(),(Vector2D(-1,-2)))
        
    def position_coop_2v2(self):
        nb_coop=len([idp for (idt, idp) in self.state.players if idt == self.idteam])
        return self.state.player_state(self.key[0],(1+self.key[1])%(nb_coop)).position
    
    def degagement(self):
        return self.shoot_but()
    
    def passe(self,p):
        return SoccerAction(Vector2D(),(p-self.state.player).norm_max(3))

    def passe_2v2(self):
        return self.shoot(self.state.position_coop_2v2())

#====================================================================================================================================
#            Replacement 

    
    def replacement_milieu(self):
        return self.aller(Vector2D(self.state.get_dir_jeu().x*45+self.state.position_mon_but().x,45))

    def replacement_attaquant4(self):
        return self.aller(Vector2D(self.state.get_dir_jeu().x*80+self.state.goal.x,self.state.ball.y))
		
    def replacement_defense2(self):
        if(self.state.id_team == 1):
            return self.aller(Vector2D(GAME_HEIGHT/2, GAME_QUARTER))
        return self.aller(Vector2D(GAME_HEIGHT/2,GAME_THREE_QUARTER))
#====================================================================================================================================
#                 Action Joueur    
    
    def action_milieu(self):
         if self.state.milieu_position_action():
            if not self.state.peut_frapper():
                return self.aller_vers_balle()
            else:
                return self.passe_2v2()
         else :
            return self.replacement_milieu()
        
    def action_attaquant4(self):
        if self.state.attaquant4_position_dribble():
            if not self.state.peut_frapper():
                return self.aller_vers_balle()
            elif not (self.state.frappe_position()):
                return self.pousse_ball()
            else :
                return self.shoot_but()
        else :
            return self.replacement_attaquant4()
        
        
    def defense(self):
        if self.state.peut_frapper() :
            return self.degagement()
        if self.state.can_def :
            return self.state.aller_vect
        if self.state.ball.x>(GAME_WIDTH*(3.0/4))-5 :
            return self.state.aller_vect
        return self.aller(self.state.position_defenseur)
    
    def defense2(self):
        if self.state.ball_camp:
            if self.state.peut_frapper():
                j1 = self.state.joueur_proche_rang(3)
                j2 = self.state.joueur_proche_rang(2)
                if self.state.est_proche_adv(j1):
                    return self.degagement()
                elif self.state.est_proche_adv(j2):
                    return self.degagement()
                else:
                    if(self.state.player.distance(j2) > self.state.player.distance(j1)):
                        return self.passe(j2)
                    else:
                        return self.passe(j1)
            else:
                 if self.state.can_def2():
                     return self.state.aller_vect
                 else:
                     return SoccerAction(acceleration = Vector2D(0, self.state.ball.y-self.state.player.y), shoot = Vector2D(0,0))            
        else:
            if(self.state.id_team == 1):
                return self.aller(Vector2D(GAME_QUARTER,GAME_HEIGHT/2))
            else:
                return self.aller(Vector2D(GAME_THREE_QUARTER,GAME_HEIGHT/2))
            
def egalite_float(a,b):
    if(abs(a-b) < 0.0001):
        return True
    return False
    
   
def Shooter(state, id_team, id_player, singleton):
        s = SuperState(state, id_team, id_player);
        singleton.id_team = id_team  #le dernier joueur a avoir le ballon
        singleton.id_player = id_player
        return SoccerAction(shoot = s.goalAdv - s.player)
    
def id_team_adv(p):
        if(p ==1):
            return 2
        return 1
    
def tir_rebond(state, id_team, id_player, cible):
    s =SuperState(state , id_team , id_player )
    A = settings.GAME_HEIGTH - (s.goalAdv.y/2) 
    O = s.goal.x - s.player.x
    Angle = math.acos(A/O) * (180/math.pi)
    Gamma = (90 - Angle) * (math.pi/180)
    SoccerAction(angle = Gamma)
    
def liste_joueur(state, id_team): #donne une liste de state de tout les joueurs
    return [(it , ip) for (it, ip) in state.players if it == id_team]


def ami_proche_pos(state, id_team, id_player):
    L = liste_joueur(state, id_team) 
    liste_position = [state.player_state(it,ip).position for (it,ip) in L if ip != id_player]
    L_distance = [distance(state,id_team,id_player,joueur) for joueur in liste_position] #on recupère la position de chaque joeurs 
    return min(L_distance)

def ami_proche(state, id_team, id_player):
    L = liste_joueur(state, id_team) 
    liste_position = [state.player_state(it,ip).position for (it,ip) in L if ip != id_player]
    L_distance = [distance(state,id_team,id_player,joueur) for joueur in liste_position] #on recupère la position de chaque joeurs 
    return [(it,ip) for (it,ip) in L if egalite_float(distance(state,id_team,id_player,state.player_state(it,ip).position),  min(L_distance)) == True and ip != id_player][0]

    #return allies
def adv_proche_pos(state, id_team, id_player):
    L = liste_joueur(state, id_team_adv(id_team)) 
    liste_position = [state.player_state(it,ip).position for (it,ip) in L if ip != id_player]
    L_distance = [(distance(state,id_team,id_player,joueur),joueur) for joueur in liste_position] #on recupère la position de chaque joeurs 
    return min(L_distance)

def joueur_proche_objet(state, id_team, id_player,objet):
    Ladv = liste_joueur(state, id_team_adv(id_team)) 
    Lami = liste_joueur(state, id_team) 
    Ljoueurs = Ladv+Lami
    L_distance = [distance(state,it,ip,objet) for (it,ip) in Ljoueurs] #on recupère la position de chaque joeurs 
    return min(L_distance)

def distance(self, cible):
    dist = math.sqrt(math.pow((cible.x - self.state.player_state(self.id_team, self.id_player).position.x),2) + 
                 math.pow((cible.y - self.state.player_state(self.id_team, self.id_player).position.y),2))
    return dist 
 

def passe(self,state, id_team, id_player,cible_pos):
    s =SuperState(state , id_team , id_player )
    v = Vector2D(cible_pos - s.player) 
    return SoccerAction(acceleration = Vector2D(), angle = v.angle)

def anticiper_ball(self):
    return self.posi_ball() + self.state.ball.vitesse.normalize()

def distanceBut(state, id_team, id_player):

    s = SuperState(state, id_team,id_player)
    dist = math.sqrt(math.pow((s.goal.x - state.player_state(id_team, id_player).position.x),2) +  math.pow((s.goal.y - state.player_state(id_team, id_player).position.y),2))
    return dist    


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

def distance(state, id_team, id_player, cible):
     dist = math.sqrt(math.pow((cible.x - state.player_state(id_team, id_player).position.x),2) + math.pow((cible.y - state.player_state(id_team, id_player).position.y),2))
     return dist 