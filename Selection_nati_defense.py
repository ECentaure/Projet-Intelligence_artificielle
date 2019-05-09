
from soccersimulator import Strategy, SoccerAction, Vector2D, SoccerTeam, Simulation, show_simu,settings
from sklearn.model_selection import ParameterGrid
from random import *



GAME_WIDTH = 150
GAME_HEIGHT = 90
CHANCE_TO_MUTATE = 0.1
GRADED_RETAIN_PERCENT = 0.5
CHANCE_RETAIN_NONGRATED = 0.05
POPULATION_COUNT = 100
GRADED_INDIVIDUAL_RETAIN_COUNT = int(POPULATION_COUNT * GRADED_RETAIN_PERCENT)
NB_KEEP = 50
COEFF_MUT = random()*0.1







class DefenseSearch ( object ):
    def __init__ ( self,strategy,attaque,params,simu = None,trials =20,max_steps =1000000,max_round_step=200):
        self.strategy = strategy
        self.attaque = attaque
        self.params = params.copy()
        self.simu = simu
        self.trials = trials
        self.max_steps = max_steps
        self.max_round_step = max_round_step
    
    def start(self,show=True): #modifier à false pour que cela  se fasse automatiquement
        if not self.simu :
            team1 = SoccerTeam( " Team ␣ 1 " )
            team2 = SoccerTeam( " Team ␣ 2 " )
            team1.add (self.strategy.name,self.strategy )
            team2.add (self.attaque.name ,self.attaque)
            self.simu = Simulation(team1,team2 ,max_steps = self.max_steps )
        self.simu.listeners += self
        
        if show:
            show_simu(self.simu)
        else:
            self.simu.start()
    
    def begin_match ( self ,team1, team2, state ):
        self.last_step = 0 # Step of the last round
        self.criterion = self.trials # Criterion to maximize ( here , number of goals )
        self.cpt_trials = 0 # Counter for trials
        self.param_grid= iter(self.params)# a modifier avec les chromosomes (non fonctionnelle) 
        self.cur_param = next(self.param_grid,None)
        #print("test" + str((self.cur_param)))# Current parameter
        if self.cur_param is None:
            raise ValueError( 'no ␣parameter ␣given')
        self.res=dict() # Dictionary of results
    
    def begin_round ( self , team1 , team2 , state ):
        ball = Vector2D(GAME_WIDTH/2, GAME_HEIGHT/2)
        self.simu.state.states [(1,0)].position = Vector2D(0, GAME_HEIGHT/2)  # Player position
        self.simu.state.states [(1,0)].vitesse = Vector2D() # Player accelerati
        self.simu.state.ball.position = ball.copy() # Ball position
        self.last_step = self.simu.step
# Last step of the game
# Set the current value for the current parameters
        print(self.cur_param)
        for key,value in self.cur_param.items():
            setattr(self.strategy,key,value)


    def end_round (self,team1,team2,state):
    # A round ends when there is a goal of if max step is achieved
        if state.goal > 0:
            self.criterion -= 1 
        self.cpt_trials += 1
        print(self.cur_param,end = "____") 
        print( "Crit:_{}___Cpt:_{} ".format(self.criterion,self.cpt_trials))
        if self.cpt_trials >= self.trials :
            self.res[tuple(self.cur_param.items())]= self.criterion*1./self.trials
            # Reset parameters
            self.criterion = 0
            self.cpt_trials = 0
            # Next parameter value
            self.cur_param = next(self.param_grid,None )
            if self.cur_param is None:
                 self.simu.end_match()
                    
           

    def update_round (self, team1 , team2,state ):
# Stop the round if it is too long
        if state.step > self.last_step + self.max_round_step:
            self.simu.end_round()
            
    def get_res(self):
        return self.res
    
    def get_best(self):
        return min(self.res, key=self.res.get)
    
    
    
    def selection(self):
        L = sorted( (value, key) for (key,value) in self.get_res().items())
        Select = []
        for i in range(0,NB_KEEP):
            Select.append(L[i][1][0][1])
        return Select
    
    
    def reproduction(self):
        L = self.selection()
        GEN2 = []
        for  i  in range (0,len(L)//2):
            for j in range (len(L)//2, len(L)):
                n = random()
                if(random() < CHANCE_TO_MUTATE):
                    if(random() < 0.5):
                        GEN2.append(L[i]+ COEFF_MUT)
                    else:
                        GEN2.append(L[j]+ COEFF_MUT)
                    GEN2.append((n*L[i]+ (1-n)*L[j]) + COEFF_MUT)
                else:
                    if(random() < 0.5):
                        GEN2.append(L[i])
                    else:
                        GEN2.append(L[j])
                    GEN2.append( n*L[i]+ (1-n)*L[j] ) # Moyenne pondérée
        return GEN2
    
    def enjambement(self):
        L = self.selection()
        GEN2 = []
        for  i  in range (0,len(L)//2):
            for j in range (len(L)//2, len(L)):
                n = random()
                if(random() < CHANCE_TO_MUTATE):
                    GEN2.append(((L[i]+ L[j])/2) + COEFF_MUT)
                    GEN2.append( ((n*L[i]+ (1-n)*L[j])/2) + COEFF_MUT)
                else:
                    GEN2.append((L[i]+ L[j])/2)
                    GEN2.append( (n*L[i]+ (1-n)*L[j])/2 )
        return GEN2
            
        
